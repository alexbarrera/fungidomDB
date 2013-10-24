fungidomDB
==========

Database for fungal protein domain information 

--

##*Database creation*

```create_db.sql``` generates the MySQL database schema. It contains a tailored version of Pfam 27.0 database and protein information from UniProtKB. A user capable to create databases is needed*.
Open a mysql console with administrative privileges and type:

    > mysql -Dpfam27 -u your_user -p < create_db.sql

***By default, mysql-server has a 'root' superuser. Use it unless you have a customized administartor user**

You will need to grant CRUD privileges on fungidom database to your mysql user.
Open a mysql console with administrative privileges and type:

    mysql> GRANT ALL on pfam27.* TO 'your_user'.

The credential used to access the MySQL database have to be placed under a [pfam] tag in your
mysql configuration file (typically ~/.my.cnf file). It should look something like this:

    ##########################################################
    #   Configuration for Python scripts to work with Pfam   #
    ##########################################################
    [pfam]
    host=127.0.0.1
    port=3307
    database=pfam27
    default-character-set=utf8
    password=***your_password

###*Python dependencies:*
- MySQLdb --If you have a Debian distribution try this: sudo apt-get install python-mysqldb
