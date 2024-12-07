#!/usr/bin/env python3

from argparse import ArgumentParser

import importlib
import pkg_resources
import os
import pandas as pd
from pathlib import Path
import re
import subprocess
import json
import hashlib
from .constants import (
    WORKBENCH_URL,
    WORKFLOW_NAME,
    WORKFLOW_VERSION,
    DERIVED_WORKFLOW_VERSION,
    AWS_CONTAINER_REGISTRY_ACCOUNT,
)

from importlib.metadata import version


def parse_args():
    """
    Parse command-line arguments

    Returns:
        args (argparse.Namespace): Parsed command-line arguments
    """
    parser = ArgumentParser(
        description="Upload genomics data and run PacBio's official Human WGS pipeline"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version('hifi_solves_run_humanwgs')}; HumanWGS workflow {WORKFLOW_VERSION}, revision {DERIVED_WORKFLOW_VERSION}",
        help="Program version",
    )

    sample_info_group = parser.add_argument_group(
        "Sample information",
        "Provide either --sample-info, OR both --movie-bams and --fam-info",
    )
    sample_info_group.add_argument(
        "-s",
        "--sample-info",
        required=False,
        type=str,
        help="Path to sample info CSV or TSV. This file should have columns [family_id, sample_id, movie_bams, phenotypes, father_id, mother_id, sex]. See documentation for more information on the format of this file.",
    )
    sample_info_group.add_argument(
        "-m",
        "--movie-bams",
        required=False,
        type=str,
        help="Path to movie bams CSV or TSV. This file should have columns [sample_id, movie_bams]. Repeated rows for each sample can be added if the sample has more than one associated movie bam.",
    )

    sample_info_group.add_argument(
        "-c",
        "--fam-info",
        required=False,
        type=str,
        help="Path to family information. This file should have columns [family_id, sample_id, father_id, mother_id, sex [, phenotype1, phenotype2, phenotype3, ... phenotypeN]]. Any number of phenotype columns may be added after the sex column; the column names should be HPO terms, and values should be 2 for 'affected' or 1 for 'unaffected'.",
    )

    parser.add_argument(
        "-b",
        "--backend",
        required=True,
        type=str.upper,
        help="Backend where infrastructure is set up",
        choices=["AWS", "GCP", "AZURE"],
    )

    parser.add_argument(
        "-r",
        "--region",
        required=True,
        type=str,
        help="Region where infrastructure is set up",
    )

    parser.add_argument(
        "-o",
        "--organization",
        required=True,
        type=str,
        help="Organization identifier; used to infer bucket names",
    )

    parser.add_argument(
        "-e",
        "--engine",
        required=False,
        type=str,
        help="Engine to use to run the workflow. Defaults to the default engine set in Workbench.",
    )

    parser.add_argument(
        "-u",
        "--upload-only",
        required=False,
        action="store_true",
        help="Upload movie BAMs and generate inputs JSON only; do not submit the workflow. If set, --write-inputs-json will also be set automatically.",
    )

    parser.add_argument(
        "-i",
        "--write-inputs-json",
        required=False,
        action="store_true",
        help="Write inputs JSON and engine configuration to a file. Files will be named {family_id}.inputs.json, {family_id}.engine_params.json, {family_id}.run_tags.json.",
    )

    parser.add_argument(
        "-f",
        "--force-rerun",
        required=False,
        default=False,
        action="store_true",
        help="Force rerun samples that have previously been run",
    )

    # AWS-specific
    parser.add_argument(
        "--aws-storage-capacity",
        required=False,
        type=str.upper,
        help="Storage capacity override for AWS HealthOmics backend. Defaults to total size of input BAMs across all samples * 8. Supply either the requested storage capacity in GB, or 'DYNAMIC' to set storage to dynamic.",
    )

    args = parser.parse_args()
    if args.sample_info is not None:
        if args.movie_bams is not None or args.fam_info is not None:
            parser.error(
                "Either --sample-info alone, or both --movie-bams and --fam-info should be defined, not both.",
            )
    else:
        if args.movie_bams is None or args.fam_info is None:
            parser.error(
                "If --sample-info is not defined, both --movie-bams and --fam-info must be set.",
            )

    if args.upload_only:
        args.write_inputs_json = True

    aws_storage_capacity = args.aws_storage_capacity
    if aws_storage_capacity is not None:
        if args.backend != "AWS":
            print("[WARN] --aws-storage-capacity argument ignored for non-AWS backend.")
        else:
            try:
                args.aws_storage_capacity = int(aws_storage_capacity)
            except ValueError:
                if args.aws_storage_capacity != "DYNAMIC":
                    parser.error(
                        "The value for --aws-storage-capacity must either by DYNAMIC or an integer representing the total storage capacity in GB."
                    )

    return args


