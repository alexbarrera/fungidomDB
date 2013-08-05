from ftplib import FTP
import os
import re
import sys
import tempfile
from PfamLocalDatabase import Database, DatabaseError

__author__ = 'abarrera'


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def downloadPfam2GO():
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
    # Walk the file creating GO terms if needed and adding them to pfamA_goTerm
    print("Updating database...")
    for line in open(PFAM_2_GO_FILE, 'r'):
        if line.startswith('!'):    # Ignore comments
            continue
            # Pfam:PF00001 7tm_1 > GO:G-protein coupled receptor activity ; GO:0004930
        match = re.search("^Pfam:(\S+).* > GO:(.*) ; GO:(\d+)$", line.rstrip())
        if match:
            pfamA_acc = match.group(1)
            goTerm_name = str(match.group(2))
            goTerm_id = int(match.group(3))
            db.insertGoTerm(goTerm_id, goTerm_name)
            db.insertPfamAGoTerm(pfamA_acc, goTerm_id)


def main():
    """

    By default, download latest Pfam2GO mapping from www.geneontology.org and update the local database.
    If a parameter is given, read Pfam2GO file (first argument) and load it into the database.
    :return:
    """
    try:
        PFAM_2_GO_FILE = ''
        if len(sys.argv) > 2:
            # Pfam2GO file provided
            PFAM_2_GO_FILE = sys.argv[1]
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