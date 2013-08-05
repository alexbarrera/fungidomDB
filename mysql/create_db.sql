/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `architecture` (
  `auto_architecture` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `architecture`      TEXT,
  `type_example`      INT(10)          NOT NULL DEFAULT '0',
  `no_seqs`           INT(8)           NOT NULL DEFAULT '0',
  `architecture_acc`  TEXT,
  PRIMARY KEY (`auto_architecture`),
  KEY `architecture_type_example_idx` (`type_example`),
  KEY `architecture_architecture_idx` (`architecture`(255)),
  KEY `architecture_architecture_acc_idx` (`architecture_acc`(255))
)
  ENGINE =MyISAM
  AUTO_INCREMENT =325028
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamA` (
  `auto_pfamA`           INT(5)                                      NOT NULL AUTO_INCREMENT,
  `pfamA_acc`            VARCHAR(7)                                  NOT NULL,
  `pfamA_id`             VARCHAR(16)                                 NOT NULL,
  `previous_id`          TINYTEXT,
  `description`          VARCHAR(100)                                NOT NULL,
  `author`               TINYTEXT                                    NOT NULL,
  `deposited_by`         VARCHAR(100)                                NOT NULL DEFAULT 'anon',
  `seed_source`          TINYTEXT                                    NOT NULL,
  `type`                 ENUM('Family', 'Domain', 'Repeat', 'Motif') NOT NULL,
  `comment`              LONGTEXT,
  `sequence_GA`          DOUBLE(8, 2)                                NOT NULL,
  `domain_GA`            DOUBLE(8, 2)                                NOT NULL,
  `sequence_TC`          DOUBLE(8, 2)                                NOT NULL,
  `domain_TC`            DOUBLE(8, 2)                                NOT NULL,
  `sequence_NC`          DOUBLE(8, 2)                                NOT NULL,
  `domain_NC`            DOUBLE(8, 2)                                NOT NULL,
  `buildMethod`          TINYTEXT                                    NOT NULL,
  `model_length`         MEDIUMINT(8)                                NOT NULL,
  `searchMethod`         TINYTEXT                                    NOT NULL,
  `msv_lambda`           DOUBLE(8, 2)                                NOT NULL,
  `msv_mu`               DOUBLE(8, 2)                                NOT NULL,
  `viterbi_lambda`       DOUBLE(8, 2)                                NOT NULL,
  `viterbi_mu`           DOUBLE(8, 2)                                NOT NULL,
  `forward_lambda`       DOUBLE(8, 2)                                NOT NULL,
  `forward_tau`          DOUBLE(8, 2)                                NOT NULL,
  `num_seed`             INT(10) DEFAULT NULL,
  `num_full`             INT(10) DEFAULT NULL,
  `updated`              TIMESTAMP                                   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created`              DATETIME DEFAULT NULL,
  `version`              SMALLINT(5) DEFAULT NULL,
  `number_archs`         INT(8) DEFAULT NULL,
  `number_species`       INT(8) DEFAULT NULL,
  `number_structures`    INT(8) DEFAULT NULL,
  `number_rp75`          INT(8) DEFAULT NULL,
  `number_ncbi`          INT(8) DEFAULT NULL,
  `number_meta`          INT(8) DEFAULT NULL,
  `average_length`       DOUBLE(6, 2) DEFAULT NULL,
  `percentage_id`        INT(3) DEFAULT NULL,
  `average_coverage`     DOUBLE(6, 2) DEFAULT NULL,
  `change_status`        TINYTEXT,
  `seed_consensus`       TEXT,
  `full_consensus`       TEXT,
  `number_shuffled_hits` INT(10) DEFAULT NULL,
  `number_rp15`          INT(8) DEFAULT NULL,
  `number_rp35`          INT(8) DEFAULT NULL,
  `number_rp55`          INT(8) DEFAULT NULL,
  PRIMARY KEY (`auto_pfamA`),
  UNIQUE KEY `pfamA_acc` (`pfamA_acc`),
  UNIQUE KEY `pfamA_id` (`pfamA_id`)
)
  ENGINE =MyISAM
  AUTO_INCREMENT =15521
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
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
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamseq` (
  `auto_pfamseq`      INT(10)      NOT NULL AUTO_INCREMENT,
  `pfamseq_id`        VARCHAR(12)  NOT NULL,
  `pfamseq_acc`       VARCHAR(6)   NOT NULL,
  `seq_version`       TINYINT(4)   NOT NULL,
  `crc64`             VARCHAR(16)  NOT NULL,
  `md5`               VARCHAR(32)  NOT NULL,
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
  `rp15`              TINYINT(1) DEFAULT '0',
  `rp35`              TINYINT(1) DEFAULT '0',
  `rp55`              TINYINT(1) DEFAULT '0',
  `rp75`              TINYINT(1) DEFAULT '0',
  PRIMARY KEY (`auto_pfamseq`),
  UNIQUE KEY `pfamseq_acc` (`pfamseq_acc`),
  KEY `ncbi_taxid` (`ncbi_taxid`),
  KEY `crc64` (`crc64`),
  KEY `pfamseq_id` (`pfamseq_id`),
  KEY `pfamseq_architecture_idx` (`auto_architecture`),
  KEY `pfamseq_ncbi_code_idx` (`ncbi_taxid`, `genome_seq`),
  KEY `pfamseq_acc_version` (`pfamseq_acc`, `seq_version`),
  KEY `md5` (`md5`),
  KEY `pfamseq_tax_idx` (`taxonomy`(350))
)
  ENGINE =MyISAM
  AUTO_INCREMENT =25397992
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `accession_UNIQUE` (`accession`),
  UNIQUE KEY `accession` (`accession`)
)
  ENGINE =InnoDB
  AUTO_INCREMENT =4533512
  DEFAULT CHARSET =latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
CREATE TABLE `goTerm` (
  `id`   INT(10) UNSIGNED NOT NULL,
  `name` TINYTEXT         NOT NULL,
  PRIMARY KEY (`id`)
);
CREATE TABLE `pfamA_goTerm` (
  `pfamA_acc` VARCHAR(7) NOT NULL REFERENCES pfamA (pfamA_acc),
  `goTerm_id` INT(10)    NOT NULL REFERENCES goTerm (id),
  PRIMARY KEY (`pfamA_acc`, `goTerm_id`)
);
