WORKBENCH_URL = "workbench.omics.ai"
WORKFLOW_NAME = "HiFi_Solves_HumanWGS"
WORKFLOW_VERSION = "v1.1.0"
WORKFLOW_SUB_VERSION = "v1.0.4"
DERIVED_WORKFLOW_VERSION = f"{WORKFLOW_VERSION}_{WORKFLOW_SUB_VERSION}"

# AWS account where containers are hosted
AWS_CONTAINER_REGISTRY_ACCOUNT = "635186400088"


def get_reference_data(reference_inputs_bucket):
    """
    Return a reference_data, slivar_data objects with paths updated to the given reference_inputs_bucket

    Args:
        reference_inputs_bucket (str): Bucket where reference data has been uploaded

    Returns:
        reference_data (dict): Reference data object with paths filled out
        slivar_data (dict): Slivar-associated data object with paths filled out
    """
    reference_data = {
        "name": "GRCh38",
        "fasta": {
            "data": f"{reference_inputs_bucket}/dataset/GRCh38/human_GRCh38_no_alt_analysis_set.fasta",
            "data_index": f"{reference_inputs_bucket}/dataset/GRCh38/human_GRCh38_no_alt_analysis_set.fasta.fai",
        },
        "pbsv_splits": f"{reference_inputs_bucket}/dataset/GRCh38/human_GRCh38_no_alt_analysis_set.pbsv_splits.json",
        "tandem_repeat_bed": f"{reference_inputs_bucket}/dataset/GRCh38/human_GRCh38_no_alt_analysis_set.trf.bed",
        "trgt_tandem_repeat_bed": f"{reference_inputs_bucket}/dataset/GRCh38/trgt/human_GRCh38_no_alt_analysis_set.trgt.v0.3.4.bed",
        "hificnv_exclude_bed": {
            "data": f"{reference_inputs_bucket}/dataset/GRCh38/hificnv/cnv.excluded_regions.common_50.hg38.bed.gz",
            "data_index": f"{reference_inputs_bucket}/dataset/GRCh38/hificnv/cnv.excluded_regions.common_50.hg38.bed.gz.tbi",
        },
        "hificnv_expected_bed_male": f"{reference_inputs_bucket}/dataset/GRCh38/hificnv/expected_cn.hg38.XY.bed",
        "hificnv_expected_bed_female": f"{reference_inputs_bucket}/dataset/GRCh38/hificnv/expected_cn.hg38.XX.bed",
        "gnomad_af": f"{reference_inputs_bucket}/dataset/GRCh38/slivar_gnotate/gnomad.hg38.v3.custom.v1.zip",
        "hprc_af": f"{reference_inputs_bucket}/dataset/GRCh38/slivar_gnotate/hprc.deepvariant.glnexus.hg38.v1.zip",
        "gff": f"{reference_inputs_bucket}/dataset/GRCh38/ensembl.GRCh38.101.reformatted.gff3.gz",
        "population_vcfs": [
            {
                "data": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/EEE_SV-Pop_1.ALL.sites.20181204.vcf.gz",
                "data_index": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/EEE_SV-Pop_1.ALL.sites.20181204.vcf.gz.tbi",
            },
            {
                "data": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/nstd166.GRCh38.variant_call.vcf.gz",
                "data_index": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/nstd166.GRCh38.variant_call.vcf.gz.tbi",
            },
            {
                "data": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/hprc.GRCh38.pbsv.vcf.gz",
                "data_index": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/hprc.GRCh38.pbsv.vcf.gz.tbi",
            },
            {
                "data": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/ont_sv_high_confidence_SVs.sorted.vcf.gz",
                "data_index": f"{reference_inputs_bucket}/dataset/GRCh38/sv_pop_vcfs/ont_sv_high_confidence_SVs.sorted.vcf.gz.tbi",
            },
        ],
    }

    slivar_data = {
        "slivar_js": f"{reference_inputs_bucket}/dataset/slivar/slivar-functions.v0.2.8.js",
        "hpo_terms": f"{reference_inputs_bucket}/dataset/hpo/hpoTerms.txt",
        "hpo_dag": f"{reference_inputs_bucket}/dataset/hpo/hpoDag.txt",
        "hpo_annotations": f"{reference_inputs_bucket}/dataset/hpo/ensembl.hpoPhenotype.tsv",
        "ensembl_to_hgnc": f"{reference_inputs_bucket}/dataset/genes/ensembl.hgncSymbol.tsv",
        "lof_lookup": f"{reference_inputs_bucket}/dataset/slivar/lof_lookup.v2.1.1.txt",
        "clinvar_lookup": f"{reference_inputs_bucket}/dataset/slivar/clinvar_gene_desc.20221214T183140.txt",
    }

    return reference_data, slivar_data
