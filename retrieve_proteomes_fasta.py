
#!/usr/bin/python
import sys
import re
import os
import subprocess
import fileinput
#import pdb; pdb.set_trace()
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

    """
    Script: retrieve_proteomes_fasta.py

    Retrieve all complete/reference proteomes from (high hierarchy) taxon(s).
    ===================================================================================
    Author: Alejandro Barrera
    email: aebmad@gmail.com
    """

    # use strict;
    # use warnings;
    # use LWP::UserAgent;
    # use HTTP::Date;
    #
    # # Taxonomy identifier of top node for query, e.g. 2 for Bacteria, 2157 for Archea, etc.
    # # (see http://www.uniprot.org/taxonomy)
    # top_node = sys.argv[0];
    #
    # my $reference = 0; # Toggle this to 1 if you want reference instead of complete proteomes.
    # my $proteome = $reference ? 'reference:yes' : 'complete:yes';
    # my $keyword = $reference ? 'keyword:1185' : 'keyword:181';
    #
    # my $contact = ''; # Please set your email address here to help us debug in case of problems.
    # my $agent = LWP::UserAgent->new(agent => "libwww-perl $contact");
    #
    # # Get a list of all taxons below the top node with a complete/reference proteome.
    # my $query_list = "http://www.uniprot.org/taxonomy/?query=ancestor:$top_node+$proteome&format=list";
    # my $response_list = $agent->get($query_list);
    # die 'Failed, got ' . $response_list->status_line .
    #   ' for ' . $response_list->request->uri . "\n"
    #   unless $response_list->is_success;
    #
    # # For each taxon, mirror its proteome in FASTA format.
    # for my $taxon (split(/\n/, $response_list->content)) {
    #   my $file = $taxon . '.fasta';
    #   my $query_taxon = "http://www.uniprot.org/uniprot/?query=organism:$taxon+$keyword&format=fasta&include=yes";
    #   my $response_taxon = $agent->mirror($query_taxon, $file);
    #
    #   if ($response_taxon->is_success) {
    #     my $results = $response_taxon->header('X-Total-Results');
    #     my $release = $response_taxon->header('X-UniProt-Release');
    #     my $date = sprintf("%4d-%02d-%02d", HTTP::Date::parse_date($response_taxon->header('Last-Modified')));
    #     print "File $file: downloaded $results entries of UniProt release $release ($date)\n";
    #   }
    #   elsif ($response_taxon->code == HTTP::Status::RC_NOT_MODIFIED) {
    #     print "File $file: up-to-date\n";
    #   }
    #   else {
    #     die 'Failed, got ' . $response_taxon->status_line .
    #       ' for ' . $response_taxon->request->uri . "\n";
    #   }
    # }
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