def load_sample_info(sample_info_csv, movie_bam_csv, fam_file):
    """
    Load the sample info DataFrame, either from a single CSVs or a fam file and a CSV

    Args:
        sample_info_csv (str): Path to CSV containing all required sample information.
                               This file should have columns [family_id, sample_id, movie_bams, phenotypes, father_id, mother_id, sex]
        movie_bam_csv (str): Path to a file relating samples to their corresponding set of movie BAM files
        fam_file (str): Path to a FAM info file. See [here](https://www.cog-genomics.org/plink/2.0/formats#fam) for format. Note that multiple phenotype columns may be added.

    Returns:
        sample_info (pd.DataFrame): DataFrame containing sample information
    """
    if sample_info_csv is not None:
        sample_info = pd.read_csv(
            sample_info_csv,
            sep=None,
            engine="python",
            dtype={
                "family_id": str,
                "sample_id": str,
                "movie_bams": str,
                "phenotypes": str,
                "father_id": str,
                "mother_id": str,
                "sex": str,
            },
        )
        sample_info.columns = (
            sample_info.columns.str.strip().str.lower().str.replace(" ", "_")
        )
    else:
        movie_bams = pd.read_csv(
            movie_bam_csv,
            sep=None,
            engine="python",
            dtype={"sample_id": str, "movie_bams": str},
        )
        movie_bams.columns = (
            movie_bams.columns.str.strip().str.lower().str.replace(" ", "_")
        )
        fam = pd.read_csv(fam_file, sep=None, engine="python")
        fam.columns = fam.columns.str.strip()
        fam_columns = fam.columns.tolist()

        # Don't modify phenotype column names
        fam.columns = [
            col.lower().replace(" ", "_") for col in fam_columns[:5]
        ] + fam_columns[5:]
        fam = fam.rename(
            columns={
                "fid": "family_id",
                "iid": "sample_id",
                "fatheriid": "father_id",
                "father_iid": "father_id",
                "f_iid": "father_id",
                "motheriid": "mother_id",
                "mother_iid": "mother_id",
                "m_iid": "mother_id",
            }
        )

        def extract_affected_phenotypes(row):
            sample_id = row["sample_id"]
            affected_phenotypes = [col for col in fam.columns[5:] if row[col] == 2]
            return [(sample_id, phenotype) for phenotype in affected_phenotypes]

        movie_and_fam = pd.merge(
            movie_bams, fam.drop(fam.columns[5:], axis=1), on="sample_id", how="outer"
        )

        sample_phenotypes = pd.DataFrame(
            fam.apply(extract_affected_phenotypes, axis=1).explode().dropna().tolist(),
            columns=["sample_id", "phenotypes"],
        )

        sample_info = pd.merge(
            movie_and_fam, sample_phenotypes, on="sample_id", how="outer"
        )

    # Strip whitespace from values
    sample_info = sample_info.apply(
        lambda x: x.str.strip() if x.dtype == "object" else x
    )

    return sample_info


def import_backend_module(backend):
    """
    Import backend-specific functions

    Args:
        backend (str): Backend where infrastructure is set up ["AWS", "GCP", "AZURE"]

    Returns:
        (module): Module containing backend-specific functions
    """
    try:
        backend_module = importlib.import_module(
            f".backends.{backend.lower()}", package="hifi_solves_run_humanwgs"
        )
    except:
        raise ImportError(f"✗ Module backends.{backend.lower()} not found.")

    return backend_module


def _confirm_unqiue_values(sample_info, columns):
    """
    Confirm that there is exactly one unique value for each family_id/sample_id combination for a set of columns in the DataFrame

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information
        columns (List[str]): Set of columns to check

    Raises:
        ValueError: If there is more than one unique value for any combination of family_id, sample_id
    """
    sample_info = sample_info.set_index(["family_id", "sample_id"])
    for column in columns:
        unique_values = sample_info.groupby(["family_id", "sample_id"])[
            column
        ].nunique()
        if (unique_values > 1).any():
            problematic_samples = sample_info[
                sample_info.index.isin(unique_values[unique_values > 1].index)
            ]
            raise ValueError(
                f"\t✗ There should be exactly one unique value of {column} for each combination of family_id, sample_id\n{problematic_samples}"
            )


