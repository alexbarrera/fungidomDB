#!/usr/bin/python
"""
PfamLocalDatabase objects to connect, access and modify a MySQL database.
-------------------------------------------------------------------------
NOTE:   This scripts uses the database credentials from the .my.cnf file
^^^^^   under a [pfam] tag. The user should be granted with CRUD
        permissions into the pfam27 schema.

"""
import sys


__author__ = 'abarrera'


class DatabaseError(Exception):
    """
    DatabaseError inherits from Exception (therefore the extensive documentation on Exception methods..).
    Incorporates a *msg* attribute to allow throwing customized messages.
    """

    def __init__(self, msg='Unknown Database error'):
        '''
        Database errors.
        :param msg:
        '''
        self.message = msg

    def __init__(self, mySQLdbError):
        self.message = "[MySQL ERROR]: "
        self.message += '-'.join([str(errorMessage) for errorMessage in mySQLdbError.args])


class Database:
    """
    Provides access to the Pfam database.
    Represents a centralized access point to connect, query and update the underlying database.
    """

    def __init__(self):
        try:
            import MySQLdb
        except ImportError:
            print("You need to install the MySQLdb module. Check:\n"
                  "http://sourceforge.net/projects/mysql-python for details.")
            sys.exit(1)

        self.db = MySQLdb.connect(host="localhost", db="pfam27", read_default_group='pfam' )
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def getSpeciesProteinArchitectureIterator(self):
        """
        Retrieve a cursor to iterate over the results.

        :return: cursor iterator. Query fields: species, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""select specie_short as species, p.accession as protein,
                                          a.architecture
                                     from pfamseq pf
                                       inner join protein p on pf.pfamseq_acc = p.accession
                                       inner join architecture a on a.auto_architecture =
                                                                    pf.auto_architecture
                                    where p.specie = 'Homo sapiens'"""
            )

            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def getArchitecturePathogenTypeIterator(self):
        """
        Retrieve a cursor to iterate over the results.

        :return: cursor iterator. Query fields: architecture, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""select   p2.specie as species,
                                            p2.accession,
                                            p2.pathogen_type,
                                            a2.architecture,
                                            a2.architecture_acc
                                        from architecture a2
                                            inner join pfamseq pf2 on a2.auto_architecture = pf2.auto_architecture
                                            inner join protein p2 on pf2.pfamseq_acc = p2.accession
                                        where p2.taxonomy like 'Eukaryota; Fungi%'"""
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def getSpeciesPhylumIterator(self):
        """
        List of species per phylum

        :return: Cursor iterator. Query fields: architecture, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""
                    select distinct
                        substring_index(substring_index(p.taxonomy, ';', 4),'; ',-1) as phylum,
                        p.specie as species
                    from protein p
                    where p.specie <> 'Homo sapiens'
                      and substring_index(substring_index(p.taxonomy, ';', 4),';',-1)  is not null
                    order by phylum, species;
                    """
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def getArchitecturesIterator(self):
        """
        Architecture (accession and name), and taxonomical information (phylum, subphylum, species, strains)
         for all fungal proteins in the database.

        :return: Cursor iterator. Query fields: architecture, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""
                select distinct
                    substring_index(substring_index(p.taxonomy, '; ', 4),'; ',-1) as phylum,
                    substring_index(substring_index(p.taxonomy, '; ', 5),'; ',-1) as subphylum,
                    substring_index(substring_index(p.taxonomy, '; ', 8),'; ',-1) as "order",
                    replace(substring_index(p.taxonomy, '; ',-1), '.','') as genus ,
                    substring_index(p.specie, ' (', 1) as species,
                    p.specie as strains,
                    a.architecture,
                    a.architecture_acc
                from architecture a
                    inner join pfamseq pf on pf.auto_architecture = a.auto_architecture
                    inner join protein p on pf.pfamseq_acc = p.accession
                where p.taxonomy like "Eukaryota; Fungi%"
                  and pf.auto_architecture <> 0"""
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def getDomainsIterator(self):
        """
        Create an iterator to retrieve fungal domains and the species in which are present.

        :return: Cursor iterator.
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""
                select distinct
                    substring_index(substring_index(p.taxonomy, '; ', 4),'; ',-1) as phylum,
                    substring_index(substring_index(p.taxonomy, '; ', 5),'; ',-1) as subphylum,
                    substring_index(substring_index(p.taxonomy, '; ', 8),'; ',-1) as "order",
                    replace(substring_index(p.taxonomy, '; ',-1), '.','') as genus ,
                    substring_index(p.specie, ' (', 1) as species,
                    p.specie as strains,
                    pfa.pfamA_id,
                    pfa.pfamA_acc
                from pfamseq pf
                      inner join protein p on pf.pfamseq_acc = p.accession
                      inner join pfamA_architecture pa on pa.auto_architecture = pf.auto_architecture
                      inner join pfamA pfa on pfa.auto_pfamA = pa.auto_pfamA
                where p.taxonomy like "Eukaryota; Fungi%" """
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def getTaxonomyIterator(self):
        """
        Architecture (accession and name), and taxonomical information (phylum, subphylum, species, strains)
         for all fungal proteins in the database.

        :return: Cursor iterator. Query fields: architecture, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""
                select distinct
                    substring_index(substring_index(p.taxonomy, '; ', 4),'; ',-1) as phylum,
                    substring_index(substring_index(p.taxonomy, '; ', 5),'; ',-1) as subphylum,
                    substring_index(substring_index(p.taxonomy, '; ', 8),'; ',-1) as "order",
                    replace(substring_index(p.taxonomy, '; ',-1), '.','') as genus ,
                    substring_index(p.specie, ' (', 1) as species,
                    specie as strains
                from protein p
                where p.taxonomy like "Eukaryota; Fungi%";
                ; """
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def getDomainsPathogenTypeIterator(self):
        """
        Retrieve a cursor to iterate over the results.

        :return: cursor iterator. Query fields: architecture, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""select p.specie as species,
                                        p.accession as protein,
                                        p.pathogen_type,
                                        pfa.pfamA_acc,
                                        pfa.pfamA_id,
                                        pfa.description
                                    from pfamA_architecture pa
                                        inner join pfamseq pf on pa.auto_architecture = pf.auto_architecture
                                        inner join protein p on pf.pfamseq_acc = p.accession
                                        inner join pfamA pfa on pfa.auto_pfamA = pa.auto_pfamA
                                    where p.taxonomy like 'Eukaryota; Fungi%'"""
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def insertGoTerm(self, id, name):
        """
        Create a new GoTerm if it doesn't exists
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""INSERT IGNORE INTO goTerm(id, name) VALUES (%d, "%s")""" % (id, name))
            self.db.commit()
            return

        except MySQLdb.Error, e:
            print e
            self.db.rollback()
            raise DatabaseError(e)

    def insertPfamAGoTerm(self, pfamA_acc, goTerm_id):
        """
        Create a new association pfamA~GoTerm
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""INSERT IGNORE INTO pfamA_goTerm(pfamA_acc, goTerm_id) VALUES ("%s", %d)"""
                                % (pfamA_acc, goTerm_id))
            self.db.commit()
            return

        except MySQLdb.Error, e:
            print e
            self.db.rollback()
            raise DatabaseError(e)

    def getNumSpeciesPathogen(self):
        """
        Find total numbers of species for each pathogen group

        :return: dictionary with pathogen groups keys and total number of species values
        :raise: DatabaseError
        """
        try:
            # retrieve total number of species per pathogen group
            self.cursor.execute("""
                SELECT p.pathogen_type,
                    count(distinct substring_index(p.specie, ' (', 1) ) as num_species,
                    count(distinct p.specie_short) as num_strains
                FROM protein p
                WHERE p.pathogen_type is not null
                GROUP BY p.pathogen_type
                ORDER BY p.pathogen_type;"""
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)


    def getProteins(self, pfam_in_clause=''):
        """
        Retrieve protein information from a list of Pfam Ids

        :param pfam_list: pfam ids list
        :return: protein information
        """
        #To don't overload the database, query in batches, 100 pfam_domains max
        try:
            self.cursor.execute("""
                select distinct p.accession, p.full_name, p.transmembrane, p.membrane, p.cell_wall,
                                p.specie, p.taxonomy, p.pathogen_type, aa.architecture, aa.architecture_acc
                from pfamseq pf
                      inner join protein p on pf.pfamseq_acc = p.accession
                      inner join architecture aa on aa.auto_architecture = pf.auto_architecture
                      inner join pfamA_architecture pa on pa.auto_architecture = pf.auto_architecture
                      inner join pfamA pfa on pfa.auto_pfamA = pa.auto_pfamA
                where pfa.pfamA_id in ('%s')
                order by p.specie;""" % pfam_in_clause
            )
            return self.cursor

        except MySQLdb.Error, e:
            print e
            raise DatabaseError(e)

    def close(self):
        self.db.close()