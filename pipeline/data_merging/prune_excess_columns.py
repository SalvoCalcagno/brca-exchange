#!/usr/bin/env python
"""
checks that all reports are accounted for in final pipeline output
"""
import argparse
import os
import pandas as pd
from workflow import pipeline_utils

BRCA_ONLY_FIELDS = ["mupit_structure",
                    "Pathogenicity_expert",
                    "Genomic_Coordinate_hg37",
                    "Max_Allele_Frequency",
                    "Protein_Change",
                    "HGVS_Protein",
                    "HGVS_cDNA",
                    "BIC_Nomenclature",
                    "Hg37_Start",
                    "Hg37_End",
                    "HGVS_RNA",
                    "URL_ENIGMA",
                    "Condition_ID_type_ENIGMA",
                    "Condition_ID_value_ENIGMA",
                    "Condition_category_ENIGMA",
                    "Clinical_significance_ENIGMA",
                    "Date_last_evaluated_ENIGMA",
                    "Assertion_method_ENIGMA",
                    "Assertion_method_citation_ENIGMA",
                    "Clinical_significance_citations_ENIGMA",
                    "Comment_on_clinical_significance_ENIGMA",
                    "Collection_method_ENIGMA",
                    "Allele_origin_ENIGMA",
                    "ClinVarAccession_ENIGMA",
                    "BX_ID_ENIGMA"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="input file to remove columns from")
    parser.add_argument("-o", "--output",
                        help="output file with removed columns")
    parser.add_argument("c", "--config", help='configuration file to inform script')

    args = parser.parse_args()

    configure_logging()

    gene_config_df = config.load_config(args.config)

    gene_symbols = pipeline_utils.concatenate_symbols(gene_config_df['symbol'])

    pruned_df = prune_columns(pd.read_csv(args.input, sep='\t'), gene_symbols)

    pruned_df.to_csv(args.output, sep='\t', index=False)


def prune_columns(df, gene_symbols):
    if "BRCA1" not in gene_symbols and "BRCA2" not in gene_symbols:
        return df.drop(BRCA_ONLY_FIELDS, axis=1)
    return df


if __name__ == "__main__":
    main()
