#!/usr/bin/python

from __future__ import division
from __future__ import print_function
from collections import defaultdict
from math import log, sqrt
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


class DomainPromiscuousException(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def getMsg(self):
        return self.msg


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
    Calculate domain promiscuity following TWO different metrics:

    -   Kullback-Leibler formula. Params:

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

    -   Weight Scores (et al. Lee & Lee, BMC Bioinformatics, 2009).
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
        raise DomainPromiscuousException("Domain %s doesn't appear in any multidomain protein in the species: %s" %
                                         (domain, key_species))
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

    return T_i, pi_i, singleton_pi_i, IAF_d, IV_d, weight_score


def generateSpeciesProteinDomainDict(db):
    """
    Create the dictionary with the data structure needed to represent bigram collections (domain combinations).
    :param db: database to access the data
    :return: bigrams specified as follows:
        bigrams['species1']['domain1']['appearances'] = appearances counter
        bigrams['species1']['domain1']['neighbours'] = list of neighbour domains
        bigrams['species1']['domain1']['proteins'] = list of proteins in which the domain1 has been found
    """
    # Data structure to return
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


class PromiscuousDomain(object):
    def __init__(self, domainName=None, metricValue=None):
        self.times_in_top = 0
        self.list_metric_values = []
        self.list_number_neighbours = []
        self.name = domainName
        self.metric_value = metricValue

    def getAvgMetricValues(self):
        return sum(self.list_metric_values) / len(self.list_metric_values)

    def getAvgNumberNeighbours(self):
        return sum(self.list_number_neighbours) / len(self.list_number_neighbours)

    def __cmp__(self, other):
        return self.name == other.name


def generatePromiscuousRankingOutput(bigrams):
    # Compute domain promiscuity and ranking of top "n" promiscuous domains
    n = 25

    topPromiscuousDomainsPi = defaultdict(PromiscuousDomain)
    topPromiscuousDomainsWF = defaultdict(PromiscuousDomain)

    # Promiscuous domains: for each domain in each species
    for key_species in sorted(bigrams):
        promiscuousList = []
        for key_domain in sorted(bigrams[key_species]):
            try:
                n_neighbors, pi_score, singleton_pi_i, IAF_d, IV_d, weight_score \
                    = processDomainPromiscuity(key_domain, key_species, bigrams)
                promiscuousList.append([key_domain, pi_score, weight_score, n_neighbors])
            except DomainPromiscuousException, e:
                # print(e.getMsg())
                continue

        # Select top xx most promiscuous domains (in case there are less than the fixed number 'n')
        top_n = min(n, promiscuousList.__len__())
        # Ranking of promiscuous domains in a given species by Pi (Kullback-Leibler formula)
        promiscuousList.sort(key=lambda x: x[1], reverse=True)
        # Add promiscuous domains to general counts
        for i in range(0, top_n):
            domain_key = promiscuousList[i][0]
            topPromiscuousDomainsPi[domain_key].times_in_top += 1
            topPromiscuousDomainsPi[domain_key].list_metric_values.append(promiscuousList[i][1])
            topPromiscuousDomainsPi[domain_key].list_number_neighbours.append(promiscuousList[i][3])

        # Ranking of promiscuous domains in a given species by weight-scores (Lee&Lee formula)
        promiscuousList.sort(key=lambda x: x[2])
        # Increase counters for the promiscuous domains
        for i in range(0, top_n):
            domain_key = promiscuousList[i][0]
            topPromiscuousDomainsWF[domain_key].times_in_top += 1
            topPromiscuousDomainsWF[domain_key].list_metric_values.append(promiscuousList[i][2])
            topPromiscuousDomainsWF[domain_key].list_number_neighbours.append(promiscuousList[i][3])

    # Print header for ranking of promiscuous domains
    print("method\ttimes_in_top\tavg_metric_value\tavg_number_neighbours")
    # Sort the counts of promiscuous domains for each metric and print them
    for domain in sorted(topPromiscuousDomainsPi,
                         key=lambda domain: topPromiscuousDomainsPi[domain].times_in_top, reverse=True):
        print("Pi_ranking", domain, topPromiscuousDomainsPi[domain].times_in_top,
              topPromiscuousDomainsPi[domain].getAvgMetricValues(),
              topPromiscuousDomainsPi[domain].getAvgNumberNeighbours(), sep='\t')

    for domain in sorted(topPromiscuousDomainsWF,
                         key=lambda domain: topPromiscuousDomainsWF[domain].times_in_top, reverse=True):
        print("Weight_scores_ranking", domain, topPromiscuousDomainsWF[domain].times_in_top,
              topPromiscuousDomainsWF[domain].getAvgMetricValues(),
              topPromiscuousDomainsWF[domain].getAvgNumberNeighbours(), sep='\t')
    return


def generatePromiscuousDomainOutput(bigrams):
    """
    Compute domain promiscuity from a bigrams dictionary. Generate the output in stdout.
    :param bigrams: data structure representing bigrams of protein domains
    """
    # Header of the output file produced
    print("species\tdomain\tnum_bigrams\tdomain_promiscuity\tsingleton_promiscuity_cutoff"
          "\tIAF_d\tIV_d\tweight_score")
    for key_species in sorted(bigrams):
        for key_domain in sorted(bigrams[key_species]):
            try:
                T_i, pi_i, singleton_pi_i, IAF_d, IV_d, weight_score \
                    = processDomainPromiscuity(key_domain, key_species, bigrams)
                # Output writen to STDOUT
                print(key_species, key_domain, T_i, pi_i, singleton_pi_i, IAF_d, IV_d, weight_score, sep='\t')
            except DomainPromiscuousException, e:
                # print(e.getMsg())
                continue


def similarityBetweenSpecies(listPromsDomainsA, squaredMetricsA, listPromsDomainsB, squaredMetricsB):
    sumCartesianProductPixQi = 0
    for promsDomainInA in listPromsDomainsA:
        matchesList = [x for x in listPromsDomainsB if x.name == promsDomainInA.name]
        if matchesList:
            sumCartesianProductPixQi += promsDomainInA.metric_value * matchesList[0].metric_value

    result = sumCartesianProductPixQi / sqrt(squaredMetricsA * squaredMetricsB)
    return result


def distanceBetweenSpecies(listPromsDomainsA, squaredMetricsA, listPromsDomainsB, squaredMetricsB):
    return 1 - similarityBetweenSpecies(listPromsDomainsA, squaredMetricsA, listPromsDomainsB, squaredMetricsB)


def angularSeparationMethod(bigrams):
    # Collection of promiscuous domains by species
    speciesInfo = defaultdict(list)

    # Promiscuous domains: for each domain in each species
    for key_species in sorted(bigrams):
        promiscuousList = []
        for key_domain in sorted(bigrams[key_species]):
            try:
                n_neighbors, pi_score, singleton_pi_i, IAF_d, IV_d, weight_score \
                    = processDomainPromiscuity(key_domain, key_species, bigrams)
                speciesInfo[key_species].append(PromiscuousDomain(key_domain, pi_score))

            except DomainPromiscuousException, e:
                # print(e.getMsg())
                continue
    speciesInfoCopy = speciesInfo.copy()
    distanceMatrix = defaultdict(dict)

    squaredMetricValues = defaultdict(float)
    for species in speciesInfo:
        sumSquaredMetric = 0
        for promsDomain in speciesInfo[species]:
            sumSquaredMetric += promsDomain.metric_value ** 2
        squaredMetricValues[species] = sumSquaredMetric

    print("\t", len(speciesInfo))
    for speciesA in sorted(speciesInfo):
        print(speciesA.ljust(10), end='\t')
        for speciesB in sorted(speciesInfoCopy):
            if speciesA == speciesB:
                distanceMatrix[speciesA][speciesB] = 0
                print(float(0), end='\t')
            else:
                distance = distanceBetweenSpecies(speciesInfo[speciesA], squaredMetricValues[speciesA],
                                                  speciesInfoCopy[speciesB], squaredMetricValues[speciesB])
                distanceMatrix[speciesA][speciesB] = distance
                print(distance, end='\t')
        print()


def main():
    try:
        db = Database()
        bigrams = generateSpeciesProteinDomainDict(db)
        db.close()
    except DatabaseError, e:
        sys.stdout.write(e.message)
        sys.exit(1)

    # generatePromiscuousRankingOutput(bigrams)
    # generatePromiscuousDomainOutput(bigrams)
    angularSeparationMethod(bigrams)
    return 1


if __name__ == '__main__':
    status = main()
    sys.exit(status)