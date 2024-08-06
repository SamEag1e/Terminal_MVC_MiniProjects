DROP DATABASE IF EXISTS `ali_baba`;
CREATE DATABASE `ali_baba`;
USE `ali_baba`;
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
CREATE TABLE `tickets` (
	ticket_id INT UNSIGNED AUTO_INCREMENT,
    transport_mode VARCHAR(255),
    origin VARCHAR(255),
    destination VARCHAR(255),
    departure DATETIME,
    arrival DATETIME,
    price VARCHAR (255),
    count INT,
    PRIMARY KEY (ticket_id)
);
CREATE TABLE `receipts` (
	receipt_id INT UNSIGNED AUTO_INCREMENT,
    ticket_id INT UNSIGNED,
    buyer_id INT UNSIGNED,
    buy_datetime DATETIME,
    tracing_code VARCHAR (255),
    total_price VARCHAR (255),
    tickets_count INT UNSIGNED,
    PRIMARY KEY (receipt_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    FOREIGN KEY (buyer_id) REFERENCES customers(customer_id)
);
CREATE TABLE `ticket_users` (
	ticket_user_id INT UNSIGNED AUTO_INCREMENT,
	receipt_id INT UNSIGNED,
    ticket_id INT UNSIGNED,
    national_code VARCHAR(10),
    phone VARCHAR(11),
    f_name VARCHAR (255),
    l_name VARCHAR (255),
    seat_number INT UNSIGNED,
    PRIMARY KEY (ticket_user_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
	FOREIGN KEY (receipt_id) REFERENCES receipts(receipt_id)
);

INSERT INTO `admins` (national_code, phone, email, username, pw, f_name, l_name)
VALUES (1234567890, 1234567890, "admin@admin.admin", "admin", "admin", "admin", "admin"),
		(0987456321, 0987456321, "admin2@gmail.com", "admin2", "admin2", "admin2", "admin2");

INSERT INTO `customers` (register_date, national_code, phone, email, username, pw, f_name, l_name)
VALUES ("2024-3-5" ,1234567890, 1234567890, "root@root.root", "root", "root", "root", "root"),
		("2023-12-1", 0987456321, 0987456321, "root2@gmail.com", "root2", "root2", "root2", "root2");

INSERT INTO `tickets` (transport_mode, origin, destination, departure, arrival, price, count)
VALUES ("airplane", "mashhad", "tehran", "2024-10-5 0:0:0", "2024-10-5 02:0:0", "30000000", 25 ),
		("train", "tabriz", "shiraz", "2024-12-1", "2024-12-3", "15000000", 30);
