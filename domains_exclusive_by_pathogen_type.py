#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
import sys
import operator
from PfamLocalDatabase import Database, DatabaseError

"""

Domain exclusive by pathogen type.

Generates a tab-separate file with columns:
    - pathogen_type. Possible values:
        4: Over 100 strains in two epidemiologic studies in Spain (FILPOP and CANDIPOP).
        3: Over 50 strains in Candipop or 20 strains in FILPOP, or very frequent worldwide (www.life-worldwide.org).
        2: Isolated in Candipop, Filpop or frequent dermatophytes.
        1: Strains present in our collection of clinical isolates (all coming from hospitals)
        0: Not defined criteria.
    - Pfam domain name i.e 'AhpC-TSA')
    - Pfam domain accession (i.e. 'PF00578')
    - Domain description.

@:param db_user
@:param db_password
@:param db_user


Author: Alejandro Barrera
email: aebmad@gmail.com

"""
__author__ = 'abarrera'


def generateDomainsDataStructure(db):
    """
    Create a dictionary with pfam domains exclusive in a single pathogen type group
    :param db: database object
    :return:
        - *dictionary* with key:pfam_acc, value:list of pathogen_type
            (it might contain duplicates, but all values are equal => convert to set)
        - *dictionary* with pfam domain info to output (pfam_acc, pfam_id, description)
    """
    pfam_pathogen_dict = defaultdict(list)
    pfam_dict = defaultdict()
    for row in db.getDomainsPathogenTypeIterator():
        species = row['species']
        protein = row['protein']
        pathogen_type = row['pathogen_type']
        pfam_id = row['pfamA_id']
        pfam_acc = row['pfamA_acc']
        pfam_description = row['description']
        # building data structures
        pfam_dict[pfam_id] = {'pfam_acc': pfam_acc, 'pfam_description': pfam_description}
        pfam_pathogen_dict[pfam_id].append(pathogen_type)

    for pfam_iter in pfam_pathogen_dict.keys():
        # ???   If a Pfam-A domain is only present in proteins of a certain pathogen_type,
        #       it should have only has 1 pathogen_type
        if len(set(pfam_pathogen_dict[pfam_iter])) != 1:
            pfam_pathogen_dict.pop(pfam_iter, None)

    return pfam_pathogen_dict, pfam_dict


def main():
    try:
        db = Database()
        pfam_pathogen_dict, pfam_dict = generateDomainsDataStructure(db)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    print("pathogen_type\tpfam_acc\tpfam_id\tdescription")
    for pfam_id, pathogen_type_list in sorted(pfam_pathogen_dict.iteritems(), key=operator.itemgetter(1, 0)):
        pfam_acc = pfam_dict[pfam_id]['pfam_acc']
        description = pfam_dict[pfam_id]['pfam_description']
        pathogen_type = pathogen_type_list[0]
        print(pathogen_type, pfam_id, pfam_acc, description, sep="\t")
    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)