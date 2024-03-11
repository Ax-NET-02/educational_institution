DROP SCHEMA IF EXISTS educate;

-- 创建数据库
CREATE SCHEMA educate;

-- 进入数据库
USE educate;


-- 创建权限表
CREATE TABLE IF NOT EXISTS permissions (
    permission_id INT PRIMARY KEY AUTO_INCREMENT,
    permission_name VARCHAR(50) NOT NULL
);


-- 创建管理员表
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_email VARCHAR(50) NOT NULL,
    admin_password_hash VARCHAR(64) NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id)
);


-- 创建客服表
CREATE TABLE IF NOT EXISTS customer_service (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL,
    message_id INT,
    permission_id INT NOT NULL,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id),
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);


-- 创建用户表
CREATE TABLE IF NOT EXISTS users
(
    user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    message_id INT,
    permission_id INT NOT NULL,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id),
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);


-- 创建消息表
CREATE TABLE IF NOT EXISTS messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    service_id INT,
    user_message_content TEXT NOT NULL,
    service_message_content TEXT NOT NULL,
    user_sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    service_sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (service_id) REFERENCES customer_service(service_id)
);






<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
