import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
from math import ceil
import pandas as pd
from ..constants import get_reference_data


def validate_bucket(bucket):
    """
    Confirm that the target upload bucket exists; strip s3:// prefix

    Args:
        bucket (str): Bucket and optional path within bucket to upload data to

    Returns:
        formatted_bucket (str): Formatted bucket name with s3:// and any paths stripped
        path_prefix (str): Path within the bucket to upload files to
    """
    bucket_and_path = bucket.removeprefix("s3://").rstrip("/").split("/")
    formatted_bucket = bucket_and_path[0]
    path_prefix = None if len(bucket_and_path) == 1 else "/".join(bucket_and_path[1:])

    s3 = boto3.client("s3")

    try:
        s3.head_bucket(Bucket=formatted_bucket)
        print("\t✓ Target bucket exists and is accessible")
        return formatted_bucket, path_prefix
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise SystemExit(f"Target bucket {bucket} does not exist.")
        elif e.response["Error"]["Code"] == "403":
            raise SystemExit(
                f"You do not have access to target bucket {bucket}; contact an administrator, or log in using a different profile."
            )
        else:
            raise e
    except NoCredentialsError as e:
        raise SystemExit(
            f"\t✗ {e}\n\tTo set AWS credentials, see https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html"
        )
    except Exception as e:
        raise SystemExit(
            f"\t✗ Something went wrong when checking if the target bucket {bucket} exists.\n\t{e}"
        )


def check_file_exists(bucket, path_prefix, file_path, sample_id, file_type):
    """
    Check if a file exists in the bucket; determine the expected path for remote files

    Args:
        bucket (str): Bucket to check for existence of files
        path_prefix (str): Path within the bucket to upload files to
        file_path (str): Local path to the file
        sample_id (str): Unique identifier for sample
        file_type (str): File type (e.g. bam)

    Returns:
        file_exists (bool): True if the file exists at remote; False if it does not
        remote_path (str): Expected path to the file in target bucket
        file_size_bytes (int): If the file exists, the size of the file in bytes
    """
    file_basename = os.path.basename(file_path)
    file_size_bytes = None

    # File is in s3 in the target bucket
    ## These files can be at different paths within the bucket than the expected one
    if file_path.startswith(f"s3://{bucket}/") or file_path.startswith(f"{bucket}/"):
        remote_path = file_path.removeprefix("s3://").removeprefix(f"{bucket}/")
    # File is in s3, but not in the target bucket; ask user to download the file locally
    elif file_path.startswith("s3://"):
        raise SystemExit(
            f"Remote file path [{file_path}] is outside of the target bucket. Please download this file to local storage to allow it to be reuploaded to the target bucket."
        )
    # File is local; we'll upload to {path_prefix}/{sample_id}/{file_type}/{file_basename}
    else:
        remote_path = f"{path_prefix + '/' if path_prefix else ''}{sample_id}/{file_type}/{file_basename}"

    try:
        s3 = boto3.client("s3")
        object_metadata = s3.head_object(Bucket=bucket, Key=remote_path)
        file_size_bytes = object_metadata["ContentLength"]
        print(f"\t✓ {file_basename}")
        return True, remote_path, file_size_bytes
    except ClientError as e:
        # File does not exist
        if e.response["Error"]["Code"] == "404":
            print(f"\t✗ {file_basename}")
            return False, remote_path, file_size_bytes
        else:
            raise e
    except Exception as e:
        raise SystemExit(
            f"Something went wrong when checking if the remote file {bucket}/{remote_path} exists.\n{e}"
        )


def upload_files(bucket, files_to_upload):
    """
    Upload files to the target bucket

    Args:
        bucket (str): Bucket to upload data to
        files_to_upload (dict): Dictionary of files to upload with keys=local path to file, values=remote path
    """
    s3 = boto3.client("s3")
    if len(files_to_upload) > 0:
        print("Uploading files to target bucket")
    for local_path, remote_path in files_to_upload.items():
        try:
            s3.upload_file(local_path, bucket, remote_path)
            print(f"\t✓ {os.path.basename(local_path)}")
        except Exception as e:
            raise SystemExit(f"Error uploading file {local_path}: {e}")