def _standardize_sex(sample_info):
    """
    Standardize the representation of sex in the sample_info DataFrame

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information

    Returns:
        sample_info (pd.DataFrame): DataFrame containing sample information with sex standardized
    """
    sex_mapping = {
        "MALE": "MALE",
        "M": "MALE",
        "1": "MALE",
        "FEMALE": "FEMALE",
        "F": "FEMALE",
        "2": "FEMALE",
        "None": None,
        "UNKNOWN": None,
        "0": None,
        "-1": None,
        "Null": None,
    }

    def map_sex(value):
        if pd.isna(value):
            return None
        elif str(value).upper() in sex_mapping:
            return sex_mapping[str(value).upper()]
        else:
            raise KeyError(
                f"Invalid sex '{value}'; should be one of ['MALE', 'FEMALE', None (empty value)]"
            )

    sample_info["sex"] = sample_info["sex"].map(map_sex)

    return sample_info


def _extract_phenotypes(sample_info):
    """
    Confirm that phenotypes are set properly and return the set of unique phenotypes. Set the phenotype to the root HPO term if the proband can be determined.
    Set the affected column based on the value of phenotypes.

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information

    Returns:
        phenotypes (pd.Series): Series containing phenotypes
        sample_info (pd.DataFrame): DataFrame containing sample information with phenotypes set
    """
    root_phenotypes = ["HP:0000001"]
    # Set phenotype to the root HPO term if it has not been defined
    if sample_info["phenotypes"].isnull().all():
        # If there is a single sample, set the phenotype to the root HPO term
        if len(sample_info) == 1:
            sample_info.at[0, "phenotypes"] = root_phenotypes

        # If there are several samples but one is a proband, set the phenotype to the root HPO term
        elif (
            len(
                sample_info[
                    sample_info["mother_id"].notnull()
                    | sample_info["father_id"].notnull()
                ]
            )
            == 1
        ):
            proband_index = sample_info[
                sample_info["mother_id"].notnull() | sample_info["father_id"].notnull()
            ].index[0]
            sample_info.at[proband_index, "phenotypes"] = root_phenotypes

        # Otherwise, raise an error and ask the user to fill this out more clearly
        else:
            raise ValueError(
                "\t✗ Must define at least one phenotype for the proband. If no particular phenotypes are desired, the root HPO term, 'HP:0000001', can be used."
            )

    # Confirm that all phenotypes match the HPO regex
    hpo_regex = re.compile(r"^HP:[0-9]{7}$")
    invalid_phenotypes = set(
        filter(
            lambda phenotype: not hpo_regex.match(phenotype),
            sample_info["phenotypes"].explode().dropna().unique(),
        )
    )
    if len(invalid_phenotypes) > 0:
        raise ValueError(
            f"\t✗ Invalid HPO term(s) found: {invalid_phenotypes}\nHPO terms should be of the form HP:xxxxxxx, where x is a digit 0-9. See [the Human Phenotype Ontology](https://hpo.jax.org/app/) for more information."
        )

    # Confirm that there is exactly one possible set of phenotypes across all samples
    unique_phenotype_sets = (
        sample_info["phenotypes"]
        .apply(lambda x: tuple(x) if x is not None else None)
        .dropna()
        .unique()
    )
    if len(unique_phenotype_sets) > 1:
        raise ValueError(
            f"\t✗ There should be exactly one unique set of phenotypes across all samples; found {unique_phenotype_sets}"
        )

    phenotypes = list(unique_phenotype_sets[0])

    # Set the affected column based on the value of phenotypes
    sample_info["affected"] = sample_info["phenotypes"].apply(
        lambda x: True if x == phenotypes else False
    )

    sample_info = sample_info.drop("phenotypes", axis=1)

    return phenotypes, sample_info


