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
-- Table structure for table `doctor`
--
CREATE TABLE `doctor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifierCode` varchar(255) NOT NULL UNIQUE,
  `firstName` varchar(255) NOT NULL,
  `middleName` varchar(255) NOT NULL, -- Considerar hacerlo NULLABLE si no siempre se tiene
  `lastName1` varchar(255) NOT NULL,
  `lastName2` varchar(255) NOT NULL, -- Considerar hacerlo NULLABLE
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
-- Table structure for table `allergies`
--
CREATE TABLE `allergies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `allergies` text COLLATE utf8mb4_general_ci NOT NULL,
  `idPatient` int NOT NULL, -- CAMBIADO de idClinicHistory
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idPatient` (`idPatient`) -- CAMBIADO
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
  `bloodPressure` varchar(20) DEFAULT NULL, -- Cambiado a varchar para rangos como "120/80"
  `heartRate` int DEFAULT NULL,
  `oxygenSaturation` int DEFAULT NULL,
  `breathingFrequency` int DEFAULT NULL,
  `glucose` decimal(5,1) DEFAULT NULL,                  
  `hemoglobin` decimal(4,1) DEFAULT NULL,               
  `reasonConsultation` varchar(255) NOT NULL,
  `currentIllness` varchar(255) NOT NULL,
  `evolution` varchar(255) NOT NULL,
  `idPatient` int NOT NULL, -- CAMBIADO de idClinicHistory
  `idDoctor` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idPatient` (`idPatient`), -- CAMBIADO
  KEY `idDoctor` (`idDoctor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `credentials`
--
CREATE TABLE `credentials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifierCode` varchar(255) NOT NULL, -- Este debería referenciar a doctor.identifierCode o patients.identifierCode
  `password` varchar(255) NOT NULL, -- Debería estar hasheada
  `idUser` int NOT NULL, -- ID del doctor o paciente al que pertenece la credencial
  `userType` enum('doctor', 'patient') NOT NULL, -- Para saber a qué tabla buscar con idUser
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_identifier_usertype` (`identifierCode`, `userType`), -- Asegura que el código sea único por tipo de usuario
  KEY `idUser` (`idUser`)
  -- Considerar FK a doctor(id) o patient(id) basado en userType, aunque esto es más complejo de implementar directamente en SQL
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
-- Table structure for table `emergencyContact`
--
CREATE TABLE `emergencyContact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `lastName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `address` text COLLATE utf8mb4_general_ci NOT NULL,
  `relationship` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phoneNumber1` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phoneNumber2` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL, -- Puede ser opcional
  `idPatient` int NOT NULL, -- CAMBIADO de idClinicHistory
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idPatient` (`idPatient`) -- CAMBIADO
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `familyBackground`
--
CREATE TABLE `familyBackground` (
  `id` int NOT NULL AUTO_INCREMENT,
  `familyBackground` text COLLATE utf8mb4_general_ci NOT NULL,
  `time` date NOT NULL,
  `degreeRelationship` enum('1','2','3','4') COLLATE utf8mb4_general_ci NOT NULL, -- Considerar varchar si los valores son nombres
  `idPatient` int NOT NULL, -- CAMBIADO de idClinicHistory
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idPatient` (`idPatient`) -- CAMBIADO
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
  `imaging` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL, -- Podría ser una URL o referencia a un archivo
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
  `exam` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL, -- Podría ser una URL o referencia a un archivo
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
-- Table structure for table `preExistingCondition`
--
CREATE TABLE `preExistingCondition` (
  `id` int NOT NULL AUTO_INCREMENT,
  `diseaseName` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `time` date NOT NULL,
  `medicament` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `treatment` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `idPatient` int NOT NULL, -- CAMBIADO de idClinicHistory
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` varchar(255) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idPatient` (`idPatient`) -- CAMBIADO
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
  ADD CONSTRAINT `fk_allergies_patient` FOREIGN KEY (`idPatient`) REFERENCES `patients` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `attention`
--
ALTER TABLE `attention`
  ADD CONSTRAINT `fk_attention_patient` FOREIGN KEY (`idPatient`) REFERENCES `patients` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_attention_doctor` FOREIGN KEY (`idDoctor`) REFERENCES `doctor` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `credentials`
--
-- Para la FK de credentials, necesitarías lógica de aplicación o triggers si quieres que idUser referencie dinámicamente
-- a patients.id o doctor.id basado en userType. Una FK directa solo puede apuntar a una tabla.
-- Ejemplo si SOLO fuera para doctores:
-- ALTER TABLE `credentials`
-- ADD CONSTRAINT `fk_credentials_doctor` FOREIGN KEY (`idUser`) REFERENCES `doctor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- NOTA: La FK original a doctor.identifierCode es menos común que a doctor.id. Si es intencional, asegúrate que doctor.identifierCode sea siempre único.

--
-- Constraints for table `diagnostic`
--
ALTER TABLE `diagnostic`
  ADD CONSTRAINT `fk_diagnostic_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `emergencyContact`
--
ALTER TABLE `emergencyContact`
  ADD CONSTRAINT `fk_emergencyContact_patient` FOREIGN KEY (`idPatient`) REFERENCES `patients` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `familyBackground`
--
ALTER TABLE `familyBackground`
  ADD CONSTRAINT `fk_familyBackground_patient` FOREIGN KEY (`idPatient`) REFERENCES `patients` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `histopathology`
--
ALTER TABLE `histopathology`
  ADD CONSTRAINT `fk_histopathology_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `imaging`
--
ALTER TABLE `imaging`
  ADD CONSTRAINT `fk_imaging_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `laboratory`
--
ALTER TABLE `laboratory`
  ADD CONSTRAINT `fk_laboratory_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `preExistingCondition`
--
ALTER TABLE `preExistingCondition`
  ADD CONSTRAINT `fk_preExistingCondition_patient` FOREIGN KEY (`idPatient`) REFERENCES `patients` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `regionalPhysicalExamination`
--
ALTER TABLE `regionalPhysicalExamination`
  ADD CONSTRAINT `fk_regionalPhysicalExamination_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `reviewOrgansSystems`
--
ALTER TABLE `reviewOrgansSystems`
  ADD CONSTRAINT `fk_reviewOrgansSystems_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `treatment`
--
ALTER TABLE `treatment`
  ADD CONSTRAINT `fk_treatment_attention` FOREIGN KEY (`idAttention`) REFERENCES `attention` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

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
-- ALTER TABLE `attention` ADD CONSTRAINT `chk_bloodPressure_range` CHECK (((`bloodPressure` is null) or ((`bloodPressure` > 40) and (`bloodPressure` < 300)))); -- Comentado porque bloodPressure ahora es varchar
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