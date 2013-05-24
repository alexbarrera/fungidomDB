/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `architecture` (
  `auto_architecture` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `architecture` text,
  `type_example` int(10) NOT NULL DEFAULT '0',
  `no_seqs` int(8) NOT NULL DEFAULT '0',
  `architecture_acc` text,
  PRIMARY KEY (`auto_architecture`),
  KEY `architecture_type_example_idx` (`type_example`),
  KEY `architecture_architecture_idx` (`architecture`(255)),
  KEY `architecture_architecture_acc_idx` (`architecture_acc`(255))
) ENGINE=MyISAM AUTO_INCREMENT=325028 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamA` (
  `auto_pfamA` int(5) NOT NULL AUTO_INCREMENT,
  `pfamA_acc` varchar(7) NOT NULL,
  `pfamA_id` varchar(16) NOT NULL,
  `previous_id` tinytext,
  `description` varchar(100) NOT NULL,
  `author` tinytext NOT NULL,
  `deposited_by` varchar(100) NOT NULL DEFAULT 'anon',
  `seed_source` tinytext NOT NULL,
  `type` enum('Family','Domain','Repeat','Motif') NOT NULL,
  `comment` longtext,
  `sequence_GA` double(8,2) NOT NULL,
  `domain_GA` double(8,2) NOT NULL,
  `sequence_TC` double(8,2) NOT NULL,
  `domain_TC` double(8,2) NOT NULL,
  `sequence_NC` double(8,2) NOT NULL,
  `domain_NC` double(8,2) NOT NULL,
  `buildMethod` tinytext NOT NULL,
  `model_length` mediumint(8) NOT NULL,
  `searchMethod` tinytext NOT NULL,
  `msv_lambda` double(8,2) NOT NULL,
  `msv_mu` double(8,2) NOT NULL,
  `viterbi_lambda` double(8,2) NOT NULL,
  `viterbi_mu` double(8,2) NOT NULL,
  `forward_lambda` double(8,2) NOT NULL,
  `forward_tau` double(8,2) NOT NULL,
  `num_seed` int(10) DEFAULT NULL,
  `num_full` int(10) DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created` datetime DEFAULT NULL,
  `version` smallint(5) DEFAULT NULL,
  `number_archs` int(8) DEFAULT NULL,
  `number_species` int(8) DEFAULT NULL,
  `number_structures` int(8) DEFAULT NULL,
  `number_rp75` int(8) DEFAULT NULL,
  `number_ncbi` int(8) DEFAULT NULL,
  `number_meta` int(8) DEFAULT NULL,
  `average_length` double(6,2) DEFAULT NULL,
  `percentage_id` int(3) DEFAULT NULL,
  `average_coverage` double(6,2) DEFAULT NULL,
  `change_status` tinytext,
  `seed_consensus` text,
  `full_consensus` text,
  `number_shuffled_hits` int(10) DEFAULT NULL,
  `number_rp15` int(8) DEFAULT NULL,
  `number_rp35` int(8) DEFAULT NULL,
  `number_rp55` int(8) DEFAULT NULL,
  PRIMARY KEY (`auto_pfamA`),
  UNIQUE KEY `pfamA_acc` (`pfamA_acc`),
  UNIQUE KEY `pfamA_id` (`pfamA_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15521 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamA_architecture` (
  `auto_pfamA` int(5) NOT NULL DEFAULT '0',
  `auto_architecture` int(10) unsigned NOT NULL DEFAULT '0',
  KEY `auto_pfamA` (`auto_pfamA`),
  KEY `auto_architecture` (`auto_architecture`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pfamseq` (
  `auto_pfamseq` int(10) NOT NULL AUTO_INCREMENT,
  `pfamseq_id` varchar(12) NOT NULL,
  `pfamseq_acc` varchar(6) NOT NULL,
  `seq_version` tinyint(4) NOT NULL,
  `crc64` varchar(16) NOT NULL,
  `md5` varchar(32) NOT NULL,
  `description` text NOT NULL,
  `evidence` tinyint(4) NOT NULL,
  `length` mediumint(8) NOT NULL DEFAULT '0',
  `species` text NOT NULL,
  `taxonomy` mediumtext,
  `is_fragment` tinyint(1) DEFAULT NULL,
  `sequence` blob NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created` datetime DEFAULT NULL,
  `ncbi_taxid` int(10) unsigned DEFAULT '0',
  `genome_seq` tinyint(1) DEFAULT '0',
  `auto_architecture` int(10) DEFAULT NULL,
  `treefam_acc` varchar(8) DEFAULT NULL,
  `rp15` tinyint(1) DEFAULT '0',
  `rp35` tinyint(1) DEFAULT '0',
  `rp55` tinyint(1) DEFAULT '0',
  `rp75` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`auto_pfamseq`),
  UNIQUE KEY `pfamseq_acc` (`pfamseq_acc`),
  KEY `ncbi_taxid` (`ncbi_taxid`),
  KEY `crc64` (`crc64`),
  KEY `pfamseq_id` (`pfamseq_id`),
  KEY `pfamseq_architecture_idx` (`auto_architecture`),
  KEY `pfamseq_ncbi_code_idx` (`ncbi_taxid`,`genome_seq`),
  KEY `pfamseq_acc_version` (`pfamseq_acc`,`seq_version`),
  KEY `md5` (`md5`),
  KEY `pfamseq_tax_idx` (`taxonomy`(350))
) ENGINE=MyISAM AUTO_INCREMENT=25397992 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `protein` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accession` varchar(45) NOT NULL,
  `length` int(11) DEFAULT '0',
  `source` varchar(8) DEFAULT NULL,
  `processed` int(11) DEFAULT '0',
  `signalp` varchar(16) DEFAULT NULL,
  `full_name` varchar(256) DEFAULT NULL,
  `EC` varchar(16) DEFAULT NULL,
  `Transmembrane` varchar(16) DEFAULT NULL,
  `Subcellular_location_CC` varchar(100) DEFAULT NULL,
  `Membrane` varchar(16) DEFAULT NULL,
  `Cell_wall` varchar(16) DEFAULT NULL,
  `Cell_wall_biogenesis_degradation` varchar(16) DEFAULT NULL,
  `specie` varchar(128) DEFAULT NULL,
  `taxonomy` mediumtext,
  `gene_name` varchar(32) DEFAULT NULL,
  `pdb` varchar(8) DEFAULT NULL,
  `ensembl_fungi_transcript_id` varchar(32) DEFAULT NULL,
  `supFam` varchar(32) DEFAULT NULL,
  `taxID` int(10) DEFAULT NULL,
  `specie_short` varchar(8) DEFAULT NULL,
  `human_homolog` int(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `accession_UNIQUE` (`accession`),
  UNIQUE KEY `accession` (`accession`)
) ENGINE=InnoDB AUTO_INCREMENT=4533512 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