def validate_format_sample_info(sample_info):
    """
    Validate that sample_info contains the required information and reformat it

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information

    Returns:
        formatted_sample_info (pd.DataFrame): Reformatted and validated sample information
        phenotypes (List[str]): List of phenotypes associated with this cohort
    """
    required_columns = ["family_id", "sample_id", "movie_bams"]
    optional_columns = ["phenotypes", "father_id", "mother_id", "sex"]

    # Confirm all the required columns are present
    missing_required_columns = set(required_columns) - set(sample_info.columns)
    if missing_required_columns:
        raise ValueError(
            f"\t✗ Missing required columns: {', '.join(sorted(missing_required_columns))}"
        )
    for col in optional_columns:
        if col not in sample_info.columns:
            sample_info[col] = None

    # Confirm that there is exactly one family ID in this file
    if sample_info["family_id"].nunique() != 1:
        raise ValueError(
            f"\t✗ There should be exactly one unique value of family_id in the sample_info file; found {list(sample_info['family_id'].unique())}\nTo run multiple families, make separate family info files"
        )

    sample_info = _standardize_sex(sample_info)

    # Confirm that there is exactly one unique value of mother_id, father_id, sex for each combination of family_id, sample_id
    _confirm_unqiue_values(sample_info, ["mother_id", "father_id", "sex"])

    # Gather movie_bams, phenotypes for each family_id-sample_id combination
    sample_info = (
        sample_info.groupby(["family_id", "sample_id"])
        .agg(
            {
                "movie_bams": lambda x: (
                    (sorted(list(set(x.dropna())))) if x.notnull().any() else None
                ),
                "phenotypes": lambda x: (
                    sorted(list(set(x.dropna()))) if x.notnull().any() else None
                ),
                "father_id": "first",
                "mother_id": "first",
                "sex": "first",
            }
        )
        .reset_index()
    )

    phenotypes, sample_info = _extract_phenotypes(sample_info)

    # Confirm that there are no null values in any required column
    na_values = sample_info[required_columns].isna().any()
    if na_values.any():
        missing_value_columns = na_values[na_values].index.tolist()
        raise ValueError(
            f"\t✗ Missing values found in required columns: {', '.join(missing_value_columns)}"
        )

    # Confirm that there are no duplicate movie bams across different samples
    movie_bams = sample_info["movie_bams"].explode().dropna()
    if len(movie_bams) != len(set(movie_bams)):
        seen_bams = set()
        duplicate_bams = set()
        for movie_bam in movie_bams:
            if movie_bam in seen_bams:
                duplicate_bams.add(movie_bam)
            else:
                seen_bams.add(movie_bam)
        raise ValueError(f"\t✗ Duplicate movie bams found: {', '.join(duplicate_bams)}")

    return sample_info, phenotypes


def _check_file_exists_locally(file_path):
    """
    Check if a file exists locally

    Args:
        file_path (str): Path to file

    Returns:
        file_exists (bool): True if file exists at path; False if it does not
        file_size_bytes (int): If the file exists, the size of the file in bytes
    """
    file_exists = Path(file_path).exists()
    file_size_gb = None
    if file_exists:
        file_size_gb = Path(file_path).stat().st_size
    return file_exists, file_size_gb


def upload_files(
    sample_info,
    backend_module,
    raw_data_bucket,
    backend,
    path_prefix=None,
):
    """
    Check whether files exist in the raw_data_bucket; if not, upload them

    Args:
        sample_info (pd.DataFrame): Sample information
        backend_module (module): Module containing backend-specific functions
        raw_data_bucket (str): Bucket where workflow input files will be uploaded
        backend (str): Backend where infrastructure is set up ["AWS", "GCP", "AZURE"]
        path_prefix (str): Path within the bucket to upload files to

    Returns:
        formatted_sample_info (pd.DataFrame): Sample information with movie bams paths
            translated to their remote equivalent
        total_file_size_bytes (int): Total size of all input movie bams
    """
    print("Checking whether files exist in the target bucket")
    file_info = {}
    sample_file_size_bytes = {}
    for sample_id, file_path in sample_info["movie_bams"].explode().items():
        exists_locally, local_size_bytes = _check_file_exists_locally(file_path)
        exists_at_remote, remote_path, remote_size_bytes = (
            backend_module.check_file_exists(
                raw_data_bucket, path_prefix, file_path, sample_id, "bam"
            )
        )
        file_size_bytes = remote_size_bytes or local_size_bytes
        file_info[file_path] = {
            "exists_locally": exists_locally,
            "exists_at_remote": exists_at_remote,
            "remote_path": remote_path,
            "file_size_bytes": file_size_bytes,
        }
        try:
            if sample_id in sample_file_size_bytes:
                sample_file_size_bytes[sample_id] += file_size_bytes
            else:
                sample_file_size_bytes[sample_id] = file_size_bytes
        except TypeError:
            raise SystemExit(
                f"Failed to retrieve file size for file {file_path}; exiting"
            )

    sample_info["total_file_size_bytes"] = sample_info["sample_id"].map(
        sample_file_size_bytes
    )

    # Error if any files do not exist locally or at remote
    files_not_found = [
        k
        for k, v in file_info.items()
        if not v["exists_locally"] and not v["exists_at_remote"]
    ]
    if len(files_not_found) > 0:
        raise FileNotFoundError(
            f"\t✗ Some files were not found locally or in raw data bucket [{raw_data_bucket}]. Check paths? Files with issues:\n{files_not_found}"
        )

    # Upload files that are local only to remote
    files_to_upload = {
        k: v["remote_path"]
        for k, v in file_info.items()
        if v["exists_locally"] and not v["exists_at_remote"]
    }
    backend_module.upload_files(raw_data_bucket, files_to_upload)

    # Define cloud-specific prefixes
    if backend == "AWS":
        prefix = "s3://"
    elif backend == "AZURE":
        prefix = "/"
    elif backend == "GCP":
        prefix = "gs://"

    sample_info["movie_bams"] = sample_info["movie_bams"].apply(
        lambda x: [
            (f"{prefix}{raw_data_bucket}/{file_info[movie_bam]['remote_path']}")
            for movie_bam in x
        ]
    )

    return sample_info


