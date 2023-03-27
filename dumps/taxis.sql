-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema taxis
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `taxis` ;

-- -----------------------------------------------------
-- Schema taxis
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `taxis` DEFAULT CHARACTER SET utf8mb3 ;
USE `taxis` ;

-- -----------------------------------------------------
-- Table `taxis`.`usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `taxis`.`usuarios` ;

CREATE TABLE IF NOT EXISTS `taxis`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL DEFAULT NULL,
  `apellido` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `empresa` VARCHAR(255) NULL DEFAULT NULL,
  `es_conductor` TINYINT NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `taxis`.`viajes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `taxis`.`viajes` ;

CREATE TABLE IF NOT EXISTS `taxis`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `direccion_inicio` VARCHAR(255) NULL DEFAULT NULL,
  `direccion_destino` VARCHAR(255) NULL DEFAULT NULL,
  `detalles` TEXT NULL DEFAULT NULL,
  `solicitante_id` INT NOT NULL,
  `conductor_id` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_usuarios_idx` (`solicitante_id` ASC) VISIBLE,
  INDEX `fk_viajes_usuarios1_idx` (`conductor_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajes_usuarios`
    FOREIGN KEY (`solicitante_id`)
    REFERENCES `taxis`.`usuarios` (`id`),
  CONSTRAINT `fk_viajes_usuarios1`
    FOREIGN KEY (`conductor_id`)
    REFERENCES `taxis`.`usuarios` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
