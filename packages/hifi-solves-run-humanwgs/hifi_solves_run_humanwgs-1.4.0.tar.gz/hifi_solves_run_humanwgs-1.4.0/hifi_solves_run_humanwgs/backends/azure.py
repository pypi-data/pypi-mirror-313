import os
import pandas as pd
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureSasCredential
from azure.core.exceptions import (
    ResourceNotFoundError,
    ClientAuthenticationError,
    ServiceRequestError,
)
from ..constants import get_reference_data
from datetime import datetime, timezone
import regex as re


def _get_credential():
    """
    Get Azure credentials using a SAS token

    Returns:
        credential (AzureSasCredential): credential used to auth with Azure
    """
    sas_token = os.getenv("AZURE_STORAGE_SAS_TOKEN", None)
    if sas_token is not None:
        try:
            credential = AzureSasCredential(sas_token)
        except ClientAuthenticationError as e:
            raise SystemExit(f"Encountered an issue when retrieving credentials: {e}")
    else:
        raise SystemExit("Must set and export the AZURE_STORAGE_SAS_TOKEN env variable")

    # Confirm that the SAS token is not expired
    try:
        expiry = datetime.fromisoformat(
            re.search(
                r"se=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)",
                sas_token,
            ).group(1)
        )

        if expiry < datetime.now(timezone.utc):
            raise SystemExit(
                "AZURE_STORAGE_SAS_TOKEN is expired; please contact your administrator to get a new token."
            )
    except:
        print("[WARN] Failed when checking if SAS token was expired; proceeding anyway")

    return credential


def validate_bucket(blob_container):
    """
    Confirm that the target upload container exists

    Args:
        blob_container (str): Storage account, container, and optional path within container to upload data to; format <storage_account>/<container>[/<path_prefix>]

    Returns:
        formatted_container_url (str): Formatted container URL with paths stripped
        path_prefix (str): Path within the container to upload files to
    """
    storage_account = blob_container.split("/")[0]
    container_and_path = blob_container.split("/")[1:]
    formatted_container = container_and_path[0]
    path_prefix = (
        None if len(container_and_path) == 1 else "/".join(container_and_path[1:])
    )
    try:
        credential = _get_credential()
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account}.blob.core.windows.net",
            credential=credential,
        )
        container_client = blob_service_client.get_container_client(formatted_container)

        # if we're able to list blobs, it means the container exists and is accessible
        next(container_client.list_blobs())
        print("\t✓ Target container exists and is accessible")
        return f"{storage_account}/{formatted_container}", path_prefix

    except StopIteration:
        # if we're able to list blobs but the container is empty, it's still accessible
        print("\t✓ Target container exists and is accessible")
        return f"{storage_account}/{formatted_container}", path_prefix

    except ClientAuthenticationError as e:
        raise SystemExit(f"✗ Authentication failed: {e}")
    except ServiceRequestError as e:
        raise SystemExit(f"✗ Azure configuration error: {e}")
    except ResourceNotFoundError:
        raise SystemExit(
            f"\t✗ Target container {formatted_container} does not exist in storage account {storage_account}."
        )
    except Exception as e:
        raise SystemExit(
            f"\t✗ Something went wrong when checking if the target container {blob_container} exists.\n\t{e}"
        )


def check_file_exists(blob_container, path_prefix, file_path, sample_id, file_type):
    """
    Check if a file exists in the container; determine the expected path for remote files
    Args:
        blob_container (str): Storage account, container to upload data to; format <storage_account>/<container>
        path_prefix (str): Path within the container to upload files to
        file_path (str): Local path to the file
        sample_id (str): Unique identifier for sample
        file_type (str): File type (e.g., bam)

    Returns:
        file_exists (bool): True if the file exists at remote; False if it does not
        remote_path (str): Expected path to the file in target container
        file_size_bytes (int): If the file exists, the size of the file in bytes
    """
    storage_account, container = blob_container.split("/")

    file_basename = os.path.basename(file_path)
    file_size_bytes = None

    # File is located in Azure Blob Storage and in the target container
    ## These files can be at different paths within the container than the expected one
    expected_prefix = f"/{storage_account}/{container}/"
    if file_path.startswith(expected_prefix):
        remote_path = file_path.removeprefix(expected_prefix)
    elif file_path.startswith(f"/{storage_account}/") and not file_path.startswith(
        expected_prefix
    ):
        raise SystemExit(
            f"\t✗ Remote file path [{file_path}] is outside of the target container. Please download this file to local storage to allow it to be reuploaded to the target container."
        )
    # File is local; we'll upload to {path_prefix}/{sample_id}/{file_type}/{file_basename}
    else:
        remote_path = f"{path_prefix + '/' if path_prefix else ''}{sample_id}/{file_type}/{file_basename}"
    try:
        credential = _get_credential()
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account}.blob.core.windows.net",
            credential=credential,
        )
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=remote_path
        )
        object_metadata = blob_client.get_blob_properties()
        file_size_bytes = object_metadata["size"]
        print(f"\t✓ {file_basename}")
        return True, remote_path, file_size_bytes
    except (ClientAuthenticationError, ServiceRequestError) as e:
        raise SystemExit(f"✗ Azure configuration error: {e}")
    except ResourceNotFoundError:
        print(f"\t✗ {file_basename}")
        return False, remote_path, file_size_bytes
    except Exception as e:
        raise SystemExit(
            f"\t✗ Something went wrong when checking if the remote file {container}/{remote_path} in storage account {storage_account} exists.\n{e}"
        )


