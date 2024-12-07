import os, json
import pandas as pd
from google.cloud import storage
from google.cloud.exceptions import NotFound, Forbidden
from ..constants import get_reference_data

# GCP project information
try:
    credentials_json_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_json_file is None:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
        )
    with open(credentials_json_file, "r") as file:
        credentials = json.load(file)
    project_id = credentials.get("project_id")
    if project_id is None:
        raise ValueError("\t✗ GCP_PROJECT_ID was not found in the credentials JSON.")
except json.JSONDecodeError:
    raise SystemExit("\t✗ The credentials JSON is invalid.")
except ValueError as e:
    raise SystemExit(f"\t✗ {e}")


def validate_bucket(bucket_name):
    """
    Confirm that the target upload bucket exists in GCP; strip gs:// prefix if present

    Args:
        bucket_name (str): Name of the GCS bucket
    Returns:
        formatted_bucket (str): Formatted bucket name
        path_prefix (str): Path within the bucket to upload files to
    """
    bucket_and_path = bucket_name.removeprefix("gs://").rstrip("/").split("/")
    formatted_bucket = bucket_and_path[0]
    path_prefix = None if len(bucket_and_path) == 1 else "/".join(bucket_and_path[1:])

    try:
        storage_client = storage.Client(project=project_id)
        storage_client.get_bucket(formatted_bucket)
        print("\t✓ Target bucket exists and is accessible")
        return formatted_bucket, path_prefix
    except (NotFound, Forbidden):
        raise SystemExit(
            f"\t✗ Target bucket {bucket_name} does not exist or you do not have access to it. If you're certain the bucket exists, contact an administrator or log in using a different profile."
        )
    except Exception as e:
        raise SystemExit(
            f"\t✗ Something went wrong when checking if the target bucket {bucket_name} exists.\n\t{e}"
        )


def check_file_exists(bucket_name, path_prefix, file_path, sample_id, file_type):
    """
    Check if a file exists in the GCS bucket; determine the expected path for remote files

    Args:
        bucket_name (str): Name of the GCS bucket
        path_prefix (str): Path within the bucket to upload files to
        file_path (str): Local path to the file
        sample_id (str): Unique identifier for sample
        file_type (str): File type (e.g., bam)

    Returns:
        file_exists (bool): True if the file exists, False otherwise
        remote_path (str): Expected path to the file in target bucket
            file_size_bytes (int): If the file exists, the size of the file in bytes
    """
    file_basename = os.path.basename(file_path)
    file_size_bytes = None

    # File is in GCS in the target bucket
    ## These files can be at different paths within the bucket than the expected one
    if file_path.startswith(f"gs://{bucket_name}/") or file_path.startswith(
        f"{bucket_name}/"
    ):
        remote_path = file_path.removeprefix("gs://").removeprefix(f"{bucket_name}/")
    # File is in GCS, but not in the target bucket; ask user to download the file locally
    elif file_path.startswith("gs://"):
        raise SystemExit(
            f"\t✗ Remote file path [{file_path}] is outside of the target bucket. Please download this file to local storage to allow it to be reuploaded to the target bucket."
        )
    # File is local; we'll upload to {path_prefix}/{sample_id}/{file_type}/{file_basename}
    else:
        remote_path = f"{path_prefix + '/' if path_prefix else ''}{sample_id}/{file_type}/{file_basename}"

    try:
        storage_client = storage.Client(project=project_id)
        bucket_client = storage_client.bucket(bucket_name)
        object_metadata = bucket_client.get_blob(blob_name=remote_path)
        if object_metadata is not None:
            file_size_bytes = object_metadata.size
            print(f"\t✓ {file_basename}")
            return True, remote_path, file_size_bytes
        else:
            print(f"\t✗ {file_basename}")
            return False, remote_path, file_size_bytes
    except NotFound:
        print(f"\t✗ {file_basename}")
        return False, remote_path, file_size_bytes
    except Exception as e:
        raise SystemExit(
            f"\t✗ Something went wrong when checking if the remote file {bucket_name}/{remote_path} exists.\n{e}"
        )


def upload_files(bucket_name, files_to_upload):
    """
    Upload files to the target GCS bucket

    Args:
        bucket_name (str): Name of the GCS bucket to upload data to
        files_to_upload (dict): Dictionary of files to upload with keys=local path to file, values=remote path within the bucket
    """
    if len(files_to_upload) > 0:
        print("Uploading files to target bucket")
        storage_client = storage.Client(project=project_id)
        bucket_client = storage_client.bucket(bucket_name)

    for local_path, remote_path in files_to_upload.items():
        try:
            blob = bucket_client.blob(remote_path)
            blob.upload_from_filename(local_path)
            print(f"\t✓ {os.path.basename(local_path)}")
        except (NotFound, Forbidden):
            raise SystemExit(f"\t✗ Target bucket {bucket_name} does not exist.")
        except Exception as e:
            raise SystemExit(f"\t✗ Error uploading file {local_path}: {e}")


def generate_inputs_json(
    sample_info,
    phenotypes,
    reference_inputs_bucket,
    workflow_file_outputs_bucket,
    region,
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
        region (str): GCP region to run the workflow in
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

    reference_inputs_bucket = f"gs://{reference_inputs_bucket}"
    workflow_file_outputs_bucket = f"gs://{workflow_file_outputs_bucket}"

    reference_data, slivar_data = get_reference_data(reference_inputs_bucket)
    humanwgs_inputs = {
        "HumanWGS_wrapper.cohort": cohort,
        "HumanWGS_wrapper.reference": reference_data,
        "HumanWGS_wrapper.slivar_data": slivar_data,
        "HumanWGS_wrapper.backend": "GCP",
        "HumanWGS_wrapper.preemptible": True,
        "HumanWGS_wrapper.workflow_outputs_bucket": workflow_file_outputs_bucket,
        "HumanWGS_wrapper.zones": f"{region}-b {region}-c",  # According to https://cloud.google.com/compute/docs/regions-zones, all regions have zones with the -b and -c suffixes
    }

    if container_registry is not None:
        humanwgs_inputs["HumanWGS_wrapper.container_registry"] = container_registry

    print("\t✓ Workflow inputs ready")
    return humanwgs_inputs, engine_params
