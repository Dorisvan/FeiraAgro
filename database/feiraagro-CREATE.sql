-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema feiraagro
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema feiraagro
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `feiraagro` DEFAULT CHARACTER SET utf8 ;
USE `feiraagro` ;

-- -----------------------------------------------------
-- Table `feiraagro`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feiraagro`.`Usuario` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(200) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `senha` VARCHAR(200) NOT NULL,
  `endereco` VARCHAR(100) NOT NULL,
  `tipo` VARCHAR(20) NOT NULL,
  `nivel` INT NOT NULL,
  `contato` VARCHAR(50) NULL,
  `estado_login` INT NULL,
  `imagem_perfil` VARCHAR(100) NULL,
  PRIMARY KEY (`codigo`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feiraagro`.`Produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feiraagro`.`Produto` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `quantidade` INT NOT NULL,
  `valor` DOUBLE NOT NULL,
  `classificacao` VARCHAR(30) NOT NULL,
  `procedencia` VARCHAR(50) NOT NULL,
  `img_produto` VARCHAR(50) NULL,
  `descricao` VARCHAR(500) NULL,
  `Usuario_codigo` BIGINT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Produto_Usuario1_idx` (`Usuario_codigo` ASC),
  CONSTRAINT `fk_Produto_Usuario1`
    FOREIGN KEY (`Usuario_codigo`)
    REFERENCES `feiraagro`.`Usuario` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feiraagro`.`Pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feiraagro`.`Pedido` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `data_pedido` DATE NOT NULL,
  `data_entrega` DATE NOT NULL,
  `quantidade` INT NOT NULL,
  `situacao` VARCHAR(50) NOT NULL,
  `modo_entrega` VARCHAR(50) NOT NULL,
  `status_compra` VARCHAR(45) NULL,
  `Usuario_codigo` BIGINT NOT NULL,
  `Produto_codigo` BIGINT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Compra_Usuario1_idx` (`Usuario_codigo` ASC),
  INDEX `fk_Pedido_Produto1_idx` (`Produto_codigo` ASC),
  CONSTRAINT `fk_Compra_Usuario1`
    FOREIGN KEY (`Usuario_codigo`)
    REFERENCES `feiraagro`.`Usuario` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pedido_Produto1`
    FOREIGN KEY (`Produto_codigo`)
    REFERENCES `feiraagro`.`Produto` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feiraagro`.`Perfil_Produtor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feiraagro`.`Perfil_Produtor` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `descricao_producao` VARCHAR(500) NULL,
  `local_venda` VARCHAR(70) NULL,
  `img0` VARCHAR(50) NULL,
  `img1` VARCHAR(50) NULL,
  `img2` VARCHAR(50) NULL,
  `img3` VARCHAR(50) NULL,
  `img_pix` VARCHAR(50) NULL,
  `Usuario_codigo` BIGINT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Perfil_Produtor_Usuario1_idx` (`Usuario_codigo` ASC),
  CONSTRAINT `fk_Perfil_Produtor_Usuario1`
    FOREIGN KEY (`Usuario_codigo`)
    REFERENCES `feiraagro`.`Usuario` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feiraagro`.`Mensagem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feiraagro`.`Mensagem` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(100) NOT NULL,
  `conteudo` VARCHAR(500) NOT NULL,
  `tipo` VARCHAR(30) NULL,
  `situacao` VARCHAR(45) NULL,
  `Usuario_codigo` BIGINT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Mensagem_Usuario1_idx` (`Usuario_codigo` ASC),
  CONSTRAINT `fk_Mensagem_Usuario1`
    FOREIGN KEY (`Usuario_codigo`)
    REFERENCES `feiraagro`.`Usuario` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feiraagro`.`Carrinho`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feiraagro`.`Carrinho` (
  `codigo` BIGINT NOT NULL AUTO_INCREMENT,
  `lista` VARCHAR(1000) NULL,
  `Usuario_codigo` BIGINT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_Carrinho_Usuario1_idx` (`Usuario_codigo` ASC),
  CONSTRAINT `fk_Carrinho_Usuario1`
    FOREIGN KEY (`Usuario_codigo`)
    REFERENCES `feiraagro`.`Usuario` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