def _register_workflow():
    """
    Register a workflow in Workbench

    Returns:
        workflow_id (str): Workflow ID for the registered workflow
    """
    package_path = pkg_resources.resource_filename("hifi_solves_run_humanwgs", "")
    entrypoint_path = os.path.join(package_path, "workflows", "hifisolves_wrapper.wdl")

    workflow_info = subprocess.run(
        [
            "omics",
            "workbench",
            "workflows",
            "create",
            "--name",
            WORKFLOW_NAME,
            "--version-name",
            DERIVED_WORKFLOW_VERSION,
            "--entrypoint",
            entrypoint_path,
        ],
        capture_output=True,
        text=True,
    )
    if workflow_info.returncode == 0:
        try:
            workflow_info_json = json.loads(workflow_info.stdout)
            workflow_id = workflow_info_json["internalId"]
            print("\t✓ Registered workflow")
            return workflow_id
        except json.JSONDecodeError as e:
            print(f"\t✗ Error parsing JSON: {e}")
    else:
        raise SystemExit(
            f"\t✗ Something went wrong when attempting to register the workflow\n{workflow_info.stderr}"
        )


def _register_workflow_version(workflow_id):
    """
    Register a workflow version in Workbench
    """
    package_path = pkg_resources.resource_filename("hifi_solves_run_humanwgs", "")
    entrypoint_path = os.path.join(package_path, "workflows", "hifisolves_wrapper.wdl")

    version_info = subprocess.run(
        [
            "omics",
            "workbench",
            "workflows",
            "versions",
            "create",
            "--workflow",
            workflow_id,
            "--name",
            DERIVED_WORKFLOW_VERSION,
            "--entrypoint",
            entrypoint_path,
        ],
        capture_output=True,
        text=True,
    )

    if version_info.returncode == 0:
        print("\t✓ Registered workflow version")
    else:
        raise SystemExit(
            f"\t✗ Something went wrong when attempting to register a workflow version\n{version_info.stderr}"
        )


def get_workflow_id(workflow_name, workflow_version):
    """
    Get the workflow ID for the HumanWGS workflow, or register it if it does not exist

    Args:
        workflow_name (str): Name of the workflow
        workflow_version (str): Workflow version

    Returns:
        workflow_id (str): Workflow ID for the HumanWGS wrapper workflow
    """

    # See if the workflow exists
    workflow_list = subprocess.run(
        [
            "omics",
            "workbench",
            "workflows",
            "list",
            "--source",
            "PRIVATE",
            "--search",
            workflow_name,
        ],
        capture_output=True,
        text=True,
    )

    if workflow_list.returncode == 0:
        try:
            workflow_list_json = json.loads(workflow_list.stdout)
            filtered_workflow_list = [
                workflow
                for workflow in workflow_list_json
                if workflow["name"] == workflow_name
            ]
            if len(filtered_workflow_list) > 0:
                workflow_id = filtered_workflow_list[0]["internalId"]

                # See if this version of the workflow exists
                versions_list = subprocess.run(
                    [
                        "omics",
                        "workbench",
                        "workflows",
                        "versions",
                        "list",
                        "--workflow",
                        workflow_id,
                    ],
                    capture_output=True,
                    text=True,
                )

                if versions_list.returncode == 0:
                    try:
                        versions_list_json = json.loads(versions_list.stdout)
                        all_versions = [v["id"] for v in versions_list_json]
                        if workflow_version in all_versions:
                            print("\t✓ Workflow found in Workbench")
                        else:
                            print(
                                f"\tWorkflow version {workflow_version} not found for workflow {workflow_name}; registering new version"
                            )
                            _register_workflow_version(workflow_id)
                    except json.JSONDecodeError as e:
                        raise SystemExit(
                            f"\t✗ Error parsing JSON: {e}\n{versions_list.stderr}"
                        )
                else:
                    raise SystemExit(
                        f"\t✗ Something went wrong when listing workflow versions\n{versions_list.stderr}"
                    )
            else:
                print("\tWorkflow not found in Workbench; registering workflow")
                workflow_id = _register_workflow()
        except json.JSONDecodeError as e:
            raise SystemExit(f"\t✗ Error parsing JSON: {e}\n{workflow_list.stderr}")
    else:
        raise SystemExit(
            f"\t✗ Something went wrong when listing workflows\n{workflow_list.stderr}"
        )
    return workflow_id


