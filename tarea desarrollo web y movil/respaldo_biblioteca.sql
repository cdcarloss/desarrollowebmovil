/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.20-11.8.9-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: biblioteca_db
-- ------------------------------------------------------
-- Server version	11.8.9-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add autor',7,'add_autor'),
(26,'Can change autor',7,'change_autor'),
(27,'Can delete autor',7,'delete_autor'),
(28,'Can view autor',7,'view_autor'),
(29,'Can add empleado',8,'add_empleado'),
(30,'Can change empleado',8,'change_empleado'),
(31,'Can delete empleado',8,'delete_empleado'),
(32,'Can view empleado',8,'view_empleado'),
(33,'Can add juego de mesa',9,'add_juegomesa'),
(34,'Can change juego de mesa',9,'change_juegomesa'),
(35,'Can delete juego de mesa',9,'delete_juegomesa'),
(36,'Can view juego de mesa',9,'view_juegomesa'),
(37,'Can add libro',10,'add_libro'),
(38,'Can change libro',10,'change_libro'),
(39,'Can delete libro',10,'delete_libro'),
(40,'Can view libro',10,'view_libro'),
(41,'Can add ebook',11,'add_libroebook'),
(42,'Can change ebook',11,'change_libroebook'),
(43,'Can delete ebook',11,'delete_libroebook'),
(44,'Can view ebook',11,'view_libroebook'),
(45,'Can add libro físico',12,'add_librofisico'),
(46,'Can change libro físico',12,'change_librofisico'),
(47,'Can delete libro físico',12,'delete_librofisico'),
(48,'Can view libro físico',12,'view_librofisico'),
(49,'Can add comentario',13,'add_comentario'),
(50,'Can change comentario',13,'change_comentario'),
(51,'Can delete comentario',13,'delete_comentario'),
(52,'Can view comentario',13,'view_comentario'),
(53,'Can add perfil',14,'add_perfil'),
(54,'Can change perfil',14,'change_perfil'),
(55,'Can delete perfil',14,'delete_perfil'),
(56,'Can view perfil',14,'view_perfil'),
(57,'Can add socio',15,'add_socio'),
(58,'Can change socio',15,'change_socio'),
(59,'Can delete socio',15,'delete_socio'),
(60,'Can view socio',15,'view_socio'),
(61,'Can add préstamo',16,'add_prestamo'),
(62,'Can change préstamo',16,'change_prestamo'),
(63,'Can delete préstamo',16,'delete_prestamo'),
(64,'Can view préstamo',16,'view_prestamo');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1000000$8TByyOaVyk38iOvSauJsKX$OxMaU6Kq6rr+X6owDlpjOb+/MTQQyR9agdkGMT8TBmc=',NULL,1,'admin','','','admin@bibliotecalarecamara.cl',1,1,'2026-09-22 09:13:11.251912'),
(2,'pbkdf2_sha256$1000000$NUvg4xymeKtxtP7PMT10t9$RvVArlPuph1xBWfBoW1cjY8xHDJcdYasRoOtkbxGkEs=',NULL,0,'lector','','','lector@bibliotecalarecamara.cl',0,1,'2026-09-22 09:13:11.762382'),
(3,'pbkdf2_sha256$1000000$FEQWv3UgbfbYDd6up5zbHS$ou/wbVZX9YqM+F45BJGwFqznY3If18DF/wD4kNUKF1I=',NULL,0,'sofia-martinez','Sofía','','sofia.martinez@example.com',0,1,'2026-09-22 09:13:12.588785'),
(4,'pbkdf2_sha256$1000000$83LWZxZfbUx1IlZLeN4PrR$z1Xp5f7VultLayKWiFHh/yNGWcAsvnMwwuNi96RBS9c=',NULL,0,'mateo-gonzalez','Mateo','','mateo.gonzalez@example.com',0,1,'2026-09-22 09:13:13.087128'),
(5,'pbkdf2_sha256$1000000$qHA5yaGlN5Ri4Mcou7NEnZ$nxxJdnB77GmDN27pAuTvUIfUiPh4Iqfl8y527ucpmag=',NULL,0,'valentina-rojas','Valentina','','valentina.rojas@example.com',0,1,'2026-09-22 09:13:13.600161'),
(6,'pbkdf2_sha256$1000000$e6YzGuHx9Q5xrwKapwuEAi$0exgbLx4u/9rXJl8yUYR4jWGViEsdlYL02d2TX5A/fQ=',NULL,0,'diego-fuentes','Diego','','diego.fuentes@example.com',0,1,'2026-09-22 09:13:14.113790'),
(7,'pbkdf2_sha256$1000000$kaMsC7cxTYmaGuUwX1wnkT$+f4D5mhPbybNPgskCL8kC0C7OhRybaW1of7VDRvnOIc=',NULL,0,'camila-torres','Camila','','camila.torres@example.com',0,1,'2026-09-22 09:13:14.636428');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_autor`
--

DROP TABLE IF EXISTS `biblioteca_autor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_autor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `nacionalidad` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_autor`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_autor` WRITE;
/*!40000 ALTER TABLE `biblioteca_autor` DISABLE KEYS */;
INSERT INTO `biblioteca_autor` VALUES
(1,'Gabriel García Márquez','Colombia'),
(2,'Isabel Allende','Chile'),
(3,'Julio Cortázar','Argentina'),
(4,'Jane Austen','Reino Unido'),
(5,'George Orwell','Reino Unido'),
(6,'Roberto Bolaño','Chile');
/*!40000 ALTER TABLE `biblioteca_autor` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_comentario`
--

DROP TABLE IF EXISTS `biblioteca_comentario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_comentario` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `texto` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `libro_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `biblioteca_comentario_usuario_id_18cd299d_fk_auth_user_id` (`usuario_id`),
  KEY `biblioteca_comentario_libro_id_5e69f885_fk_biblioteca_libro_id` (`libro_id`),
  CONSTRAINT `biblioteca_comentario_libro_id_5e69f885_fk_biblioteca_libro_id` FOREIGN KEY (`libro_id`) REFERENCES `biblioteca_libro` (`id`),
  CONSTRAINT `biblioteca_comentario_usuario_id_18cd299d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_comentario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_comentario` WRITE;
/*!40000 ALTER TABLE `biblioteca_comentario` DISABLE KEYS */;
INSERT INTO `biblioteca_comentario` VALUES
(1,'Una relectura obligada. Cada vez encuentro algo nuevo en Macondo.','2026-09-22 09:13:15.262152',3,1),
(2,'Al principio cuesta seguir a toda la familia Buendía, pero vale la pena.','2026-09-22 09:13:15.266971',4,1),
(3,'Inquietante y todavía muy vigente. Lo terminé en dos días.','2026-09-22 09:13:15.271349',5,6),
(4,'Bolaño construye personajes que se sienten reales. Muy recomendado.','2026-09-22 09:13:15.276482',6,8),
(5,'Elizabeth Bennet es uno de mis personajes favoritos de la literatura.','2026-09-22 09:13:15.284528',7,5);
/*!40000 ALTER TABLE `biblioteca_comentario` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_empleado`
--

DROP TABLE IF EXISTS `biblioteca_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_empleado` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `correo` varchar(254) NOT NULL,
  `cargo` varchar(20) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_empleado`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_empleado` WRITE;
/*!40000 ALTER TABLE `biblioteca_empleado` DISABLE KEYS */;
INSERT INTO `biblioteca_empleado` VALUES
(1,'Andrea Silva','andrea.silva@bibliotecalarecamara.cl','ADMINISTRADOR',1),
(2,'Felipe Muñoz','felipe.munoz@bibliotecalarecamara.cl','BIBLIOTECARIO',1),
(3,'Javiera Pérez','javiera.perez@bibliotecalarecamara.cl','ASISTENTE',1);
/*!40000 ALTER TABLE `biblioteca_empleado` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_juegomesa`
--

DROP TABLE IF EXISTS `biblioteca_juegomesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_juegomesa` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `stock` int(10) unsigned NOT NULL CHECK (`stock` >= 0),
  `imagen` varchar(100) DEFAULT NULL,
  `nombre` varchar(120) NOT NULL,
  `marca` varchar(80) NOT NULL,
  `categoria` varchar(12) NOT NULL,
  `jugadores_min` smallint(5) unsigned NOT NULL CHECK (`jugadores_min` >= 0),
  `jugadores_max` smallint(5) unsigned NOT NULL CHECK (`jugadores_max` >= 0),
  `edad_minima` smallint(5) unsigned NOT NULL CHECK (`edad_minima` >= 0),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_juegomesa`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_juegomesa` WRITE;
/*!40000 ALTER TABLE `biblioteca_juegomesa` DISABLE KEYS */;
INSERT INTO `biblioteca_juegomesa` VALUES
(1,1,'portadas/juegos/catan_NG69o1V.jpg','Catan','Devir','ESTRATEGIA',3,4,10),
(2,2,'portadas/juegos/carcassonne_JE4he70.jpg','Carcassonne','Devir','FAMILIAR',2,5,7),
(3,0,'portadas/juegos/dixit_BwjVBwn.jpg','Dixit','Libellud','PARTY',3,6,8),
(4,2,'portadas/juegos/catan-los-colonos-junior_Xv3zx9r.jpg','Catan: Los Colonos Junior','Devir','INFANTIL',2,4,6),
(5,1,'portadas/juegos/azul_edQ2yYJ.jpg','Azul','Next Move Games','ESTRATEGIA',2,4,8);
/*!40000 ALTER TABLE `biblioteca_juegomesa` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_libro`
--

DROP TABLE IF EXISTS `biblioteca_libro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_libro` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `stock` int(10) unsigned NOT NULL CHECK (`stock` >= 0),
  `imagen` varchar(100) DEFAULT NULL,
  `titulo` varchar(180) NOT NULL,
  `isbn` varchar(17) NOT NULL,
  `anio_publicacion` int(10) unsigned NOT NULL CHECK (`anio_publicacion` >= 0),
  `tipo` varchar(10) NOT NULL,
  `autor_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`),
  KEY `biblioteca_libro_autor_id_c1df5079_fk_biblioteca_autor_id` (`autor_id`),
  CONSTRAINT `biblioteca_libro_autor_id_c1df5079_fk_biblioteca_autor_id` FOREIGN KEY (`autor_id`) REFERENCES `biblioteca_autor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_libro`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_libro` WRITE;
/*!40000 ALTER TABLE `biblioteca_libro` DISABLE KEYS */;
INSERT INTO `biblioteca_libro` VALUES
(1,2,'portadas/libros/cien-anos-de-soledad_5JJJusH.jpg','Cien años de soledad','9780307474728',1967,'FISICO',1),
(2,2,'portadas/libros/el-amor-en-los-tiempos-del-colera_1VF0fpV.jpg','El amor en los tiempos del cólera','9780307389732',1985,'FISICO',1),
(3,1,'portadas/libros/la-casa-de-los-espiritus_tfKOjEh.jpg','La casa de los espíritus','9781501117015',1982,'FISICO',2),
(4,1,'portadas/libros/rayuela_MPZmgSc.jpg','Rayuela','9788437604572',1963,'FISICO',3),
(5,4,'portadas/libros/orgullo-y-prejuicio_tdp6pcl.jpg','Orgullo y prejuicio','9780141439518',1813,'FISICO',4),
(6,4,'portadas/libros/1984_8tsL8cN.jpg','1984','9780451524935',1949,'FISICO',5),
(7,2,'portadas/libros/rebelion-en-la-granja_wBZMdPy.jpg','Rebelión en la granja','9780451526342',1945,'FISICO',5),
(8,0,'portadas/libros/los-detectives-salvajes_sHjRORl.jpg','Los detectives salvajes','9788433974787',1998,'FISICO',6),
(9,98,'portadas/libros/cien-anos-de-soledad-ebook_MhshErz.jpg','Cien años de soledad (ebook)','9780307474711',1967,'EBOOK',1),
(10,99,'portadas/libros/paula_UyenXfz.jpg','Paula','9780061564253',1994,'EBOOK',2),
(11,98,'portadas/libros/bestiario_eUTSlcx.jpg','Bestiario','9788420633121',1951,'EBOOK',3),
(12,99,'portadas/libros/emma_2OCXbS2.jpg','Emma','9780141439587',1815,'EBOOK',4),
(13,99,'portadas/libros/rayuela-ebook_lMbzGOf.jpg','Rayuela (ebook)','9990000004',1963,'EBOOK',3),
(14,99,'portadas/libros/rebelion-en-la-granja-ebook_oLMChJD.jpg','Rebelión en la granja (ebook)','9990000007',1945,'EBOOK',5);
/*!40000 ALTER TABLE `biblioteca_libro` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_libroebook`
--

DROP TABLE IF EXISTS `biblioteca_libroebook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_libroebook` (
  `libro_ptr_id` bigint(20) NOT NULL,
  `formato_archivo` varchar(10) NOT NULL,
  `tamano_mb` int(10) unsigned NOT NULL CHECK (`tamano_mb` >= 0),
  PRIMARY KEY (`libro_ptr_id`),
  CONSTRAINT `biblioteca_libroeboo_libro_ptr_id_6eceb2e7_fk_bibliotec` FOREIGN KEY (`libro_ptr_id`) REFERENCES `biblioteca_libro` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_libroebook`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_libroebook` WRITE;
/*!40000 ALTER TABLE `biblioteca_libroebook` DISABLE KEYS */;
INSERT INTO `biblioteca_libroebook` VALUES
(9,'EPUB',3),
(10,'EPUB',2),
(11,'PDF',4),
(12,'MOBI',3),
(13,'EPUB',5),
(14,'EPUB',5);
/*!40000 ALTER TABLE `biblioteca_libroebook` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_librofisico`
--

DROP TABLE IF EXISTS `biblioteca_librofisico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_librofisico` (
  `libro_ptr_id` bigint(20) NOT NULL,
  `ubicacion` varchar(40) NOT NULL,
  PRIMARY KEY (`libro_ptr_id`),
  CONSTRAINT `biblioteca_librofisi_libro_ptr_id_2baf2355_fk_bibliotec` FOREIGN KEY (`libro_ptr_id`) REFERENCES `biblioteca_libro` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_librofisico`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_librofisico` WRITE;
/*!40000 ALTER TABLE `biblioteca_librofisico` DISABLE KEYS */;
INSERT INTO `biblioteca_librofisico` VALUES
(1,'Estante A-01'),
(2,'Estante A-02'),
(3,'Estante A-03'),
(4,'Estante B-01'),
(5,'Estante C-01'),
(6,'Estante D-01'),
(7,'Estante D-02'),
(8,'Estante B-02');
/*!40000 ALTER TABLE `biblioteca_librofisico` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_perfil`
--

DROP TABLE IF EXISTS `biblioteca_perfil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_perfil` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `foto` varchar(100) DEFAULT NULL,
  `descripcion` varchar(280) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `biblioteca_perfil_usuario_id_907216f4_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_perfil`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_perfil` WRITE;
/*!40000 ALTER TABLE `biblioteca_perfil` DISABLE KEYS */;
INSERT INTO `biblioteca_perfil` VALUES
(1,'','Administra el catálogo, los socios y los préstamos de la biblioteca.',1),
(2,'','Cuenta de prueba genérica (sin socio vinculado).',2),
(3,'','',3),
(4,'','',4),
(5,'','',5),
(6,'','',6),
(7,'','',7);
/*!40000 ALTER TABLE `biblioteca_perfil` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_prestamo`
--

DROP TABLE IF EXISTS `biblioteca_prestamo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_prestamo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_prestamo` date NOT NULL,
  `fecha_devolucion_prevista` date NOT NULL,
  `fecha_devolucion_real` date DEFAULT NULL,
  `devuelto` tinyint(1) NOT NULL,
  `empleado_id` bigint(20) DEFAULT NULL,
  `juego_id` bigint(20) DEFAULT NULL,
  `libro_id` bigint(20) DEFAULT NULL,
  `socio_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `biblioteca_prestamo_empleado_id_434a8a04_fk_bibliotec` (`empleado_id`),
  KEY `biblioteca_prestamo_juego_id_c62b4483_fk_biblioteca_juegomesa_id` (`juego_id`),
  KEY `biblioteca_prestamo_libro_id_c71c231b_fk_biblioteca_libro_id` (`libro_id`),
  KEY `biblioteca_prestamo_socio_id_4aa743ea_fk_biblioteca_socio_id` (`socio_id`),
  CONSTRAINT `biblioteca_prestamo_empleado_id_434a8a04_fk_bibliotec` FOREIGN KEY (`empleado_id`) REFERENCES `biblioteca_empleado` (`id`),
  CONSTRAINT `biblioteca_prestamo_juego_id_c62b4483_fk_biblioteca_juegomesa_id` FOREIGN KEY (`juego_id`) REFERENCES `biblioteca_juegomesa` (`id`),
  CONSTRAINT `biblioteca_prestamo_libro_id_c71c231b_fk_biblioteca_libro_id` FOREIGN KEY (`libro_id`) REFERENCES `biblioteca_libro` (`id`),
  CONSTRAINT `biblioteca_prestamo_socio_id_4aa743ea_fk_biblioteca_socio_id` FOREIGN KEY (`socio_id`) REFERENCES `biblioteca_socio` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_prestamo`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_prestamo` WRITE;
/*!40000 ALTER TABLE `biblioteca_prestamo` DISABLE KEYS */;
INSERT INTO `biblioteca_prestamo` VALUES
(1,'2026-09-22','2026-10-06',NULL,0,2,NULL,1,1),
(2,'2026-09-22','2026-10-06',NULL,0,2,NULL,3,2),
(3,'2026-09-22','2026-10-06',NULL,0,3,NULL,6,3),
(4,'2026-09-22','2026-10-06',NULL,0,1,NULL,8,4),
(5,'2026-09-22','2026-09-29',NULL,0,NULL,NULL,9,5),
(6,'2026-09-22','2026-09-29',NULL,0,NULL,NULL,11,1),
(7,'2026-09-22','2026-10-02',NULL,0,2,1,NULL,2),
(8,'2026-09-22','2026-10-02',NULL,0,NULL,3,NULL,3),
(9,'2026-09-22','2026-10-06','2026-09-22',1,3,NULL,5,4),
(10,'2026-09-02','2026-09-16',NULL,0,1,NULL,7,5);
/*!40000 ALTER TABLE `biblioteca_prestamo` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `biblioteca_socio`
--

DROP TABLE IF EXISTS `biblioteca_socio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `biblioteca_socio` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `correo` varchar(254) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `fecha_registro` date NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `biblioteca_socio_usuario_id_dfcf987e_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biblioteca_socio`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `biblioteca_socio` WRITE;
/*!40000 ALTER TABLE `biblioteca_socio` DISABLE KEYS */;
INSERT INTO `biblioteca_socio` VALUES
(1,'Sofía Martínez','sofia.martinez@example.com','+56911112222','2026-09-22',3),
(2,'Mateo González','mateo.gonzalez@example.com','+56922223333','2026-09-22',4),
(3,'Valentina Rojas','valentina.rojas@example.com','+56933334444','2026-09-22',5),
(4,'Diego Fuentes','diego.fuentes@example.com','+56944445555','2026-09-22',6),
(5,'Camila Torres','camila.torres@example.com','+56955556666','2026-09-22',7);
/*!40000 ALTER TABLE `biblioteca_socio` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(7,'biblioteca','autor'),
(13,'biblioteca','comentario'),
(8,'biblioteca','empleado'),
(9,'biblioteca','juegomesa'),
(10,'biblioteca','libro'),
(11,'biblioteca','libroebook'),
(12,'biblioteca','librofisico'),
(14,'biblioteca','perfil'),
(16,'biblioteca','prestamo'),
(15,'biblioteca','socio'),
(5,'contenttypes','contenttype'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-09-22 09:13:06.921529'),
(2,'auth','0001_initial','2026-09-22 09:13:07.922363'),
(3,'admin','0001_initial','2026-09-22 09:13:08.140034'),
(4,'admin','0002_logentry_remove_auto_add','2026-09-22 09:13:08.155555'),
(5,'admin','0003_logentry_add_action_flag_choices','2026-09-22 09:13:08.174618'),
(6,'contenttypes','0002_remove_content_type_name','2026-09-22 09:13:08.343796'),
(7,'auth','0002_alter_permission_name_max_length','2026-09-22 09:13:08.429055'),
(8,'auth','0003_alter_user_email_max_length','2026-09-22 09:13:08.495022'),
(9,'auth','0004_alter_user_username_opts','2026-09-22 09:13:08.508931'),
(10,'auth','0005_alter_user_last_login_null','2026-09-22 09:13:08.590055'),
(11,'auth','0006_require_contenttypes_0002','2026-09-22 09:13:08.593041'),
(12,'auth','0007_alter_validators_add_error_messages','2026-09-22 09:13:08.607174'),
(13,'auth','0008_alter_user_username_max_length','2026-09-22 09:13:08.660879'),
(14,'auth','0009_alter_user_last_name_max_length','2026-09-22 09:13:08.710930'),
(15,'auth','0010_alter_group_name_max_length','2026-09-22 09:13:08.765941'),
(16,'auth','0011_update_proxy_permissions','2026-09-22 09:13:08.774912'),
(17,'auth','0012_alter_user_first_name_max_length','2026-09-22 09:13:08.820949'),
(18,'biblioteca','0001_initial','2026-09-22 09:13:10.087935'),
(19,'biblioteca','0002_alter_libroebook_options_alter_librofisico_options_and_more','2026-09-22 09:13:10.108859'),
(20,'sessions','0001_initial','2026-09-22 09:13:10.199054');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES
('l4pmig3s59v4jen3tw19kydzigco1baj','eyJjYXJyaXRvIjp7fX0:1x8wZ4:ga2HuXQrf2vG9bUFyD7B8J0o_msW6zRiOIm1nU6kzgY','2026-10-06 09:13:26.004572');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-09-22  9:14:21
