#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
import sys
import operator
from PfamLocalDatabase import Database, DatabaseError

"""
Domain architectures exclusive by pathogen type, present only in species
belonging to the same pathogen type

Generates a tab-separate file with columns:
    - pathogen_type. Possible values:
        4: Over 100 strains in two epidemiologic studies in Spain (FILPOP and CANDIPOP).
        3: Over 50strains in Candipop or 20 strains in FILPOP, or very frequent worldwide (www.life-worldwide.org).
        2: Isolated in Candipop, Filpop or frequent dermatophytes.
        1: Strains present in our collection of clinical isolates (all coming from hospitals)
        0: Not defined criteria.
    - architecture. Pfam domain names (i.e 'AhpC-TSA~1-cysPrx_C') separated by '~'
    - architecture_acc. Pfam domain accessions (i.e. 'PF00578 PF10417') separated by ' '

@:param db_user
@:param db_password
@:param db_user


Author: Alejandro Barrera
email: aebmad@gmail.com

"""
__author__ = 'abarrera'


def generateArchitectureDataStructure(db):
    """
    Create a dictionary with domain architectures exclusive in a single pathogen type group.
    :param db: database object
    :return: dictionary
        key: tuple (architecture_acc, architecture)
        value: list of pathogen_type
            (it might contain duplicates, but all values are equal => convert to set)
    """
    architecture_pathogen_dict = defaultdict(list)
    for row in db.getArchitecturePathogenTypeIterator():
        species = row['species']
        protein = row['accession']
        pathogen_type = row['pathogen_type']
        architecture = row['architecture']
        architecture_acc = row['architecture_acc']

        architecture_pathogen_dict[(architecture, architecture_acc)].append(pathogen_type)

    for architecture_iter, architecture_acc_iter in architecture_pathogen_dict.keys():
        # ???   If an architecture is only present in proteins of a certain pathogen_type,
        #       it should have only has 1 pathogen_type
        if len(set(architecture_pathogen_dict[(architecture_iter, architecture_acc_iter)])) != 1:
            architecture_pathogen_dict.pop((architecture_iter, architecture_acc_iter), None)
    return architecture_pathogen_dict


def main():
    try:
        db = Database()
        architectures = generateArchitectureDataStructure(db)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    print("pathogen_type\tarchitecture_name\tarchitecture_acc")
    for architecture_descriptors, pathogen_type_list in sorted(architectures.iteritems(),
                                                               key=operator.itemgetter(1, 0)):
        architecture, architecture_acc = architecture_descriptors
        pathogen_type = pathogen_type_list[0]
        print(pathogen_type, architecture, architecture_acc, sep="\t")
    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)