-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
-- Host: mysql
-- Generation Time: Feb 09, 2025 at 05:42 PM
-- Server version: 9.2.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: clinic
--

-- --------------------------------------------------------

--
-- Table structure for table `allergies`
--
CREATE TABLE `allergies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `allergies` text COLLATE utf8mb4_general_ci NOT NULL,
  `idClinicHistory` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idClinicHistory` (`idClinicHistory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attention`
--
CREATE TABLE `attention` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL,
  `weight` decimal(6,2) DEFAULT NULL,                   
  `height` decimal(5,2) DEFAULT NULL,                   
  `temperature` decimal(4,1) DEFAULT NULL,              
  `bloodPressure` int DEFAULT NULL,                    
  `heartRate` int DEFAULT NULL,
  `oxygenSaturation` int DEFAULT NULL,
  `breathingFrequency` int DEFAULT NULL,
  `glucose` decimal(5,1) DEFAULT NULL,                  
  `hemoglobin` decimal(4,1) DEFAULT NULL,               
  `reasonConsultation` varchar(255) NOT NULL,
  `currentIllness` varchar(255) NOT NULL,
  `evolution` varchar(255) NOT NULL,
  `idClinicHistory` int NOT NULL,
  `idDoctor` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idClinicHistory` (`idClinicHistory`),
  KEY `idDoctor` (`idDoctor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `credentials`
--
CREATE TABLE `credentials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifierCode` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `identifierCode` (`identifierCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `diagnostic`
--
CREATE TABLE `diagnostic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cie10Code` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `disease` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `observations` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `diagnosticCondition` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `chronology` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--
CREATE TABLE `doctor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifierCode` varchar(255) NOT NULL UNIQUE,
  `firstName` varchar(255) NOT NULL,
  `middleName` varchar(255) NOT NULL,
  `lastName1` varchar(255) NOT NULL,
  `lastName2` varchar(255) NOT NULL,
  `phoneNumber` varchar(255) NOT NULL,
  `address` mediumtext NOT NULL,
  `gender` enum('Masculino','Femenino','No Binario','Otro','Prefiero no decir') NOT NULL,
  `sex` enum('Masculino','Femenino','Prefiero no decir') NOT NULL,
  `speciality` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `emergencyContact`
--
CREATE TABLE `emergencyContact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `lastName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `address` text COLLATE utf8mb4_general_ci NOT NULL,
  `relationship` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phoneNumber1` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phoneNumber2` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `idClinicHistory` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idClinicHistory` (`idClinicHistory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `familyBackground`
--
CREATE TABLE `familyBackground` (
  `id` int NOT NULL AUTO_INCREMENT,
  `familyBackground` text COLLATE utf8mb4_general_ci NOT NULL,
  `time` date NOT NULL,
  `degreeRelationship` enum('1','2','3','4') COLLATE utf8mb4_general_ci NOT NULL,
  `idClinicHistory` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idClinicHistory` (`idClinicHistory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `histopathology`
--
CREATE TABLE `histopathology` (
  `id` int NOT NULL AUTO_INCREMENT,
  `histopathology` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `imaging`
--
CREATE TABLE `imaging` (
  `id` int NOT NULL AUTO_INCREMENT,
  `typeImaging` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `imaging` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `laboratory`
--
CREATE TABLE `laboratory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `typeExam` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `exam` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifierType` enum('Cedula','Pasaporte','GeneratedIdentifier') COLLATE utf8mb4_general_ci NOT NULL,
  `identifierCode` varchar(255) COLLATE utf8mb4_general_ci NOT NULL UNIQUE,
  `firstName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `middleName` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lastName1` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `lastName2` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nationality` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` mediumtext COLLATE utf8mb4_general_ci NOT NULL,
  `phoneNumber` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `birthdate` date NOT NULL,
  `gender` enum('Masculino','Femenino','No Binario','Otro','Prefiero no decir') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sex` enum('Masculino','Femenino','Prefiero no decir') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `civilStatus` enum('Soltero/a','UniónDeHecho','Casado/a','Divorciado/a','Viudo/a') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `job` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `bloodType` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `preExistingCondition`
--
CREATE TABLE `preExistingCondition` (
  `id` int NOT NULL AUTO_INCREMENT,
  `diseaseName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `time` date NOT NULL,
  `medicament` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `treatment` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `idClinicHistory` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idClinicHistory` (`idClinicHistory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `regionalPhysicalExamination`
--
CREATE TABLE `regionalPhysicalExamination` (
  `id` int NOT NULL AUTO_INCREMENT,
  `typeExamination` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `examination` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reviewOrgansSystems`
--
CREATE TABLE `reviewOrgansSystems` (
  `id` int NOT NULL AUTO_INCREMENT,
  `typeReview` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `review` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `treatment`
--
CREATE TABLE `treatment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `medicament` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `via` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dosage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `unity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `frequency` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `indications` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `warning` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idAttention` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idAttention` (`idAttention`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `allergies`
--
ALTER TABLE `allergies`
  ADD CONSTRAINT `allergies_ibfk_1` FOREIGN KEY (`idClinicHistory`) REFERENCES `patients` (`id`);

--
-- Constraints for table `attention`
--
ALTER TABLE `attention`
  ADD CONSTRAINT `attention_ibfk_1` FOREIGN KEY (`idClinicHistory`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `attention_ibfk_2` FOREIGN KEY (`idDoctor`) REFERENCES `doctor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `credentials`
--
-- ALTER TABLE `credentials`
--  ADD CONSTRAINT `credentials_ibfk_1` FOREIGN KEY (`identifierCode`) REFERENCES `doctor` (`identifierCode`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `diagnostic`
--
ALTER TABLE `diagnostic`
  ADD CONSTRAINT `diagnostic_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `emergencyContact`
--
ALTER TABLE `emergencyContact`
  ADD CONSTRAINT `emergencyContact_ibfk_1` FOREIGN KEY (`idClinicHistory`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `familyBackground`
--
ALTER TABLE `familyBackground`
  ADD CONSTRAINT `familyBackground_ibfk_1` FOREIGN KEY (`idClinicHistory`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `histopathology`
--
ALTER TABLE `histopathology`
  ADD CONSTRAINT `histopathology_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `imaging`
--
ALTER TABLE `imaging`
  ADD CONSTRAINT `imaging_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `laboratory`
--
ALTER TABLE `laboratory`
  ADD CONSTRAINT `laboratory_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `preExistingCondition`
--
ALTER TABLE `preExistingCondition`
  ADD CONSTRAINT `preExistingCondition_ibfk_1` FOREIGN KEY (`idClinicHistory`) REFERENCES `patients` (`id`);

--
-- Constraints for table `regionalPhysicalExamination`
--
ALTER TABLE `regionalPhysicalExamination`
  ADD CONSTRAINT `regionalPhysicalExamination_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `reviewOrgansSystems`
--
ALTER TABLE `reviewOrgansSystems`
  ADD CONSTRAINT `reviewOrgansSystems_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `treatment`
--
ALTER TABLE `treatment`
  ADD CONSTRAINT `treatment_ibfk_1` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Índices adicionales para optimizar consultas
--
ALTER TABLE `patients` ADD INDEX `idx_patients_name` (`firstName`, `lastName1`, `lastName2`);
ALTER TABLE `doctor` ADD INDEX `idx_doctor_name` (`firstName`, `lastName1`, `lastName2`);
ALTER TABLE `patients` ADD INDEX `idx_patients_created_at` (`created_at`);
ALTER TABLE `patients` ADD INDEX `idx_patients_updated_at` (`updated_at`);
ALTER TABLE `doctor` ADD INDEX `idx_doctor_created_at` (`created_at`);
ALTER TABLE `doctor` ADD INDEX `idx_doctor_updated_at` (`updated_at`);
ALTER TABLE `attention` ADD INDEX `idx_attention_created_at` (`created_at`);
ALTER TABLE `attention` ADD INDEX `idx_attention_updated_at` (`updated_at`);
ALTER TABLE `diagnostic` ADD INDEX `idx_diagnostic_created_at` (`created_at`);
ALTER TABLE `diagnostic` ADD INDEX `idx_diagnostic_updated_at` (`updated_at`);
ALTER TABLE `treatment` ADD INDEX `idx_treatment_created_at` (`created_at`);
ALTER TABLE `treatment` ADD INDEX `idx_treatment_updated_at` (`updated_at`);
ALTER TABLE `patients` ADD INDEX `idx_patients_is_deleted` (`is_deleted`);
ALTER TABLE `doctor` ADD INDEX `idx_doctor_is_deleted` (`is_deleted`);
ALTER TABLE `attention` ADD INDEX `idx_attention_is_deleted` (`is_deleted`);
ALTER TABLE `diagnostic` ADD INDEX `idx_diagnostic_is_deleted` (`is_deleted`);
ALTER TABLE `treatment` ADD INDEX `idx_treatment_is_deleted` (`is_deleted`);
ALTER TABLE `emergencyContact` ADD INDEX `idx_emergencyContact_is_deleted` (`is_deleted`);
ALTER TABLE `familyBackground` ADD INDEX `idx_familyBackground_is_deleted` (`is_deleted`);
ALTER TABLE `preExistingCondition` ADD INDEX `idx_preExistingCondition_is_deleted` (`is_deleted`);

--
-- Restricciones CHECK para validación de datos
--
ALTER TABLE `patients` ADD CONSTRAINT `chk_birthdate_not_future` CHECK ((`birthdate` <= curdate()));
ALTER TABLE `attention` ADD CONSTRAINT `chk_weight_range` CHECK (((`weight` is null) or ((`weight` > 0) and (`weight` < 500))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_height_range` CHECK (((`height` is null) or ((`height` > 0) and (`height` < 300)))); -- Si la altura es en cm. Si es en m, sería < 3
ALTER TABLE `attention` ADD CONSTRAINT `chk_temperature_range` CHECK (((`temperature` is null) or ((`temperature` > 25) and (`temperature` < 45))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_bloodPressure_range` CHECK (((`bloodPressure` is null) or ((`bloodPressure` > 40) and (`bloodPressure` < 300))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_heartRate_range` CHECK (((`heartRate` is null) or ((`heartRate` > 30) and (`heartRate` < 250))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_oxygenSaturation_range` CHECK (((`oxygenSaturation` is null) or ((`oxygenSaturation` >= 0) and (`oxygenSaturation` <= 100))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_breathingFrequency_range` CHECK (((`breathingFrequency` is null) or ((`breathingFrequency` > 0) and (`breathingFrequency` < 100))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_glucose_range` CHECK (((`glucose` is null) or ((`glucose` > 0) and (`glucose` < 1500))));
ALTER TABLE `attention` ADD CONSTRAINT `chk_hemoglobin_range` CHECK (((`hemoglobin` is null) or ((`hemoglobin` > 0) and (`hemoglobin` < 30))));
ALTER TABLE `doctor` ADD CONSTRAINT `chk_doctor_email_format` CHECK ((`email` regexp _utf8mb4'^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$'));
ALTER TABLE `familyBackground` ADD CONSTRAINT `chk_familyBackground_time_not_future` CHECK ((`time` <= curdate()));
ALTER TABLE `preExistingCondition` ADD CONSTRAINT `chk_preExistingCondition_time_not_future` CHECK ((`time` <= curdate()));
ALTER TABLE `attention` ADD CONSTRAINT `chk_attention_date_not_future` CHECK ((`date` <= CURRENT_TIMESTAMP));

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;