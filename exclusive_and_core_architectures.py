#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
import sys
from PfamLocalDatabase import Database, DatabaseError

"""
Core architectures by phylum.
Generate a tab-delimited file with domain architectures exclusive to a single phylum
 and represented in each species of the phylum (high evolutionary conservation).

Tab-separate file columns:
    - phylum.
    - architecture. Pfam domain names (i.e 'AhpC-TSA~1-cysPrx_C') separated by '~'
    - architecture_acc. Pfam domain accessions (i.e. 'PF00578 PF10417') separated by ' '

@:param db_user
@:param db_password
@:param db_user


Author: Alejandro Barrera
email: aebmad@gmail.com

"""
__author__ = 'abarrera'

TAXONOMY_TYPES = ['phylum', 'subphylum', 'order', 'genus', 'species', 'strains']
LEAF_CORE_TAXA_TYPE = 'strains'


def generateArchitectureDataStructure(db):
    """
    Create a dictionary with domain architectures exclusive in a single pathogen type group.
    :param db: database object
    :return: dictionary
        key: tuple (architecture_acc, architecture)
        value: list of pathogen_type
            (it might contain duplicates, but all values are equal => convert to set)
    """
    architectures = defaultdict(lambda: defaultdict(list))

    for row in db.getArchitecturesIterator():
        for tax_name in TAXONOMY_TYPES:
            architectures[(row['architecture'], row['architecture_acc'])][tax_name].append(row[tax_name])
    return architectures


def getTaxonomyCounts(db):
    taxonomy_counts = defaultdict(int)
    for row in db.getTaxonomyIterator():
        for tax_name in TAXONOMY_TYPES:
            taxonomy_counts[row[tax_name]] += 1
    return taxonomy_counts


def main():
    try:
        db = Database()
        architectures = generateArchitectureDataStructure(db)
        taxonomy_counts = getTaxonomyCounts(db)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    # Architectures exclusive by phylum
    print("architecture_ids", "architectures_acc", sep="\t", end="\t")
    for taxon_index in range(len(TAXONOMY_TYPES) - 1):
        print(TAXONOMY_TYPES[taxon_index], "core", sep="\t", end="\t")
    print()

    for architecture in architectures:
        print(architecture[0], architecture[1], sep="\t", end="\t")
        for taxa_index in range(len(TAXONOMY_TYPES) - 1):
            if len(set(architectures[architecture][TAXONOMY_TYPES[taxa_index]])) == 1:
                print(architectures[architecture][TAXONOMY_TYPES[taxa_index]][0], sep="\t", end="\t")
                # Core?
                num_sub_taxa = len(set(architectures[architecture][LEAF_CORE_TAXA_TYPE]))
                max_aux = taxonomy_counts[architectures[architecture][TAXONOMY_TYPES[taxa_index]][0]]
                if num_sub_taxa == max_aux:
                    print(1, sep="\t", end="\t")
                else:
                    print(0, sep="\t", end="\t")
            else:
                print(0, 0, sep="\t", end="\t")
        print()

    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)