def write_inputs_json(family_id, workflow_inputs, engine_params, tags):
    """
    Write inputs JSON (and engine_params, if any) to files

    Args:
        family_id (str): Unique family ID for the run
        workflow_inptus (dict): Inputs JSON that will be used to trigger the workflow
        engine_params (dict): Configuration parameters for the engine
        tags (dict): Set of tags to add to the workflow run

    Returns:
        inputs_json_file (str): Path to the inputs JSON file that was written
        engine_params_file (str): Path to the engine parameters file that was written
        tags_file (str): Path to the run tags file
    """
    inputs_json_file = f"{family_id}.inputs.json"
    engine_params_file = f"{family_id}.engine_params.json"
    tags_file = f"{family_id}.run_tags.json"

    print(f"Writing workflow inputs")

    # Write inputs JSON
    if os.path.exists(inputs_json_file):
        with open(inputs_json_file, "r") as f:
            existing_inputs = json.load(f)

        if workflow_inputs == existing_inputs:
            print(
                f"\t✓ Existing identical inputs file found; continuing [{inputs_json_file}]"
            )
        else:
            raise SystemExit(
                f"\t✗ Inputs JSON file [{inputs_json_file}] already exists and has different contents to the current inputs; won't overwrite!\n\tEither delete this file, or use a unique family identifier in the sample information file."
            )
    else:
        with open(inputs_json_file, "w") as f:
            json.dump(workflow_inputs, f, indent=2)
        print(f"\t✓ Wrote inputs to {inputs_json_file}")

    # Write engine params
    with open(engine_params_file, "w") as f:
        json.dump(engine_params, f, indent=2)
    print(f"\t✓ Wrote engine params to {engine_params_file}")

    # Write run tags
    with open(tags_file, "w") as f:
        json.dump(tags, f, indent=2)
    print(f"\t✓ Wrote run tags to {tags_file}")

    return inputs_json_file, engine_params_file, tags_file


def get_tags(workflow_inputs):
    """
    Get tags for a workflow run

    Args:
        workflow_inptus (dict): Inputs JSON that will be used to trigger the workflow

    Returns:
        tags (dict): Set of tags to add to the workflow run
    """
    identifier = (
        workflow_inputs["HumanWGS_wrapper.cohort"]["cohort_id"]
        + "-"
        + "-".join(
            [
                sample["sample_id"]
                for sample in workflow_inputs["HumanWGS_wrapper.cohort"]["samples"]
            ]
        )
    )

    # Note that the same inputs run in different clouds will have different input hashes, because the inputs include the path to the files (cloud-specific)
    inputs_hash = hashlib.md5(
        (json.dumps(workflow_inputs, sort_keys=True)).encode("utf-8")
    ).hexdigest()

    tags = {"identifier": identifier, "inputs_hash": inputs_hash}

    return tags


