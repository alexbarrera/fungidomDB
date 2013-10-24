#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
import sys
import operator
from PfamLocalDatabase import Database, DatabaseError
from utils.UtilsPathogens import get_number_ssp_stt_members, is_exclusive

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


def generateDomainsDataStructure(db, collapse_pathogen_groups=False):
    """
    Create a dictionary with pfam domains exclusive in a single pathogen type group
    :param db: database object
    :return:
        - *dictionary* with key:pfam_acc, value:list of pathogen_type
            (it might contain duplicates, but all values are equal => convert to set)
        - *dictionary* with pfam domain info to output (pfam_acc, pfam_id, description)
        - *dictionary* species and strains info for each domain
    """

    # Calculate total numbers of species and strains for each pathogen group
    counts_species_pathogen_dict = defaultdict(lambda: defaultdict(int))
    for row in db.getNumSpeciesPathogen():
        counts_species_pathogen_dict[row['pathogen_type']]['num_species'] = row['num_species']
        counts_species_pathogen_dict[row['pathogen_type']]['num_strains'] = row['num_strains']

    domain_strains_species_dict = defaultdict(lambda: defaultdict(list))
    pfam_pathogen_dict = defaultdict(list)
    pfam_dict = defaultdict()
    for row in db.getDomainsPathogenTypeIterator():
        strains = row['species']
        species = str(strains).split(' (')[0]
        protein = row['protein']
        pathogen_type = row['pathogen_type']
        pfam_id = row['pfamA_id']
        pfam_acc = row['pfamA_acc']
        pfam_description = row['description']
        # building data structures
        pfam_dict[pfam_id] = {'pfam_acc': pfam_acc, 'pfam_description': pfam_description}
        pfam_pathogen_dict[pfam_id].append(pathogen_type)
        domain_strains_species_dict[pfam_id]['species'].append(species)
        domain_strains_species_dict[pfam_id]['strains'].append(strains)

    for pfam_iter in pfam_pathogen_dict.keys():
        # ???   If a Pfam-A domain is only present in proteins of a certain pathogen_type,
        #       it should have only has 1 pathogen_type

        pathogen_groups_set = set(pfam_pathogen_dict[pfam_iter])
        if not is_exclusive(pathogen_groups_set, collapse_pathogen_groups):
            pfam_pathogen_dict.pop(pfam_iter)
            domain_strains_species_dict.pop(pfam_iter)
        else:
            # Check if the architecture is present in all species and strains
            species_set = set(domain_strains_species_dict[pfam_iter]['species'])
            strains_set = set(domain_strains_species_dict[pfam_iter]['strains'])
            total_num_species, total_num_strains = get_number_ssp_stt_members(counts_species_pathogen_dict,
                                                                              pathogen_groups_set,
                                                                              collapse_pathogen_groups)
            domain_strains_species_dict[pfam_iter]['total_num_species'] = total_num_species
            domain_strains_species_dict[pfam_iter]['total_num_strains'] = total_num_strains
            if total_num_species == len(species_set):
                domain_strains_species_dict[pfam_iter]['all_species']
                if total_num_strains == len(strains_set):
                    domain_strains_species_dict[pfam_iter]['all_strains']
    return pfam_pathogen_dict, pfam_dict, domain_strains_species_dict


def group_representation(pathogen_group, collapse_pathogen_groups):
    if collapse_pathogen_groups:
        # Groups 0 and 1 => 1
        # Groups 3 and 4 => 3
        if pathogen_group == 0:
            return 1
        if pathogen_group == 4:
            return 3
    return pathogen_group


def print_output(pfam_pathogen_dict, pfam_dict, domain_species_dict, collapse_pathogen_groups):
    print("pathogen_type\tpfam_acc\tpfam_id\tdescription\trepresented_species\trepresented_strains")
    for pfam_id, pathogen_type_list in sorted(pfam_pathogen_dict.iteritems(), key=operator.itemgetter(1, 0)):
        pfam_acc = pfam_dict[pfam_id]['pfam_acc']
        description = pfam_dict[pfam_id]['pfam_description']
        pathogen_type = group_representation(pathogen_type_list[0], collapse_pathogen_groups)
        in_every_member = ''
        no_species = len(set(domain_species_dict[pfam_id]['species']))
        no_strains = len(set(domain_species_dict[pfam_id]['strains']))
        total_species = domain_species_dict[pfam_id]['total_num_species']
        total_strains = domain_species_dict[pfam_id]['total_num_strains']
        if domain_species_dict[pfam_id]['all_species']:
            in_every_member += 'all_species'
            if domain_species_dict[pfam_id]['all_strains']:
                in_every_member += '\t' + 'all_strains'
        print(pathogen_type, pfam_id, pfam_acc, description, str(no_species) + '/' + str(total_species),
              str(no_strains) + '/' + str(total_strains), in_every_member, sep="\t")
    return


def main():
    collapse_pathogen_groups = False
    try:
        db = Database()
        pfam_pathogen_dict, pfam_dict, domain_species_dict = generateDomainsDataStructure(db, collapse_pathogen_groups)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    print_output(pfam_pathogen_dict, pfam_dict, domain_species_dict, collapse_pathogen_groups)
    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)