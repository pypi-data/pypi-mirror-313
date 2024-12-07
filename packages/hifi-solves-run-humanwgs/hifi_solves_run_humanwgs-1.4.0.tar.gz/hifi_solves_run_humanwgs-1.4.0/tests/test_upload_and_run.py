#!/usr/bin/env python3

import unittest
from hifi_solves_run_humanwgs.upload_and_run import validate_format_sample_info

import pandas as pd


class TestValidateFormatSampleInfo(unittest.TestCase):
    def test_missing_required_family_id_column(self):
        sample_info = pd.DataFrame(
            {
                "sample_id": ["HG002", "HG003", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG003.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Missing required columns: family_id" == str(context.exception)
        )

    def test_missing_required_sample_id_column(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "movie_bams": ["_HG002.bam", "_HG003.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Missing required columns: sample_id" == str(context.exception)
        )

    def test_missing_required_movie_bams_column(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG003", "HG004"],
                "phenotypes": ["HP:0000001", None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Missing required columns: movie_bams" == str(context.exception)
        )

    def test_missing_multiple_required_columns(self):
        sample_info = pd.DataFrame(
            {
                "sample_id": ["HG002", "HG003", "HG004"],
                "phenotypes": ["HP:0000001", None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Missing required columns: family_id, movie_bams"
            == str(context.exception)
        )

    def test_invalid_sex(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG002", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG002_2.bam", "_HG004.bam"],
                "sex": ["Male", None, "fem"],
            }
        )
        with self.assertRaisesRegex(KeyError, "Invalid sex"):
            validate_format_sample_info(sample_info)

    def test_one_unique_value_of_mother_id(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG002", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG002_2.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
                "mother_id": ["HG001", "HG003", None],
            }
        )
        with self.assertRaisesRegex(
            ValueError,
            "There should be exactly one unique value of mother_id for each combination of family_id, sample_id",
        ) as context:
            validate_format_sample_info(sample_info)

    def test_one_unique_value_of_father_id(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG002", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG002_2.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
                "father_id": ["HG001", "HG003", None],
            }
        )
        with self.assertRaisesRegex(
            ValueError,
            "There should be exactly one unique value of father_id for each combination of family_id, sample_id",
        ) as context:
            validate_format_sample_info(sample_info)

    def test_one_unique_value_of_sex(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG002", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG002_2.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
                "sex": ["Male", "Female", None],
            }
        )
        with self.assertRaisesRegex(
            ValueError,
            "There should be exactly one unique value of sex for each combination of family_id, sample_id",
        ) as context:
            validate_format_sample_info(sample_info)

    def test_no_phenotype_set_singleton(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort"],
                "sample_id": ["HG002"],
                "movie_bams": ["_HG002.bam"],
                "phenotypes": [None],
                "father_id": [None],
            }
        )
        _, phenotypes = validate_format_sample_info(sample_info)
        self.assertEqual(phenotypes, ["HP:0000001"])

    def test_set_default_phenotype(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG003", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG003.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
                "father_id": ["HG002", None, None],
            }
        )
        formatted_sample_info, phenotypes = validate_format_sample_info(sample_info)
        affected_sample_ids = formatted_sample_info[
            formatted_sample_info["affected"] == 1
        ].sample_id
        self.assertEqual(len(affected_sample_ids), 1)
        self.assertEqual(affected_sample_ids[0], "HG002")
        self.assertEqual(phenotypes, ["HP:0000001"])

    def test_proband_unclear_phenotype_unset(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG003", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG003.bam", "_HG004.bam"],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Must define at least one phenotype for the proband. If no particular phenotypes are desired, the root HPO term, 'HP:0000001', can be used."
            == str(context.exception)
        )

    def test_invalid_hpo_terms(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG003", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG003.bam", "_HG004.bam"],
                "phenotypes": ["HP_0000001", None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Invalid HPO term(s) found: {'HP_0000001'}\nHPO terms should be of the form HP:xxxxxxx, where x is a digit 0-9. See [the Human Phenotype Ontology](https://hpo.jax.org/app/) for more information."
            == str(context.exception)
        )

    def test_different_phenotypes_sets(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG003", "HG004"],
                "movie_bams": ["_HG002.bam", "_HG003.bam", "_HG004.bam"],
                "phenotypes": ["HP:0000001", "HP:0000002", None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ There should be exactly one unique set of phenotypes across all samples; found [('HP:0000001',) ('HP:0000002',)]"
            == str(context.exception)
        )

    def test_no_missing_values_in_required_columns(self):
        sample_info = pd.DataFrame(
            {
                "family_id": ["HG002_cohort", "HG002_cohort", "HG002_cohort"],
                "sample_id": ["HG002", "HG003", "HG004"],
                "movie_bams": ["_HG002.bam", None, "_HG004.bam"],
                "phenotypes": ["HP:0000001", None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Missing values found in required columns: movie_bams"
            == str(context.exception)
        )

    def test_no_duplicate_movie_bams_in_different_samples(self):
        sample_info = pd.DataFrame(
            {
                "family_id": [
                    "HG002_cohort",
                    "HG002_cohort",
                    "HG002_cohort",
                    "HG002_cohort",
                ],
                "sample_id": ["HG002", "HG003", "HG004", "HG004"],
                "movie_bams": [
                    "_HG002.bam",
                    "_HG003.bam",
                    "_HG003.bam",
                    "_HG004.bam",
                ],
                "phenotypes": ["HP:0000001", None, None, None],
            }
        )
        with self.assertRaises(ValueError) as context:
            validate_format_sample_info(sample_info)
        self.assertTrue(
            "\t✗ Duplicate movie bams found: _HG003.bam" == str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
