#!/usr/bin/python
"""
Script: retrieve_proteomes_fasta.py

Retrieve all complete/reference proteomes from (high hierarchy) taxon(s).
===================================================================================
Author: Alejandro Barrera
email: aebmad@gmail.com
"""
import sys
import subprocess
import fileinput
import urllib2

code_for_complete = '181'
code_for_reference = '1185'
url_list_complete_proteomes = \
    "http://www.uniprot.org/taxonomy/?query=ancestor:%s+complete:yes&format=list"
url_list_reference_proteomes = \
    "http://www.uniprot.org/taxonomy/?query=ancestor:%s+reference:yes&format=list"


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():

    try:
        ## Reads taxid, try to download as a reference proteome. if not a complete
        for line in fileinput.input():
            top_node = line.rstrip()
            try:
                # Get a list of all taxons below the top node with a complete proteome.
                url_response = urllib2.urlopen(url_list_complete_proteomes % top_node)
                download_proteomes_by_taxon_list(url_response, code_for_complete)
                url_response = urllib2.urlopen(url_list_reference_proteomes % top_node)
                download_proteomes_by_taxon_list(url_response, code_for_reference)

            except urllib2.URLError, urlErr:
                sys.exit(urlErr.reason)
    except Usage, err:
        print >> sys.stderr, err.msg
    sys.exit()

def download_proteomes_by_taxon_list(taxid_list, keyword):
    """
    Download all proteomes using taxonomy identifiers (taxids)
    :param taxon_list: a list of taxids
    """

    print "Downloading proteomes..."
    for taxid in taxid_list:
        command = """wget -c -O ./proteome_organism_swissprot_taxid_%s_%s.fasta 'http://www.uniprot.org/uniprot/?query=organism:%s+keyword:%s&force=yes&format=fasta&include=yes'""" % (
            taxid.rstrip(), keyword, taxid.rstrip(), keyword)
        subprocess.call(command, shell=True)
    print "Done."


if __name__ == "__main__":
    main()