def print_manual_submission_instructions(
    workflow_inputs,
    workflow_id,
    workflow_version,
    engine,
    engine_params,
    tags,
    inputs_json_file,
    engine_params_file,
    tags_file,
):
    """
    Trigger a run of the workflow via Workbench

    Args:
        workflow_inputs (dict): Inputs JSON that will be used to trigger the workflow
        workflow_id (str): The workflow ID of the workflow registered in Workbench
        workflow_version (str): The version of the workflow to submit
        engine (str): Engine ID to run the workflow through; defaults to the default engine configured in Workbench
        engine_params (dict): Configuration parameters for the engine
        tags (dict): Set of tags to add to the workflow run
        inputs_json_file (str): Path to the inputs JSON file
        engine_params_file (str): Path to the engine parameters file
        tags_file (str): Path to the run tags file
    """
    tags_newline_delimited = "\n\t".join([f"{k}:{v}" for k, v in tags.items()])

    previous_runs = list_previous_runs(tags, workflow_id, workflow_version)

    print()
    print("╔═════════════════════════╗")
    print("║ SUBMITTING THE WORKFLOW ║")
    print("╚═════════════════════════╝")

    if len(previous_runs) > 0:
        print(
            f"[WARN] Found {len(previous_runs)} previous runs (either queued, running, or complete) using this workflow version and these inputs."
        )
        print(
            "Make sure you're certain you want to rerun this sample before running any of the following commands."
        )
        print()

    # CLI submission
    print("┍━━━━━━━━━━━━━┑")
    print("│ Via the CLI │")
    print("┕━━━━━━━━━━━━━┙")
    print(
        "Run the following command from the same directory you ran the current script from:"
    )
    omics_run_cmd = [
        "omics workbench runs submit",
        f"--url {workflow_id}/{workflow_version}",
        f"--workflow-params @{inputs_json_file}",
        f"--tags @{tags_file}",
    ]
    if len(engine_params) > 0:
        omics_run_cmd.append(f"--engine-params @{engine_params_file}")
    if engine:
        omics_run_cmd.append(f"--engine {engine}")

    print()
    print(" \\\n\t".join(omics_run_cmd))
    print()

    # UI submission
    print("┍━━━━━━━━━━━━━┑")
    print("│ Via browser │")
    print("┕━━━━━━━━━━━━━┙")
    omics_browser_instructions = [
        f"Visit https://workbench.omics.ai/workflows/{workflow_id}/run/{workflow_version}",
        "In the Inputs tab, click 'Upload'",
        f"Select the inputs JSON file and press 'Upload'\n\n\tInputs JSON file: {Path(inputs_json_file).resolve()}\n",
    ]
    if engine:
        omics_browser_instructions.append(
            f"In the Engine tab, select Engine '{engine}'"
        )
    if len(engine_params) > 0:
        omics_browser_instructions.append(
            f"In the Engine tab, set Parameters to:\n\n\t{json.dumps(engine_params)}\n"
        )
    omics_browser_instructions.extend(
        [
            "In the top right corner, click 'Submit Run'",
            f"In tags, enter (you can copy and paste the whole block of key:value pairs that follows):\n\n\t{tags_newline_delimited}\n",
            "Click 'Submit'",
        ]
    )

    for index, instruction in enumerate(omics_browser_instructions):
        print(f"{index + 1}. {instruction}")
    print()

    # Script-based submission
    print("┍━━━━━━━━━━━━━━━━━┑")
    print("│ Via this script │")
    print("┕━━━━━━━━━━━━━━━━━┙")
    print(
        "To submit the workflow directly, you can rerun this command without the --upload-only flag, and the workflow will be submitted for you automatically using the above configuration."
    )
    print()


def list_previous_runs(tags, workflow_id, workflow_version):
    """
    Get the list of previous runs using the same set of tags that this input set / workflow version would produce

    Args:
        tags (dict): Set of tags to add to the workflow run
        workflow_id (str): The workflow ID of the workflow registered in Workbench
        workflow_version (str): The version of the workflow to submit

    Returns:
        runs (dict): Set of runs that contains all of the given tags
    """
    run_list = subprocess.run(
        [
            "omics",
            "workbench",
            "runs",
            "list",
            "--state",
            "QUEUED",
            "--state",
            "INITIALIZING",
            "--state",
            "RUNNING",
            "--state",
            "COMPLETE",
            "--tags",
            json.dumps(tags),
            "--search",
            f"{workflow_id}/versions/{workflow_version}",
        ],
        capture_output=True,
        text=True,
    )
    if run_list.returncode == 0:
        try:
            run_list_json = json.loads(run_list.stdout)
        except json.JSONDecodeError as e:
            print(f"\t✗ Error parsing JSON: {e}")
    else:
        raise SystemExit(
            f"\t✗ Something went wrong when listing previous runs\n{run_list.stderr}"
        )

    return run_list_json


def trigger_workflow_run(
    workflow_inputs,
    workflow_id,
    workflow_version,
    engine,
    engine_params,
    tags,
    rerun=False,
):
    """
    Trigger a run of the workflow via Workbench

    Args:
        workflow_inputs (dict): Inputs JSON that will be used to trigger the workflow
        workflow_id (str): The workflow ID of the workflow registered in Workbench
        workflow_version (str): The version of the workflow to submit
        engine (str): Engine ID to run the workflow through; defaults to the default engine configured in Workbench
        engine_params (dict): Configuration parameters for the engine
        tags (dict): Set of tags to add to the workflow run
        rerun (bool): Whether or not to force rerun samples that have already been run
    """
    # Ensure this combination of workflow/version/inputs has not been run successfully before
    previous_runs = list_previous_runs(tags, workflow_id, workflow_version)
    if len(previous_runs) > 0:
        if rerun is False:
            raise SystemExit(
                f"\t✗ Found {len(previous_runs)} previous runs (either queued, running, or complete) using this workflow version and these inputs; not triggering workflow.\n\tTo force a rerun, rerun this command with the --force-rerun flag.\n\nScript execution complete"
            )
        else:
            print(
                "Previous runs found for this workflow version and inputs; rerunning anyway."
            )

    workflow_run_cmd = [
        "omics",
        "workbench",
        "runs",
        "submit",
        "--url",
        f"{workflow_id}/{workflow_version}",
        "--workflow-params",
        json.dumps(workflow_inputs),
        "--tags",
        json.dumps(tags),
    ]
    if len(engine_params) > 0:
        engine_params_string = ",".join([f"{k}={v}" for k, v in engine_params.items()])
        workflow_run_cmd.extend(
            [
                "--engine-params",
                engine_params_string,
            ]
        )

    if engine is not None:
        workflow_run_cmd.extend(["--engine", engine])

    workflow_run = subprocess.run(
        workflow_run_cmd,
        capture_output=True,
        text=True,
    )

    if workflow_run.returncode == 0:
        try:
            workflow_run_json = json.loads(workflow_run.stdout)
            workflow_run_id = workflow_run_json["runs"][0]["run_id"]
            if workflow_run_id is None:
                raise SystemExit(
                    f"\t✗ Something went wrong when submitting the workflow\n{workflow_run_json['runs'][0]['msg']}"
                )
        except json.JSONDecodeError as e:
            print(f"\t✗ Error parsing JSON: {e}")
    else:
        raise SystemExit(
            f"\t✗ Something went wrong when submitting the worklfow\n{workflow_run.stderr}"
        )

    print(f"\t✓ Workflow run submitted; ID [{workflow_run_id}]")
    print()