def upload_files(blob_container, files_to_upload):
    """
    Upload files to the target container

    Args:
        blob_container (str): Storage account, container to upload data to; format <storage_account>/<container>
        files_to_upload (dict): Dictionary of files to upload with keys=local path to file, values=remote path
    """
    storage_account, container = blob_container.split("/")

    credential = _get_credential()
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account}.blob.core.windows.net",
        credential=credential,
        max_single_put_size=4 * 1024 * 1024,
        connection_timeout=600,
    )
    container_client = blob_service_client.get_container_client(container)

    if len(files_to_upload) > 0:
        print("Uploading files to target container")
    for local_path, remote_path in files_to_upload.items():
        try:
            blob_client = container_client.get_blob_client(remote_path)
            with open(local_path, "rb") as data:
                blob_client.upload_blob(data)
            print(f"\t✓ {os.path.basename(local_path)}")
        except ClientAuthenticationError as e:
            raise SystemExit(f"✗ Authentication failed: {e}")
        except ServiceRequestError as e:
            raise SystemExit(f"✗ Azure configuration error: {e}")
        except ResourceNotFoundError:
            raise SystemExit(
                f"\t✗ Error uploading file {local_path}: The specified container {container} does not exist."
            )
        except Exception as e:
            raise SystemExit(f"\t✗ Error uploading file {local_path}: {e}")


def generate_inputs_json(
    sample_info,
    phenotypes,
    reference_inputs_bucket,
    workflow_file_outputs_bucket,
    region=None,
    container_registry=None,
    **kwargs,
):
    """
    Generate the inputs JSON needed to execute a workflow run

    Args:
        sample_info (pd.DataFrame): Sample information
        phenotypes (List[str]): List of phenotypes associated with this cohort
        reference_inputs_bucket (str): Bucket where reference files are located
        workflow_file_outputs_bucket (str): Bucket where workflow output files will be written
        region (str): Region to run the workflow in; does not need to be specified when backend is AZURE
        container_registry (str): Alternate container registry to pull workflow images from; defaults to [PacBio's public Quay.io](https://quay.io/organization/pacbio)

    Returns:
        humanwgs_inputs (dict): Inputs JSON with all values filled out
        engine_params (dict): Configuration parameters for the engine
    """
    engine_params = {}

    samples = sample_info.drop(columns=["family_id", "total_file_size_bytes"]).to_dict(
        orient="records"
    )
    samples_no_null_values = [
        {
            key: value
            for key, value in sample.items()
            if isinstance(value, list) or pd.notnull(value)
        }
        for sample in samples
    ]

    cohort = {
        "cohort_id": sample_info["family_id"].unique()[0],
        "samples": samples_no_null_values,
        "phenotypes": phenotypes,
    }

    reference_inputs_bucket = f"/{reference_inputs_bucket}"
    workflow_file_outputs_bucket = f"/{workflow_file_outputs_bucket}"

    reference_data, slivar_data = get_reference_data(reference_inputs_bucket)
    humanwgs_inputs = {
        "HumanWGS_wrapper.cohort": cohort,
        "HumanWGS_wrapper.reference": reference_data,
        "HumanWGS_wrapper.slivar_data": slivar_data,
        "HumanWGS_wrapper.backend": "Azure",
        "HumanWGS_wrapper.preemptible": True,
        "HumanWGS_wrapper.workflow_outputs_bucket": workflow_file_outputs_bucket,
    }

    if container_registry is not None:
        humanwgs_inputs["HumanWGS_wrapper.container_registry"] = container_registry

    print("\t✓ Workflow inputs ready")
    return humanwgs_inputs, engine_params
