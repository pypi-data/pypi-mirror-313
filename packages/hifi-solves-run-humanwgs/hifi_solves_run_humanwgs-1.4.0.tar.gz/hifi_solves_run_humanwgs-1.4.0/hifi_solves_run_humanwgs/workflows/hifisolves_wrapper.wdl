version 1.0

import "HiFi-human-WGS-WDL/workflows/wdl-common/wdl/workflows/backend_configuration/backend_configuration.wdl" as BackendConfiguration
import "HiFi-human-WGS-WDL/workflows/main.wdl" as main

workflow HumanWGS_wrapper {
    input {
        Cohort cohort

        ReferenceData reference
        SlivarData? slivar_data

        String deepvariant_version = "1.5.0"
        DeepVariantModel? deepvariant_model

        Int? pbsv_call_mem_gb
        Int? glnexus_mem_gb
        Boolean run_tertiary_analysis = false

        # Backend configuration
        String backend
        String? zones
        String? aws_spot_queue_arn
        String? aws_on_demand_queue_arn
        String? container_registry
        Boolean preemptible

        # Wrapper workflow inputs
        String workflow_outputs_bucket
    }

    String workflow_name = "HumanWGS"
    String workflow_version = "v1.1.0"

    call BackendConfiguration.backend_configuration {
        input:
            backend = backend,
            zones = zones,
            aws_spot_queue_arn = aws_spot_queue_arn,
            aws_on_demand_queue_arn = aws_on_demand_queue_arn,
            container_registry = container_registry
    }

    RuntimeAttributes default_runtime_attributes = if preemptible then backend_configuration.spot_runtime_attributes else backend_configuration.on_demand_runtime_attributes

    String create_timestamp_docker_image = (if (backend == "AWS") then default_runtime_attributes.container_registry + "/" else "") + "ubuntu:jammy"
    String upload_outputs_docker_image = (if (backend == "AWS") then default_runtime_attributes.container_registry + "/" else "dnastack/") + "hifi_solves_tools:1.4.0"

    call main.humanwgs as humanwgs {
        input:
            cohort = cohort,
            reference = reference,
            slivar_data = slivar_data,
            deepvariant_model = deepvariant_model,
            pbsv_call_mem_gb = pbsv_call_mem_gb,
            glnexus_mem_gb = glnexus_mem_gb,
            run_tertiary_analysis = run_tertiary_analysis,
            deepvariant_version = deepvariant_version,
            backend = backend,
            zones = zones,
            aws_spot_queue_arn = aws_spot_queue_arn,
            aws_on_demand_queue_arn = aws_on_demand_queue_arn,
            container_registry = container_registry,
            preemptible = preemptible
    }

    # Gather workflow output files
    ## IndexData
    scatter (small_variant_gvcf in humanwgs.small_variant_gvcfs) {
        File small_variant_gvcf_data = small_variant_gvcf.data
        File small_variant_gvcf_data_index = small_variant_gvcf.data_index
    }

    scatter (sample_phased_small_variant_vcf in humanwgs.sample_phased_small_variant_vcfs) {
        File sample_phased_small_vcf_data = sample_phased_small_variant_vcf.data
        File sample_phased_small_vcf_data_index = sample_phased_small_variant_vcf.data_index
    }

    scatter (sample_phased_sv_vcfs in humanwgs.sample_phased_sv_vcfs) {
        File sample_phased_sv_data = sample_phased_sv_vcfs.data
        File sample_phased_sv_data_index = sample_phased_sv_vcfs.data_index
    }

    scatter (merged_haplotagged_bam in humanwgs.merged_haplotagged_bam) {
        File mhb_data = merged_haplotagged_bam.data
        File mhb_data_index = merged_haplotagged_bam.data_index
    }

    scatter (trgt_spanning_reads in humanwgs.trgt_spanning_reads) {
        File trgt_reads_data = trgt_spanning_reads.data
        File trgt_reads_data_index = trgt_spanning_reads.data_index
    }

    scatter (trgt_repeat_vcf in humanwgs.trgt_repeat_vcf) {
        File trgt_vcf_data = trgt_repeat_vcf.data
        File trgt_vcf_data_index = trgt_repeat_vcf.data_index
    }


    scatter (paraphase_realigned_bam in humanwgs.paraphase_realigned_bams) {
        File prb_data = paraphase_realigned_bam.data
        File prb_data_index = paraphase_realigned_bam.data_index
    }

    scatter (hificnv_vcf in humanwgs.hificnv_vcfs) {
        File hificnv_vcf_data = hificnv_vcf.data
        File hificnv_vcf_data_index = hificnv_vcf.data_index
    }

    ## IndexData?
    if (defined(humanwgs.cohort_sv_vcf)) {
        IndexData phased_joint_sv_vcf_struct = select_first([humanwgs.cohort_sv_vcf])

        File cohort_sv_vcf_data = phased_joint_sv_vcf_struct.data
        File cohort_sv_vcf_data_index = phased_joint_sv_vcf_struct.data_index
    }

    if (defined(humanwgs.cohort_small_variant_vcf)) {
        IndexData phased_joint_small_variant_vcf_struct = select_first([humanwgs.cohort_small_variant_vcf])

        File cohort_small_variant_vcf_data = phased_joint_small_variant_vcf_struct.data
        File cohort_small_variant_vcf_data_index = phased_joint_small_variant_vcf_struct.data_index
    }

    if (defined(humanwgs.filtered_small_variant_vcf)) {
        IndexData filtered_small_variant_vcf_struct = select_first([humanwgs.filtered_small_variant_vcf])

        File filtered_small_variant_vcf_data = filtered_small_variant_vcf_struct.data
        File filtered_small_variant_vcf_data_index = filtered_small_variant_vcf_struct.data_index
    }

    if (defined(humanwgs.compound_het_small_variant_vcf)) {
        IndexData compound_het_small_variant_vcf_struct = select_first([humanwgs.compound_het_small_variant_vcf])

        File compound_het_small_variant_vcf_data = compound_het_small_variant_vcf_struct.data
        File compound_het_small_variant_vcf_data_index = compound_het_small_variant_vcf_struct.data_index
    }

    if (defined(humanwgs.filtered_svpack_vcf)) {
        IndexData filtered_svpack_vcf_struct = select_first([humanwgs.filtered_svpack_vcf])

        File filtered_svpack_vcf_data = filtered_svpack_vcf_struct.data
        File filtered_svpack_vcf_data_index = filtered_svpack_vcf_struct.data_index
    }

    # Create array of workflow output names and their corresponding outputs
    # Each workflow_output_name is at the same index as the corresponding array of workflow_output_files
    Array[String] workflow_output_names = [
        # sample_analysis output
        "bam_stats",
        "small_variant_gvcfs",
        "small_variant_vcf_stats",
        "small_variant_roh_out",
        "small_variant_roh_bed",
        "sample_phased_small_variant_vcfs",
        "sample_phased_sv_vcfs",
        "hiphase_stats",
        "hiphase_blocks",
        "hiphase_haplotags",
        "merged_haplotagged_bam",
        "haplotagged_bam_mosdepth_summary",
        "haplotagged_bam_mosdepth_region_bed",
        "trgt_spanning_reads",
        "trgt_repeat_vcf",
        "trgt_dropouts",
        "cpg_pileup_beds",
        "cpg_pileup_bigwigs",
        "paraphase_output_jsons",
        "paraphase_realigned_bams",
        "paraphase_vcfs",
        "hificnv_vcfs",
        "hificnv_copynum_bedgraphs",
        "hificnv_depth_bws",
        "hificnv_maf_bws",

        # cohort_analysis output
        "cohort_sv_vcf",
        "cohort_small_variant_vcf",
        "cohort_hiphase_stats",
        "cohort_hiphase_blocks",

        # tertiary_analysis output
        "filtered_small_variant_vcf",
        "compound_het_small_variant_vcf",
        "filtered_svpack_vcf",
        "filtered_small_variant_tsv",
        "compound_het_small_variant_tsv",
        "filtered_svpack_tsv"
    ]

    Array[Array[File]] workflow_output_files = [
        # sample_analysis output
        flatten(humanwgs.bam_stats),
        flatten([small_variant_gvcf_data, small_variant_gvcf_data_index]),
        humanwgs.small_variant_vcf_stats,
        humanwgs.small_variant_roh_out,
        humanwgs.small_variant_roh_bed,
        flatten([sample_phased_small_vcf_data, sample_phased_small_vcf_data_index]),
        flatten([sample_phased_sv_data, sample_phased_sv_data_index]),
        humanwgs.sample_hiphase_stats,
        humanwgs.sample_hiphase_blocks,
        humanwgs.sample_hiphase_haplotags,
        flatten([mhb_data, mhb_data_index]),
        humanwgs.haplotagged_bam_mosdepth_summary,
        humanwgs.haplotagged_bam_mosdepth_region_bed,
        flatten([trgt_reads_data, trgt_reads_data_index]),
        flatten([trgt_vcf_data, trgt_vcf_data_index]),
        humanwgs.trgt_dropouts,
        flatten(humanwgs.cpg_pileup_beds),
        flatten(humanwgs.cpg_pileup_bigwigs),
        humanwgs.paraphase_output_jsons,
        flatten([prb_data, prb_data_index]),
        flatten(humanwgs.paraphase_vcfs),
        flatten([hificnv_vcf_data, hificnv_vcf_data_index]),
        humanwgs.hificnv_copynum_bedgraphs,
        humanwgs.hificnv_depth_bws,
        humanwgs.hificnv_maf_bws,

        # cohort_analysis output
        select_all([cohort_sv_vcf_data, cohort_sv_vcf_data_index]),
        select_all([cohort_small_variant_vcf_data, cohort_small_variant_vcf_data_index]),
        select_all([humanwgs.cohort_hiphase_stats]),
        select_all([humanwgs.cohort_hiphase_blocks]),

        #tertiary_analysis output
        select_all([filtered_small_variant_vcf_data, filtered_small_variant_vcf_data_index]),
        select_all([compound_het_small_variant_vcf_data, compound_het_small_variant_vcf_data_index]),
        select_all([filtered_svpack_vcf_data, filtered_svpack_vcf_data_index]),
        select_all([humanwgs.filtered_small_variant_tsv]),
        select_all([humanwgs.compound_het_small_variant_tsv]),
        select_all([humanwgs.filtered_svpack_tsv])
    ]

    call create_timestamp {
        input:
            workflow_output_files = workflow_output_files, # !StringCoercion,
            create_timestamp_docker_image = create_timestamp_docker_image,
            runtime_attributes = default_runtime_attributes
    }

    call organize_outputs_and_write_to_bucket as organize_and_write_workflow_outputs {
        input:
            output_names = workflow_output_names,
            output_files = workflow_output_files, # !StringCoercion
            output_type = "workflow",
            backend = backend,
            identifier = cohort.cohort_id,
            timestamp = create_timestamp.timestamp,
            workflow_version = workflow_version,
            workflow_name = workflow_name,
            output_bucket = workflow_outputs_bucket,
            upload_outputs_docker_image = upload_outputs_docker_image,
            runtime_attributes = default_runtime_attributes
    }

   output {
        # Workflow outputs
        File workflow_output_json = organize_and_write_workflow_outputs.output_json
        File workflow_output_manifest_tsv = organize_and_write_workflow_outputs.output_manifest_tsv
    }

    parameter_meta {
        workflow_outputs_bucket: {help: "Path to the bucket where the workflow outputs will be stored"}
    }
}

