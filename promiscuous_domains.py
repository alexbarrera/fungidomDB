#!/usr/bin/python

from __future__ import division
from __future__ import print_function
from collections import defaultdict
from math import log
import sys
from PfamLocalDatabase import Database, DatabaseError

"""
Analysis of the protein domain promiscuity.

Generates a tab-separated file with 2 different promiscuity quantitative measures:
   1. Weighted Bigram Frequency (Basu et al. 2008)
   2. Weight Score (Lee et al. 2009)

@:param db_user
@:param db_password
@:param db_user


Author: Alejandro Barrera
email: aebmad@gmail.com

"""

__author__ = 'abarrera'
__version__ = "$Revision: cfd6d2cb1ca6 $"
# $Source$




class Domain:
    def __init__(self, pfam_acc, pfam_id):
        """
        Contains Domain information.
        :param pfam_acc:
        :param pfam_id:
        """
        self.pfam_acc = pfam_acc
        self.pfam_id = pfam_id
        self.weighted_bigram_freq = None

    def set_weigthed_bigram_freq(self, wbf):
        self.weighted_bigram_freq = wbf


def processDomainPromiscuity(domain=None, key_species=None, bigrams=None):
    """
    Calculate domain promiscuity following Kullback-Leibler formula. Params:

        pi_i = quanitative measure of domain i promiscuity
            = beta_i*log(beta_i/f_i)
        beta_i = bigram frequency of domain i
              = T_i / (0.5*Sum[j=1, t]T_j)
        T_i = number of unique domain neighbors of domain i
        t   = number of distinct domain types
        f_i = frequency of domain i in the genome, we need number of domain per genome
           = n_i/N_i
        n_i = total count of domain i in a given genome
        N_i = total count of domains in a given genome

    Calculate everything regarding Weight Scores (et al. Lee & Lee, BMC Bioinformatics, 2009).
    Two measures Inverse Abundance Frequency (IAF) and Inverse Versatility (IV):

            weight_score = IAF_d * IV_d
            IAF_d = log_2(p_t/p_d)
                where   p_t = total number of proteins in a given genome
                        p_d = number of proteins containing domain 'd' in a given genome
            IV_d = 1/f_d
                where   f_d = number of distinct domain types/families adjacent to domain 'd'
    """
    T_i = len(set(bigrams[key_species][domain]['neighbours']))
    if not T_i:
        # print "Domain %s doesn't appear in any multidomain protein in the species: %s" % (domain, key_species)
        return
    t = len(bigrams)
    n_i = bigrams[key_species][domain]['appearances']
    N = 0
    sum_i_t = 0
    protein_list = []
    for domain_iter in bigrams[key_species]:
        N += bigrams[key_species][domain_iter]['appearances']
        sum_i_t += len(set(bigrams[key_species][domain_iter]['neighbours']))
        protein_list.append(bigrams[key_species][domain_iter]['proteins'])

    p_t = len(set([iter for sublist in protein_list for iter in sublist]))

    f_i = n_i / N

    # promiscuity value of a singleton, a domain present only once in the genome
    # and having only one bigram type, is taken as the cutoff
    singleton_pi_i = (1 / (0.5 * sum_i_t)) * log((1 / (0.5 * sum_i_t)) / (1 / N), 10)

    beta_i = T_i / (0.5 * sum_i_t)
    pi_i = beta_i * log(beta_i / f_i, 10)

    # Calculate Weight Score
    f_d = T_i
    IV_d = 1 / f_d

    p_d = len(set(bigrams[key_species][domain]['proteins']))
    IAF_d = log(p_t / p_d, 2)

    weight_score = IAF_d * IV_d

    # Output writen to STDOUT
    print(key_species, domain, T_i, pi_i, singleton_pi_i, IAF_d, IV_d, weight_score, sep='\t')
    return


def generateSpeciesProteinDomainDict(db):
    # Dictionary to return
    bigrams = defaultdict(lambda: defaultdict(lambda: defaultdict()))

    # create a data structure with architecture information
    for row in db.getSpeciesProteinArchitectureIterator():
        species = row['species']
        protein = row['protein']
        domains = str(row['architecture']).split('~') # Return list of proteins

        for i in range(len(domains) - 1): #last not iterated
            # bigrams[domains[i]][species]['count'] = bigrams[domains[i]][species]['count'] + 1
            bigrams[species][domains[i]].setdefault('appearances', 0)
            bigrams[species][domains[i]]['appearances'] += 1
            bigrams[species][domains[i]].setdefault('neighbours', []).append(domains[i + 1])
            bigrams[species][domains[i + 1]].setdefault('neighbours', []).append(domains[i])
            bigrams[species][domains[i]].setdefault('proteins', []).append(protein)
        bigrams[species][domains[len(domains) - 1]].setdefault('appearances', 0)
        bigrams[species][domains[len(domains) - 1]]['appearances'] += 1
        bigrams[species][domains[len(domains) - 1]].setdefault('neighbours', [])
        bigrams[species][domains[len(domains) - 1]].setdefault('proteins', []).append(protein)

    return bigrams


def main():
    try:
        db = Database()
        bigrams = generateSpeciesProteinDomainDict(db)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    print("species\tdomain\tnum_bigrams\tdomain_promiscuity\tsingleton_promiscuity_cutoff"
          "\tIAF_d\tIV_d\tweight_score")
    for key_species in sorted(bigrams):
        for key_domain in sorted(bigrams[key_species]):
            processDomainPromiscuity(key_domain, key_species, bigrams)

    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)