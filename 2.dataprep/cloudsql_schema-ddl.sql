-- MySQL dump 10.17  Distrib 10.3.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 10.139.16.14    Database: 
-- ------------------------------------------------------
-- Server version	8.0.18-google

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Retail`
--

-- CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Retail` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `Retail`;

--
-- Table structure for table `category_lookup`
--

DROP TABLE IF EXISTS `category_lookup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category_lookup` (
  `item_code` int(11) DEFAULT NULL,
  `category` varchar(60) DEFAULT NULL,
  `category_code` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `channels`
--

DROP TABLE IF EXISTS `channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channels` (
  `ID` int(11) DEFAULT NULL,
  `NAME` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `id` int(11) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(70) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `zip` varchar(50) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `traffic_source` varchar(50) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `ID` int(11) DEFAULT NULL,
  `SEQUENCE_NUMBER` int(11) DEFAULT NULL,
  `SESSION_ID` varchar(100) DEFAULT NULL,
  `IP_ADDRESS` varchar(100) DEFAULT NULL,
  `CITY` varchar(60) DEFAULT NULL,
  `STATE` varchar(60) DEFAULT NULL,
  `COUNTRY` varchar(70) DEFAULT NULL,
  `ZIP` varchar(30) DEFAULT NULL,
  `LATITUDE` float DEFAULT NULL,
  `LONGITUDE` float DEFAULT NULL,
  `OS` varchar(20) DEFAULT NULL,
  `BROWSER` varchar(20) DEFAULT NULL,
  `TRAFFIC_SOURCE` varchar(40) DEFAULT NULL,
  `USER_ID` int(11) DEFAULT NULL,
  `URI` varchar(150) DEFAULT NULL,
  `EVENT_TYPE` varchar(50) DEFAULT NULL,
  `CREATED_AT` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory_items`
--

DROP TABLE IF EXISTS `inventory_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_items` (
  `ID` int(11) DEFAULT NULL,
  `PRODUCT_ID` int(11) DEFAULT NULL,
  `COST` float DEFAULT NULL,
  `PRODUCT_CATEGORY` varchar(100) DEFAULT NULL,
  `PRODUCT_NAME` varchar(255) DEFAULT NULL,
  `PRODUCT_BRAND` varchar(120) DEFAULT NULL,
  `PRODUCT_RETAIL_PRICE` float DEFAULT NULL,
  `PRODUCT_DEPARTMENT` varchar(60) DEFAULT NULL,
  `PRODUCT_SKU` varchar(60) DEFAULT NULL,
  `PRODUCT_DISTRIBUTION_CENTER_ID` int(11) DEFAULT NULL,
  `CREATED_AT` timestamp NULL DEFAULT NULL,
  `SOLD_AT` timestamp NULL DEFAULT NULL,
  KEY `idx_id` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_items` (
  `ID` int(11) DEFAULT NULL,
  `ORDER_ID` int(11) DEFAULT NULL,
  `USER_ID` int(11) DEFAULT NULL,
  `INVENTORY_ITEM_ID` int(11) DEFAULT NULL,
  `SALE_PRICE` float DEFAULT NULL,
  `STATUS` varchar(20) DEFAULT NULL,
  `CREATED_AT` timestamp NULL DEFAULT NULL,
  `RETURNED_AT` timestamp NULL DEFAULT NULL,
  `SHIPPED_AT` timestamp NULL DEFAULT NULL,
  `DELIVERED_AT` timestamp NULL DEFAULT NULL,
  KEY `idx_id` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `ID` int(11) NOT NULL,
  `COST` float DEFAULT NULL,
  `DEPARTMENT` varchar(60) DEFAULT NULL,
  `CATEGORY` varchar(100) DEFAULT NULL,
  `SUB_CATEGORY` varchar(100) DEFAULT NULL,
  `NAME` varchar(255) DEFAULT NULL,
  `BRAND` varchar(50) DEFAULT NULL,
  `RETAIL_PRICE` float DEFAULT NULL,
  `SKU` varchar(100) DEFAULT NULL,
  `DISTRIBUTION_CENTER_ID` int(11) DEFAULT NULL,
  `IMAGE_LINK` varchar(255) DEFAULT NULL,
  `SIZE` varchar(10) DEFAULT NULL,
  `COLOR` varchar(50) DEFAULT NULL,
  `CURRENCY_CODE` varchar(50) DEFAULT NULL,
  `ESTIMATED_DELIVERY_DAY` int(11) DEFAULT NULL,
  `AVAILABILITY` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review` (
  `id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `review` varchar(255) DEFAULT NULL,
  `star_rating` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `transaction_detail1`
--

DROP TABLE IF EXISTS `transaction_detail1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_detail1` (
  `transaction_timestamp` timestamp NULL DEFAULT NULL,
  `transaction_id` int(11) NOT NULL,
  `store_id` int(11) DEFAULT NULL,
  `channel_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transaction_detail2`
--

DROP TABLE IF EXISTS `transaction_detail2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_detail2` (
  `transaction_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `sale_price` float DEFAULT NULL,
  `gross_margin` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `us_stores`
--

DROP TABLE IF EXISTS `us_stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `us_stores` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `sq_ft` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `row_num` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(60) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `city` varchar(60) DEFAULT NULL,
  `state` varchar(60) DEFAULT NULL,
  `country` varchar(60) DEFAULT NULL,
  `zip` varchar(20) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `traffic_source` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
