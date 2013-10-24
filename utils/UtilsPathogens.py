__author__ = 'abarrera'


def get_number_ssp_stt_members(counts_species_pathogen_dict, pathogen_groups_set, collapse_flag):
    """
    Utility for the pathogen groups defined in the database. It computes the number of distinct species
    and strains contained in a dictionary.


    :param counts_species_pathogen_dict: counts of species and strains for each pathogen group in the database.
    :param pathogen_groups_set: for each Pfam, groups of pathogen types found.
    :param collapse_flag
    """
    pathogen = pathogen_groups_set.pop()
    total_num_species = int(counts_species_pathogen_dict[pathogen]['num_species'])
    total_num_strains = int(counts_species_pathogen_dict[pathogen]['num_strains'])
    if collapse_flag and pathogen != 2:
        if pathogen == 0:
            pathogen = 1
        elif pathogen == 1:
            pathogen = 0
        elif pathogen == 3:
            pathogen = 4
        elif pathogen == 4:
            pathogen = 3

        # pathogen = pathogen_groups_set.pop()
        total_num_species += int(counts_species_pathogen_dict[pathogen]['num_species'])
        total_num_strains += int(counts_species_pathogen_dict[pathogen]['num_strains'])

    return total_num_species, total_num_strains


def is_exclusive(pathogen_groups_set, collapse_pathogen_groups):
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