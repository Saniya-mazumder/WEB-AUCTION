-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: auction_system
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auction_items`
--

DROP TABLE IF EXISTS `auction_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auction_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `address` text NOT NULL,
  `phone` varchar(15) NOT NULL,
  `duration` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'active',
  `highest_bidder_id` int DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `seller_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auction_items`
--

LOCK TABLES `auction_items` WRITE;
/*!40000 ALTER TABLE `auction_items` DISABLE KEYS */;
INSERT INTO `auction_items` VALUES (1,'Vase',1,132432.00,'Vellore','8240000000',2,'2025-03-27 18:13:50','active',NULL,'2025-04-05 08:42:21',NULL),(3,'vase',1,400000.00,'Vellore','8240000000',2,'2025-04-01 16:21:26','active',NULL,'2025-04-05 08:42:21',NULL),(6,'vase',1,2.00,'Vellore','8240000000',2,'2025-04-01 16:46:04','active',NULL,'2025-04-05 08:42:21',NULL),(7,'Chain',1,230000.00,'Chennai','8342233445',2,'2025-04-01 17:04:12','active',NULL,'2025-04-05 08:42:21',NULL),(8,'Ring',2,1000000.00,'Kolkata','8989765432',1,'2025-04-01 18:03:17','active',NULL,'2025-04-05 08:42:21',NULL),(9,'Camera',1,100000.00,'Hyderabad','8240000000',2,'2025-04-02 15:04:48','active',NULL,'2025-04-05 08:42:21',NULL),(10,'Laptop',1,200000.00,'Hyderabad','8240000000',1,'2025-04-03 02:44:01','active',NULL,'2025-04-05 08:42:21',NULL),(11,'Pencil',2,300000.00,'Moon','9876543210',2,'2025-04-05 09:15:10','active',NULL,'2025-04-05 09:15:10',2);
/*!40000 ALTER TABLE `auction_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_requests`
--

DROP TABLE IF EXISTS `purchase_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `buyer_id` int NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `buyer_id` (`buyer_id`),
  CONSTRAINT `purchase_requests_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `auction_items` (`id`),
  CONSTRAINT `purchase_requests_ibfk_2` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_requests`
--

LOCK TABLES `purchase_requests` WRITE;
/*!40000 ALTER TABLE `purchase_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` enum('buyer','seller') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'saniya_mazumder','$2b$12$z1FGILf30yWlHS4DeiYZBu8bqnCMdd9vjIfbj8u4o8Sm5OCXzmxyC','buyer'),(2,'Taniya','$2b$12$DkqF4RKL.tm1JnnPakAuieFJFNGlegRZZTyiDt3Mep8NB4LFIqyMS','seller'),(4,'saniya','$2b$12$EQh/s/9EKDFcwm5wUvyyYe3P4dUcjh1JBs.2UgVHvpJaV5Y8xcTMW','seller');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-06 11:39:39