def generate_inputs_json(
    sample_info,
    phenotypes,
    reference_inputs_bucket,
    workflow_file_outputs_bucket,
    region=None,
    container_registry=None,
    aws_storage_capacity=None,
    **kwargs,
):
    """
    Generate the inputs JSON needed to execute a workflow run

    Args:
        sample_info (pd.DataFrame): Sample information
        phenotypes (List[str]): List of phenotypes associated with this cohort
        reference_inputs_bucket (str): Bucket where reference files are located
        workflow_file_outputs_bucket (str): Bucket where workflow output files will be written
        region (str): Region to run the workflow in; does not need to be specified when backend is AWS
        container_registry (str): Alternate container registry to pull workflow images from; defaults to [PacBio's public Quay.io](https://quay.io/organization/pacbio)

    Returns:
        humanwgs_inputs (dict): Inputs JSON with all values filled out
        engine_params (dict): Configuration parameters for the engine
    """
    engine_params = {}
    # HealthOmics will round up to the nearest multiple of 1200 GB, with a min of 1.2 TB and a max of 9.6 TB
    # [Docs](https://docs.aws.amazon.com/omics/latest/dev/workflows-run-types.html)
    min_healthomics_storage_gigabytes = 1200
    max_healthomics_storage_gigabytes = 9600

    # Dynamic storage
    if aws_storage_capacity == "DYNAMIC":
        engine_params = {"storage_type": "DYNAMIC"}
    # Static storage
    else:
        # Set storage capacity using user override
        if aws_storage_capacity is not None:
            estimated_storage_capacity = int(aws_storage_capacity)
        # Storage capacity not set; we'll estimate it based on input file sizes
        else:
            total_file_size_gigabytes = sum(sample_info["total_file_size_bytes"]) / (
                1024 * 1024 * 1024
            )
            estimated_storage_capacity = int(ceil(total_file_size_gigabytes * 8)) + 50

        # Set minimum storage to 1.2 TB, regardless of other settings
        if estimated_storage_capacity < min_healthomics_storage_gigabytes:
            print(
                f"\t[WARN] Estimated required intermediate storage capacity [{estimated_storage_capacity / 1000} TB] is lower than HealthOmics' minimum capacity of {min_healthomics_storage_gigabytes / 1000} TB.\n\tSetting to the HealthOmics minimum."
            )
            estimated_storage_capacity = min_healthomics_storage_gigabytes
        # Set maximum storage to 9.6 TB, regardless of other settings
        if estimated_storage_capacity > max_healthomics_storage_gigabytes:
            print(
                f"\t[WARN] Estimated required intermediate storage capacity [{estimated_storage_capacity / 1000} TB] exceeds HealthOmics' maximum capacity of {max_healthomics_storage_gigabytes / 1000} TB.\n\tSetting to the HealthOmics max, but the workflow may fail due to running out of disk space."
            )
            estimated_storage_capacity = max_healthomics_storage_gigabytes

        engine_params = {
            "storage_type": "STATIC",
            "storage_capacity": estimated_storage_capacity,
        }

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

    reference_inputs_bucket = f"s3://{reference_inputs_bucket}"
    workflow_file_outputs_bucket = f"s3://{workflow_file_outputs_bucket}"

    reference_data, slivar_data = get_reference_data(reference_inputs_bucket)
    humanwgs_inputs = {
        "HumanWGS_wrapper.cohort": cohort,
        "HumanWGS_wrapper.reference": reference_data,
        "HumanWGS_wrapper.slivar_data": slivar_data,
        "HumanWGS_wrapper.backend": "AWS",
        "HumanWGS_wrapper.preemptible": True,
        "HumanWGS_wrapper.workflow_outputs_bucket": workflow_file_outputs_bucket,
    }

    if container_registry is not None:
        humanwgs_inputs["HumanWGS_wrapper.container_registry"] = container_registry

    print("\t✓ Workflow inputs ready")
    return humanwgs_inputs, engine_params
