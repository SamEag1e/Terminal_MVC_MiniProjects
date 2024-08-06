DROP DATABASE IF EXISTS `online_shop`;
CREATE DATABASE `online_shop`;
USE `online_shop`;
CREATE TABLE `customers` (
	customer_id INT UNSIGNED AUTO_INCREMENT,
    register_date DATE,
    national_code VARCHAR(10),
    phone VARCHAR(11),
    email VARCHAR (255),
    username VARCHAR (255),
    pw VARCHAR (255),
    f_name VARCHAR (255),
    l_name VARCHAR (255),
    PRIMARY KEY (customer_id)
);
CREATE TABLE `admins` (
	admin_id INT UNSIGNED AUTO_INCREMENT,
    national_code VARCHAR(10),
    phone VARCHAR(11),
    email VARCHAR (255),
    username VARCHAR (255),
    pw VARCHAR (255),
    f_name VARCHAR (255),
    l_name VARCHAR (255),
    PRIMARY KEY (admin_id)
);
CREATE TABLE `products` (
	product_id INT UNSIGNED AUTO_INCREMENT,
    product_type VARCHAR(255),
    product_name VARCHAR(255),
    price VARCHAR (255),
    count INT,
    PRIMARY KEY (product_id)
);
CREATE TABLE `receipts` (
	receipt_id INT UNSIGNED AUTO_INCREMENT,
    customer_id INT UNSIGNED,
    buy_datetime DATETIME,
    tracing_code VARCHAR (255),
    total_price VARCHAR (255),
    products_count INT UNSIGNED,
    PRIMARY KEY (receipt_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE `product_users` (
	product_user_id INT UNSIGNED AUTO_INCREMENT,
	receipt_id INT UNSIGNED,
    product_id INT UNSIGNED,
    count INT UNSIGNED,
    PRIMARY KEY (product_user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
	FOREIGN KEY (receipt_id) REFERENCES receipts(receipt_id)
);
INSERT INTO `admins` (national_code, phone, email, username, pw, f_name, l_name)
VALUES (1234567890, 1234567890, "admin@admin.admin", "admin", "admin", "admin", "admin"),
		(0987456321, 0987456321, "admin2@gmail.com", "admin2", "admin2", "admin2", "admin2");

INSERT INTO `customers` (register_date, national_code, phone, email, username, pw, f_name, l_name)
VALUES ("2024-3-5" ,1234567890, 1234567890, "root@root.root", "root", "root", "root", "root"),
		("2023-12-1", 0987456321, 0987456321, "root2@gmail.com", "root2", "root2", "root2", "root2");

INSERT INTO `products` (product_type, product_name, price, count)
VALUES ("books", "joz az koll", "2000000", 50),
		("wall Clocks", "technoline WT 8000", "20000000", 20);
