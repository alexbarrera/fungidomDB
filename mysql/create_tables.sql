-- MySQL dump 10.13  Distrib 5.5.32, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: pfam27
-- ------------------------------------------------------
-- Server version	5.5.32-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION */;
/*!40103 SET @OLD_TIME_ZONE = @@TIME_ZONE */;
/*!40103 SET TIME_ZONE = '+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0 */;
/*!40101 SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES = @@SQL_NOTES, SQL_NOTES = 0 */;

--
-- Table structure for table `architecture`
--

DROP TABLE IF EXISTS `architecture`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `architecture` (
  `auto_architecture` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `architecture`      TEXT,
  `no_seqs`           INT(8)           NOT NULL DEFAULT '0',
  `architecture_acc`  TEXT,
  PRIMARY KEY (`auto_architecture`),
  KEY `architecture_architecture_idx` (`architecture`(255)),
  KEY `architecture_architecture_acc_idx` (`architecture_acc`(255))
)
  ENGINE =MyISAM
  AUTO_INCREMENT =325028
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `goTerm`
--

DROP TABLE IF EXISTS `goTerm`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `goTerm` (
  `id`   INT(10) UNSIGNED NOT NULL,
  `name` TINYTEXT         NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE =InnoDB
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfamA`
--

DROP TABLE IF EXISTS `pfamA`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamA` (
  `auto_pfamA`           INT(5)                                      NOT NULL AUTO_INCREMENT,
  `pfamA_acc`            VARCHAR(7)                                  NOT NULL,
  `pfamA_id`             VARCHAR(16)                                 NOT NULL,
  `description`          VARCHAR(100)                                NOT NULL,
  `author`               TINYTEXT                                    NOT NULL,
  `seed_source`          TINYTEXT                                    NOT NULL,
  `type`                 ENUM('Family', 'Domain', 'Repeat', 'Motif') NOT NULL,
  `comment`              LONGTEXT,
  `model_length`         MEDIUMINT(8)                                NOT NULL,
  `number_archs`         INT(8) DEFAULT NULL,
  `number_species`       INT(8) DEFAULT NULL,
  `number_structures`    INT(8) DEFAULT NULL,
  `number_ncbi`          INT(8) DEFAULT NULL,
  `average_length`       DOUBLE(6, 2) DEFAULT NULL,
  `percentage_id`        INT(3) DEFAULT NULL,
  `average_coverage`     DOUBLE(6, 2) DEFAULT NULL,
  `number_shuffled_hits` INT(10) DEFAULT NULL,
  PRIMARY KEY (`auto_pfamA`),
  UNIQUE KEY `pfamA_acc` (`pfamA_acc`),
  UNIQUE KEY `pfamA_id` (`pfamA_id`)
)
  ENGINE =MyISAM
  AUTO_INCREMENT =15521
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfamA_architecture`
--

DROP TABLE IF EXISTS `pfamA_architecture`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamA_architecture` (
  `auto_pfamA`        INT(5)           NOT NULL DEFAULT '0',
  `auto_architecture` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  KEY `auto_pfamA` (`auto_pfamA`),
  KEY `auto_architecture` (`auto_architecture`)
)
  ENGINE =MyISAM
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfamA_goTerm`
--

DROP TABLE IF EXISTS `pfamA_goTerm`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamA_goTerm` (
  `pfamA_acc` VARCHAR(7) NOT NULL,
  `goTerm_id` INT(10)    NOT NULL,
  PRIMARY KEY (`pfamA_acc`, `goTerm_id`)
)
  ENGINE =InnoDB
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pfamseq`
--

DROP TABLE IF EXISTS `pfamseq`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamseq` (
  `auto_pfamseq`      INT(10)      NOT NULL AUTO_INCREMENT,
  `pfamseq_id`        VARCHAR(12)  NOT NULL,
  `pfamseq_acc`       VARCHAR(6)   NOT NULL,
  `seq_version`       TINYINT(4)   NOT NULL,
  `description`       TEXT         NOT NULL,
  `evidence`          TINYINT(4)   NOT NULL,
  `length`            MEDIUMINT(8) NOT NULL DEFAULT '0',
  `species`           TEXT         NOT NULL,
  `taxonomy`          MEDIUMTEXT,
  `is_fragment`       TINYINT(1) DEFAULT NULL,
  `sequence`          BLOB         NOT NULL,
  `updated`           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created`           DATETIME DEFAULT NULL,
  `ncbi_taxid`        INT(10) UNSIGNED DEFAULT '0',
  `genome_seq`        TINYINT(1) DEFAULT '0',
  `auto_architecture` INT(10) DEFAULT NULL,
  `treefam_acc`       VARCHAR(8) DEFAULT NULL,
  PRIMARY KEY (`auto_pfamseq`),
  UNIQUE KEY `pfamseq_acc` (`pfamseq_acc`),
  KEY `ncbi_taxid` (`ncbi_taxid`),
  KEY `pfamseq_id` (`pfamseq_id`),
  KEY `pfamseq_architecture_idx` (`auto_architecture`),
  KEY `pfamseq_ncbi_code_idx` (`ncbi_taxid`, `genome_seq`),
  KEY `pfamseq_acc_version` (`pfamseq_acc`, `seq_version`),
  KEY `pfamseq_tax_idx` (`taxonomy`(350))
)
  ENGINE =MyISAM
  AUTO_INCREMENT =25397992
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `protein`
--

DROP TABLE IF EXISTS `protein`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `protein` (
  `id`                               INT(11)     NOT NULL AUTO_INCREMENT,
  `accession`                        VARCHAR(45) NOT NULL,
  `length`                           INT(11) DEFAULT '0',
  `source`                           VARCHAR(8) DEFAULT NULL,
  `processed`                        INT(11) DEFAULT '0',
  `signalp`                          VARCHAR(16) DEFAULT NULL,
  `full_name`                        VARCHAR(256) DEFAULT NULL,
  `EC`                               VARCHAR(16) DEFAULT NULL,
  `Transmembrane`                    VARCHAR(16) DEFAULT NULL,
  `Subcellular_location_CC`          VARCHAR(100) DEFAULT NULL,
  `Membrane`                         VARCHAR(16) DEFAULT NULL,
  `Cell_wall`                        VARCHAR(16) DEFAULT NULL,
  `Cell_wall_biogenesis_degradation` VARCHAR(16) DEFAULT NULL,
  `specie`                           VARCHAR(128) DEFAULT NULL,
  `taxonomy`                         MEDIUMTEXT,
  `gene_name`                        VARCHAR(32) DEFAULT NULL,
  `pdb`                              VARCHAR(8) DEFAULT NULL,
  `ensembl_fungi_transcript_id`      VARCHAR(32) DEFAULT NULL,
  `supFam`                           VARCHAR(32) DEFAULT NULL,
  `taxID`                            INT(10) DEFAULT NULL,
  `specie_short`                     VARCHAR(8) DEFAULT NULL,
  `human_homolog`                    INT(1) DEFAULT '0',
  `pathogen_type`                    TINYINT(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accession` (`accession`)
)
  ENGINE =InnoDB
  AUTO_INCREMENT =4533512
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE = @OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE = @OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES = @OLD_SQL_NOTES */;


