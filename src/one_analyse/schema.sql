-- MySQL dump 10.13  Distrib 5.7.9, for Win32 (AMD64)
--
-- Host: localhost    Database: one_db
-- ------------------------------------------------------
-- Server version	5.7.11-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `period_records`
--

DROP TABLE IF EXISTS `period_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period_records` (
  `device` varchar(256) DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  `regular_buy` int(11) DEFAULT NULL,
  `rid` int(11) NOT NULL,
  `time` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `period_id` int(11) NOT NULL,
  PRIMARY KEY (`rid`,`user_id`,`period_id`),
  KEY `period_records_ibfk_uid_idx` (`user_id`),
  KEY `period_records_ibfk_pid_idx` (`period_id`),
  CONSTRAINT `period_records_ibfk_pid` FOREIGN KEY (`period_id`) REFERENCES `periods` (`period`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `period_records_ibfk_uid` FOREIGN KEY (`user_id`) REFERENCES `users` (`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `periods`
--

DROP TABLE IF EXISTS `periods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `periods` (
  `period` int(11) NOT NULL,
  `calc_time` datetime DEFAULT NULL,
  `cost` int(11) DEFAULT NULL,
  `duobao_time` datetime DEFAULT NULL,
  `lucky_code` int(11) DEFAULT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`period`),
  KEY `periods_ibfk_uid_idx` (`owner_id`),
  CONSTRAINT `periods_ibfk_uid` FOREIGN KEY (`owner_id`) REFERENCES `users` (`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `user_period_total_num`
--

DROP TABLE IF EXISTS `user_period_total_num`;
/*!50001 DROP VIEW IF EXISTS `user_period_total_num`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `user_period_total_num` AS SELECT 
 1 AS `total_num`,
 1 AS `regular_buy`,
 1 AS `time`,
 1 AS `user_id`,
 1 AS `period_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `cid` int(11) NOT NULL,
  `ip` varchar(128) DEFAULT NULL,
  `ip_address` varchar(128) DEFAULT NULL,
  `avatar_prefix` varchar(128) DEFAULT NULL,
  `bonus_num` int(11) DEFAULT NULL,
  `coin` int(11) DEFAULT NULL,
  `is_first_login` tinyint(1) DEFAULT NULL,
  `mobile` varchar(16) DEFAULT NULL,
  `nick_name` varchar(256) DEFAULT NULL,
  `uid` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `user_period_total_num`
--

/*!50001 DROP VIEW IF EXISTS `user_period_total_num`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`one`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `user_period_total_num` AS select sum(`period_records`.`num`) AS `total_num`,`period_records`.`regular_buy` AS `regular_buy`,`period_records`.`time` AS `time`,`period_records`.`user_id` AS `user_id`,`period_records`.`period_id` AS `period_id` from `period_records` group by `period_records`.`user_id`,`period_records`.`period_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-03 17:03:53
