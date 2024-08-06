DROP DATABASE IF EXISTS `school`;
CREATE DATABASE `school`; 
USE `school`;
CREATE TABLE `students` (
    student_id INT UNSIGNED AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
	password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(11),
    birth_date DATE,
    PRIMARY KEY (student_id)
);
CREATE TABLE `staff` (
    staff_id INT UNSIGNED AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
	password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(11),
    birth_date DATE,
    role_id INT,
    PRIMARY KEY (staff_id)
);
CREATE TABLE `role_ids` (
    role_id INT UNSIGNED AUTO_INCREMENT,
    role_name VARCHAR(50),
	PRIMARY KEY (role_id)
);
CREATE TABLE `courses` (
	course_id INT UNSIGNED AUTO_INCREMENT,
    course_name VARCHAR(255),
    duration VARCHAR(255),
    price VARCHAR(255),
	PRIMARY KEY (course_id)
);
CREATE TABLE `course_students` (
    course_id INT UNSIGNED ,
    student_id INT UNSIGNED ,
	FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

INSERT INTO `role_ids` (role_id, role_name)
VALUES (1,"Teacher"),(2,"Expert"),(3,"Manager");
INSERT INTO `students` (username)
VALUES("S1"),("S2"),("S3");
INSERT INTO `staff` (username, password, role_id)
VALUES("M1", 1234, 4), ("M2", 1234, 4), ("E1", 1234, 3), ("E2", 1234, 3), 
("T1", 1234, 2), ("T2", 1234, 2), ("T3", 1234, 2), ("T4", 1234, 2);
INSERT INTO `courses` (course_name)
VALUES('C');
INSERT INTO `course_students` (course_id, student_id)
VALUES (1, 1),(1, 2),(1, 3);