task create_timestamp {
    input {
        Array[Array[String]] workflow_output_files
        String create_timestamp_docker_image

        RuntimeAttributes runtime_attributes
    }

    command <<<
        set -euo pipefail

        date +%s > timestamp.txt

        echo -e "Created timestamp for outputs\n~{sep='\n' flatten(workflow_output_files)}"
    >>>

    output {
        String timestamp = read_string("timestamp.txt")
    }

    runtime {
        docker: create_timestamp_docker_image
        cpu: 2
        memory: "4 GB"
        disk: "15 GB"
        disks: "local-disk 15 HDD"
        preemptible: runtime_attributes.preemptible_tries
        maxRetries: runtime_attributes.max_retries
        awsBatchRetryAttempts: runtime_attributes.max_retries
        queueArn: runtime_attributes.queue_arn
        zones: runtime_attributes.zones
    }
}

task organize_outputs_and_write_to_bucket {
    input {
        Array[String] output_names
        Array[Array[String]] output_files
        String output_type
        String backend
        String identifier
        String timestamp
        String workflow_version
        String workflow_name
        String output_bucket
        String upload_outputs_docker_image

        RuntimeAttributes runtime_attributes
    }

    command <<<
        set -euo pipefail

        cp ~{write_lines(output_names)} output_names.txt
        cp ~{write_tsv(output_files)} output_files.tsv

        files_to_json.py \
            -n output_names.txt \
            -f output_files.tsv \
            -j ~{identifier}.~{output_type}_outputs.json

        upload_outputs.sh \
            -b ~{backend} \
            -i ~{identifier} \
            -t ~{timestamp} \
            -w ~{workflow_name} \
            -v ~{workflow_version} \
            -o ~{output_bucket} \
            -j ~{identifier}.~{output_type}_outputs.json \
            -m ~{identifier}.~{output_type}_outputs.manifest.tsv
    >>>

    output {
        File output_json = "~{identifier}.~{output_type}_outputs.json"
        File output_manifest_tsv = "~{identifier}.~{output_type}_outputs.manifest.tsv"
    }

    runtime {
        docker: upload_outputs_docker_image
        cpu: 2
        memory: "4 GB"
        disk: "50 GB"
        disks: "local-disk 50 HDD"
        bootDiskSizeGb: 20
        preemptible: runtime_attributes.preemptible_tries
        maxRetries: runtime_attributes.max_retries
        awsBatchRetryAttempts: runtime_attributes.max_retries
        queueArn: runtime_attributes.queue_arn
        zones: runtime_attributes.zones
    }
}