def main():
    args = parse_args()

    sample_info = load_sample_info(args.sample_info, args.movie_bams, args.fam_info)

    # Import backend-specific functions
    backend_module = import_backend_module(args.backend)

    print("Formatting sample information")
    formatted_sample_info, phenotypes = validate_format_sample_info(sample_info)
    formatted_sample_info.set_index("sample_id", drop=False, inplace=True)
    print("\t✓ Sample information formatted")

    # Bucket configuration
    if args.backend == "AZURE":
        storage_account = args.organization.replace("-", "") + "storage"
        raw_data_bucket = f"{storage_account}/rawdata"
        reference_inputs_bucket = f"{storage_account}/referenceinputs"
        workflow_file_outputs_bucket = f"{storage_account}/workflowfile"
    else:
        organization = args.organization
        raw_data_bucket = f"{organization}-raw-data"
        reference_inputs_bucket = f"{organization}-reference-inputs"
        workflow_file_outputs_bucket = f"{organization}-workflow-file-outputs"

    print("Confirming that the raw data bucket exists, and that you have access to it")
    raw_data_bucket, path_prefix = backend_module.validate_bucket(raw_data_bucket)

    formatted_sample_info_with_paths = upload_files(
        formatted_sample_info,
        backend_module,
        raw_data_bucket,
        args.backend,
        path_prefix,
    )

    container_registry = (
        (f"{AWS_CONTAINER_REGISTRY_ACCOUNT}.dkr.ecr.{args.region}.amazonaws.com")
        if args.backend == "AWS"
        else None
    )

    print("Preparing worfklow inputs")
    workflow_inputs, engine_params = backend_module.generate_inputs_json(
        formatted_sample_info_with_paths,
        phenotypes,
        reference_inputs_bucket,
        workflow_file_outputs_bucket,
        args.region,
        container_registry,
        aws_storage_capacity=args.aws_storage_capacity,
    )

    print("Configuring workbench")
    subprocess.run(["omics", "use", WORKBENCH_URL])
    print("\t✓ Workbench configured")

    print(
        f"Registering or retrieving the workflow from Workbench ([{WORKFLOW_NAME}:{DERIVED_WORKFLOW_VERSION}])"
    )
    workflow_id = get_workflow_id(WORKFLOW_NAME, DERIVED_WORKFLOW_VERSION)

    run_tags = get_tags(workflow_inputs)

    if args.write_inputs_json:
        family_id = sample_info["family_id"].unique()[0].replace(" ", "_")
        inputs_json_file, engine_params_file, run_tags_file = write_inputs_json(
            family_id, workflow_inputs, engine_params, run_tags
        )

    if args.upload_only:
        print_manual_submission_instructions(
            workflow_inputs,
            workflow_id,
            DERIVED_WORKFLOW_VERSION,
            args.engine,
            engine_params,
            run_tags,
            inputs_json_file,
            engine_params_file,
            run_tags_file,
        )
    else:
        print("Triggering workflow run")
        trigger_workflow_run(
            workflow_inputs,
            workflow_id,
            DERIVED_WORKFLOW_VERSION,
            args.engine,
            engine_params,
            run_tags,
            args.force_rerun,
        )

    print("╔═════════════════════════╗")
    print("║ MONITORING THE WORKFLOW ║")
    print("╚═════════════════════════╝")
    print(
        "To monitor the workflow run, please visit https://workbench.omics.ai/monitor"
    )
    print()
    print("Script execution complete")


if __name__ == "__main__":
    main()
