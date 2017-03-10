#!/usr/bin/env python
"""
checks that all bx_ids are accounted for
"""
import argparse
import csv
import logging
from os import listdir
from os.path import isfile, join, abspath
import vcf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--built",
                        help="built.tsv with all variants")
    parser.add_argument("-o", "--ready_input_dir",
                        help="file directory with all procesed files with bx_ids used to compile built.tsv")
    parser.add_argument('-a', "--artifacts_dir", help='Artifacts directory with pipeline artifact files.')
    parser.add_argument("-v", "--verbose", action="count", default=True, help="determines logging")

    args = parser.parse_args()

    if args.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.CRITICAL

    log_file_path = args.artifacts_dir + "missing_reports.log"
    logging.basicConfig(filename=log_file_path, filemode="w", level=logging_level)

    bx_ids = {}

    files = [f for f in listdir(args.ready_input_dir) if isfile(join(args.ready_input_dir, f)) and "ready" in f or "ENIGMA_combined_with_bx_ids" in f]

    # Get all bx_ids present in source files organized by source
    for file in files:
        file_path = abspath(args.ready_input_dir + file)
        if file_path.endswith('.tsv'):
            source = "ENIGMA"
            bx_ids[source] = []
            tsv_file = csv.DictReader(open(file_path, "r"), delimiter='\t')
            for report in tsv_file:
                ids = map(int, report['BX_ID'].split(','))
                bx_ids[source] = bx_ids[source] + ids
        else:
            suffix = 'ready.vcf'
            source = file[:(len(file)-len(suffix))]
            bx_ids[source] = []
            vcf_reader = vcf.Reader(open(file_path, 'r'), strict_whitespace=True)
            try:
                for record in vcf_reader:
                    ids = map(int, record.INFO['BX_ID'])
                    bx_ids[source] = bx_ids[source] + ids
            except ValueError as e:
                print e

    built = csv.DictReader(open(args.built, "r"), delimiter='\t')
    column_prefix = "BX_ID_"
    bx_id_columns = [f for f in built.fieldnames if column_prefix in f]
    matches_per_source = {}
    for variant in built:
        for column in bx_id_columns:
            source = column[len(column_prefix):]
            if source not in matches_per_source:
                matches_per_source[source] = []
            source_bx_ids = variant[column]
            variant_sources = variant["Source"].split(',')
            match = False
            for src in variant_sources:
                if source == src:
                    match = True
            if isEmpty(source_bx_ids):
                if match:
                    logging.warning("Variant %s has source %s but no report ids from that source", variant, source)
            else:
                if not match:
                    logging.warning("Variant %s has report(s) %s from source %s, but source is not associated with variant", variant, source_bx_ids, source)
                else:
                    source_bx_ids = map(int, source_bx_ids.split(','))
                    for source_bx_id in source_bx_ids:
                        if source_bx_id in bx_ids[source]:
                            matches_per_source[source].append(source_bx_id)
                        else:
                            logging.warning("Report(s) %s found on variant %s, but report does not exist from source %s", source_bx_ids, variant, source)

    missing_reports = {}
    for source in matches_per_source:
        matches = sorted(matches_per_source[source])
        matches_set = set(matches)
        if len(matches) != len(matches_set):
            print "Error with matches"
        original_ids = sorted(bx_ids[source])
        original_ids_set = set(original_ids)
        if len(original_ids) != len(original_ids_set):
            print "Error with original ids"
        missing_reports[source] = matches_set.symmetric_difference(original_ids_set)

    logging.debug("Reports absent from release: %s", missing_reports)


def isEmpty(value):
    return value == '-' or value is None


if __name__ == "__main__":
    main()
