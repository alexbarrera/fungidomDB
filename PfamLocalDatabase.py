import MySQLdb
import sys

__author__ = 'abarrera'


class DatabaseError(Exception):
    def __init__(self, msg='Unknown Database error'):
        """
        Database errors.
        :param msg:
        """
        self.message = msg

    def __init__(self, mySQLdbError):
        self.message = "[MySQL ERROR]: "
        self.message += '-'.join([str(errorMessage) for errorMessage in mySQLdbError.args])


class Database:
    def __init__(self):
        try:
            import MySQLdb
        except ImportError:
            print("You need to install the MySQLdb module. Check:\n"
                  "http://sourceforge.net/projects/mysql-python for details.")
            sys.exit(1)

        self.db = MySQLdb.connect(host="localhost", user="root", passwd="569291", db="pfam27")
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def getSpeciesProteinArchitectureIterator(self):
        """
        Retrieve a cursor to iterate over the results.

        :return: cursor iterator. Query fields: species, protein, architecture
        :raise: DatabaseError
        """
        try:
            # retrieve species, protein accession and pfam architectures
            self.cursor.execute("""select specie as species, p.accession as protein,
                                          a.architecture
                                     from pfamseq pf
                                       inner join protein p on pf.pfamseq_acc = p.accession
                                       inner join architecture a on a.auto_architecture =
                                                                    pf.auto_architecture
                                    where p.taxonomy like 'Eukaryota; Fungi%'"""
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

    def close(self):
        self.db.close()