-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema taxi_empresa
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema taxi_empresa
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `taxi_empresa` DEFAULT CHARACTER SET utf8 ;
USE `taxi_empresa` ;

-- -----------------------------------------------------
-- Table `taxi_empresa`.`usuarios`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `taxi_empresa`.`usuarios` ;

CREATE TABLE IF NOT EXISTS `taxi_empresa`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `apellido` VARCHAR(255) NULL,
  `empresa` VARCHAR(255) NULL,
  `cargo` VARCHAR(255) NULL,
  `telefono` TEXT NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taxi_empresa`.`conductores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `taxi_empresa`.`conductores` ;

CREATE TABLE IF NOT EXISTS `taxi_empresa`.`conductores` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `apellido` VARCHAR(255) NULL,
  `empresa` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `taxi_empresa`.`viajes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `taxi_empresa`.`viajes` ;

CREATE TABLE IF NOT EXISTS `taxi_empresa`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `direccion_inicio` VARCHAR(255) NULL,
  `direccion_destino` VARCHAR(255) NULL,
  `detalles` TEXT NULL,
  `usuario_id` INT NOT NULL,
  `conductor_id` INT NULL,
  `valor_viaje` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_conductor_idx` (`conductor_id` ASC) VISIBLE,
  INDEX `fk_viajes_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajes_conductor`
    FOREIGN KEY (`conductor_id`)
    REFERENCES `taxi_empresa`.`conductores` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_viajes_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `taxi_empresa`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
