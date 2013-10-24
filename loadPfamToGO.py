#!/usr/bin/python
"""
Load GO terms into a local MySQL database using a mapping file.
---------------------------------------------------------------
NOTE: If no file is provided, this script will automatically
      download the latest version of the file pfam2go.txt from
      the Gene Ontology public FTP.
"""

from ftplib import FTP
import os
import re
import sys
import tempfile
import textwrap
from PfamLocalDatabase import Database, DatabaseError

__author__ = 'Alejandro Barrera'
__date__ = '15 October 2013'
__credits__ = """Grant EIC-EMBL-2011-0091. Instituto de Salud Carlos III - EMBL-European Bioinformatics Institute"""


class Usage(Exception):
    """
    Usage class inherits from Exception (therefore the extensive documentation on Exception methods..).
    Incorporates a *msg* attribute to allow throwing a customized message.
    """

    def __init__(self, msg):
        self.msg = msg


def downloadPfam2GO():
    """Download the latest Pfam2GO file into a tempfile."""
    print('No Pfam2GO file provided. Preparing to download the latest version from http://www.geneontology.org/')
    nonPassive = False                      # force active mode FTP for server?
    fileName = 'pfam2go'                    # file to be downloaded
    dirName = '/pub/go/external2go/'        # remote directory to fetch from
    siteName = 'ftp.geneontology.org'       # FTP site to contact
    userInfo = ('anonymous', '')     # use () for anonymous

    print('Connecting...')
    connection = FTP(siteName)                  # connect to FTP site
    connection.login(*userInfo)                 # default is anonymous login
    connection.cwd(dirName)                     # xfer 1k at a time to localfile
    if nonPassive:                              # force active FTP if server requires
        connection.set_pasv(False)

    print('Downloading...')
    localFile = tempfile.NamedTemporaryFile(delete=False)   # local temporary file to store download
    connection.retrbinary('RETR ' + fileName, localFile.write, 1024)
    connection.quit()
    localFile.close()

    return localFile.name


def loadPfam2GOFile(PFAM_2_GO_FILE, db):
    """
    Parse a Pfam2GO file, inserting the terms into a local MySQL database.
    :param PFAM_2_GO_FILE: Pfam2GO text file with mapping of Pfam entries and GO terms.
    :param db: a PfamLocalDatabase object representing a local MySQL database instance.
    """
    # Walk the file creating GO terms if needed and adding them to pfamA_goTerm
    print("Updating database...")
    for line in open(PFAM_2_GO_FILE, 'r'):
        if line.startswith('!'):    # Ignore comments
            continue
            # Pfam:PF00001 7tm_1 > GO:G-protein coupled receptor activity ; GO:0004930
        match = re.search("^Pfam:(\S+).* > GO:(.*) ; GO:(\d+)$", line.rstrip())
        if match:
            pfamA_acc = match.group(1)                  # Pfam accession
            goTerm_name = str(match.group(2))           # GO term name
            goTerm_id = int(match.group(3))             # GO term id
            db.insertGoTerm(goTerm_id, goTerm_name)
            db.insertPfamAGoTerm(pfamA_acc, goTerm_id)


def main():
    """
    Load GO terms into a local MySQL database using a mapping file.
        - If no file is provided, the latest Pfam2GO mapping file from http://www.geneontology.org is downloaded into a
        temp file - located in /tmp/.
        - If a parameter is given, read Pfam2GO file (first argument) and load it into the database.
    """
    try:
        import argparse

        parser = argparse.ArgumentParser(
            prog='loadPfamToGO.py',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''
            Load GO terms into a local MySQL database using a mapping file.
            ---------------------------------------------------------------
            NOTE: If no file is provided, this script will automatically
                  download the latest version of the file pfam2go.txt from
                  the GeneOntology public FTP.
            '''))
        parser.add_argument('--file', dest='PFAM_2_GO_FILE', metavar='pfam2go.txt',
                            help='a tab-separated values file containing the mapping in a format similar to the one \
                           found at: http://www.geneontology.org/external2go/pfam2go')
        args = parser.parse_args()

        if args.PFAM_2_GO_FILE:
            # Pfam2GO file provided
            PFAM_2_GO_FILE = args.PFAM_2_GO_FILE
            if not os.path.exists(PFAM_2_GO_FILE):
                message = 'The file ' + PFAM_2_GO_FILE + ' doesn\'t exist'
                raise Usage(message)
        else:
            # Download Pfam2GO into a temporary file
            PFAM_2_GO_FILE = downloadPfam2GO()

        db = Database()
        loadPfam2GOFile(PFAM_2_GO_FILE, db)
        db.close()

    except (DatabaseError, Usage), e:
        sys.stdout.write(e.message)
        db.close()
        sys.exit(1)

    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)