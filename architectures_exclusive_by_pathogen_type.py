#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
import sys
import operator
from PfamLocalDatabase import Database, DatabaseError
from utils.UtilsPathogens import get_number_ssp_stt_members

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


def generateArchitectureDataStructure(db, collapse_pathogen_groups=False):
    """
    Create a dictionary with domain architectures exclusive in a single pathogen type group.
    :param db: database object
    :return: dictionary
        key: tuple (architecture_acc, architecture)
        value: list of pathogen_type
            (it might contain duplicates, but all values are equal => convert to set)
    """

    # Calculate total numbers of species and strains for each pathogen group
    counts_species_pathogen_dict = defaultdict(lambda: defaultdict(int))
    for row in db.getNumSpeciesPathogen():
        counts_species_pathogen_dict[row['pathogen_type']]['num_species'] = row['num_species']
        counts_species_pathogen_dict[row['pathogen_type']]['num_strains'] = row['num_strains']

    architecture_pathogen_dict = defaultdict(list)
    arch_strains_species_dict = defaultdict(lambda: defaultdict(list))
    for row in db.getArchitecturePathogenTypeIterator():
        strains = row['species']
        species = str(strains).split(' (')[0]
        pathogen_type = row['pathogen_type']
        architecture_id = row['architecture']
        architecture_acc = row['architecture_acc']
        architecture_pathogen_dict[(architecture_id, architecture_acc)].append(pathogen_type)
        arch_strains_species_dict[(architecture_id, architecture_acc)]['species'].append(species)
        arch_strains_species_dict[(architecture_id, architecture_acc)]['strains'].append(strains)

    for architecture in architecture_pathogen_dict.keys():
        # If an architecture is only present in proteins of a certain pathogen_type,
        # it should have only 1 pathogen_type
        pathogen_groups_set = set(architecture_pathogen_dict[architecture])
        if not exclusive_arch(pathogen_groups_set, collapse_pathogen_groups):
            architecture_pathogen_dict.pop(architecture)
            arch_strains_species_dict.pop(architecture)
        else:
            # Check if the architecture is present in all species and strains
            species_set = set(arch_strains_species_dict[architecture]['species'])
            strains_set = set(arch_strains_species_dict[architecture]['strains'])
            total_num_species, total_num_strains = get_number_ssp_stt_members(counts_species_pathogen_dict,
                                                                              pathogen_groups_set,
                                                                              collapse_pathogen_groups)
            arch_strains_species_dict[architecture]['total_num_species'] = total_num_species
            arch_strains_species_dict[architecture]['total_num_strains'] = total_num_strains
            if total_num_species == len(species_set):
                arch_strains_species_dict[architecture]['all_species']
                if total_num_strains == len(strains_set):
                    arch_strains_species_dict[architecture]['all_strains']

    return architecture_pathogen_dict, arch_strains_species_dict


def exclusive_arch(pathogen_groups_set, collapse_pathogen_groups):
    """
    Boolean function to check if a given architecture is exclusive.
    :param pathogen_groups_set: all pathogen groups for a given architecture
    :param collapse_pathogen_groups: flag to consider 3 instead of 5 groups
        (0 and 1, 3 and 4, 2)
    :return: True if exclusive, False otherwise
    """
    if len(pathogen_groups_set) == 1:
        return True

    # Only check pathogen grouping when the flag is on
    if collapse_pathogen_groups:
        if len(pathogen_groups_set) > 2:
            return False
        if 0 in pathogen_groups_set and 1 in pathogen_groups_set:
            return True
        if 3 in pathogen_groups_set and 4 in pathogen_groups_set:
            return True
    return False


def group_representation(pathogen_group, collapse_pathogen_groups):
    if collapse_pathogen_groups:
        # Groups 0 and 1 => 1
        # Groups 3 and 4 => 3
        if pathogen_group == 0:
            return 1
        if pathogen_group == 4:
            return 3
    return pathogen_group


def print_output(architectures, arch_in_all_members_dict, collapse_pathogen_groups):
    print("pathogen_type\tarchitecture_name\tarchitecture_acc\trepresented_species\trepresented_strains")
    for architecture_descriptors, pathogen_type_list in sorted(architectures.iteritems(),
                                                               key=operator.itemgetter(1, 0)):
        architecture, architecture_acc = architecture_descriptors
        pathogen_type = group_representation(pathogen_type_list[0], collapse_pathogen_groups)
        in_every_member = ''
        no_species = len(set(arch_in_all_members_dict[architecture_descriptors]['species']))
        no_strains = len(set(arch_in_all_members_dict[architecture_descriptors]['strains']))
        total_species = arch_in_all_members_dict[architecture_descriptors]['total_num_species']
        total_strains = arch_in_all_members_dict[architecture_descriptors]['total_num_strains']
        if arch_in_all_members_dict[architecture_descriptors]['all_species']:
            in_every_member += 'all_species'
            if arch_in_all_members_dict[architecture_descriptors]['all_strains']:
                in_every_member += '\t' + 'all_strains'
        print(pathogen_type, architecture, architecture_acc, str(no_species) + '/' + str(total_species),
              str(no_strains) + '/' + str(total_strains), in_every_member, sep="\t")


def main():
    collapse_pathogen_groups = False
    try:
        db = Database()
        architectures, arch_in_all_members_dict = generateArchitectureDataStructure(db, collapse_pathogen_groups)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    print_output(architectures, arch_in_all_members_dict, collapse_pathogen_groups)
    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)