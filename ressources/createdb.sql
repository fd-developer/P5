CREATE DATABASE database CHARACTER SET 'utf8mb4';
CREATE USER 'dbuser'@'dbserver' IDENTIFIED BY 'dbpassword';
USE database;
GRANT ALL PRIVILEGES ON database.* TO 'dbuser'@'dbserver'; 
CREATE TABLE Categorie (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
)
ENGINE=INNODB;
CREATE TABLE Product (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,
    name text,
    nutriscoreG VARCHAR(1),
    store text,
    url text,
    substitute VARCHAR(20),
    PRIMARY KEY (id)
)
ENGINE=INNODB;
CREATE TABLE REL_Product_Categorie (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_product INT UNSIGNED,
    id_categorie INT UNSIGNED,
    PRIMARY KEY (id)
)
ENGINE=INNODB;
CREATE INDEX id_product ON REL_Product_Categorie (id_product);
CREATE INDEX id_categorie ON REL_Product_Categorie (id_categorie);
ALTER TABLE REL_Product_Categorie
ADD CONSTRAINT fk_id_categorie FOREIGN KEY (id_categorie) REFERENCES Categorie(id);
ALTER TABLE REL_Product_Categorie
ADD CONSTRAINT fk_id_product FOREIGN KEY (id_product) REFERENCES Product(id);