#!/usr/bin/python
import os
import sys
import fileinput
from PfamLocalDatabase import Database, DatabaseError

__author__ = 'abarrera'


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def getProteinsFromPfamIdList(pfam_list, db):
    """
    Find architectures and proteins with the pfam domains provided in the list

    :param pfam_list: pfam domain list
    :param db: database to query
    """
    first = 0
    last = len(pfam_list) - 1
    MAX_ELEMENT_IN_CLAUSE = 100 # Limit number to build the "in" clause.
    # If more than this, brake the query into smaller queries
    elements_remaining = True
    print_header_flag = True
    while elements_remaining:
        # join first MAX_ELEMENT_IN_CLAUSE elements into an in clause
        in_clause = '\', \''.join(pfam_list[first:first + MAX_ELEMENT_IN_CLAUSE])
        for row in db.getProteins(in_clause):
            if print_header_flag:
                print '\t'.join([field for field in row.keys()])
                print_header_flag = False
            print '\t'.join([str(value) if value else 'None' for value in row.values()])
        first += MAX_ELEMENT_IN_CLAUSE
        elements_remaining = last - first > 0


def main():
    """

    Retrieve Proteins containing a list of Pfam identifiers
    :optional param: file with pfam identifiers
    :return: Protein information in Stdout
    """
    try:
        PFAM_IDS_FILE = ''
        if len(sys.argv) == 2:
            # PfamIds file provided
            PFAM_IDS_FILE = sys.argv[1]
            if not os.path.exists(PFAM_IDS_FILE):
                message = 'The file ' + PFAM_IDS_FILE + ' doesn\'t exist\n'
                raise Usage(message)

        pfam_list = [line.rstrip() for line in fileinput.input()]   # IMPORTANT: fileinput reads from file if specified,
        # from stdin otherwise
        db = Database()
        getProteinsFromPfamIdList(pfam_list, db)
        db.close()

    except Usage, e:
        sys.stdout.write(e.msg)
        sys.exit(1)

    except DatabaseError, e:
        sys.stdout.write(e.message)
        db.close()
        sys.exit(1)

    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)