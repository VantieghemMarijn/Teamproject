-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: clients
-- ------------------------------------------------------
-- Server version	5.7.28-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activeclients`
--

DROP TABLE IF EXISTS `activeclients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activeclients` (
  `idactiveclients` int(11) NOT NULL AUTO_INCREMENT,
  `clientname` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idactiveclients`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activeclients`
--

LOCK TABLES `activeclients` WRITE;
/*!40000 ALTER TABLE `activeclients` DISABLE KEYS */;
INSERT INTO `activeclients` VALUES (16,'marijn'),(17,'marijn');
/*!40000 ALTER TABLE `activeclients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientlist`
--

DROP TABLE IF EXISTS `clientlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientlist` (
  `clientid` int(11) NOT NULL AUTO_INCREMENT,
  `clientname` varchar(45) NOT NULL,
  `clientnick` varchar(45) NOT NULL,
  `clientemail` varchar(45) NOT NULL,
  PRIMARY KEY (`clientid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientlist`
--

LOCK TABLES `clientlist` WRITE;
/*!40000 ALTER TABLE `clientlist` DISABLE KEYS */;
INSERT INTO `clientlist` VALUES (20,'marijn','test','sdfsd'),(21,'marijn','test','marijn');
/*!40000 ALTER TABLE `clientlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `querylog`
--

DROP TABLE IF EXISTS `querylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `querylog` (
  `querylogid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `queryname` varchar(45) NOT NULL,
  `queryparam` varchar(45) NOT NULL,
  PRIMARY KEY (`querylogid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `querylog`
--

LOCK TABLES `querylog` WRITE;
/*!40000 ALTER TABLE `querylog` DISABLE KEYS */;
INSERT INTO `querylog` VALUES (1,'marijn','q0',''),(2,'marijn','q1',''),(3,'wout','q3',''),(4,'klaas','q2',''),(5,'wout','q3','');
/*!40000 ALTER TABLE `querylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'clients'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-10 20:54:19
