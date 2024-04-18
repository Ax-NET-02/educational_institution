-- 删除已有的数据库
DROP SCHEMA IF EXISTS educate;

-- 创建新的数据库
CREATE SCHEMA educate;

-- 使用新的数据库
USE educate;

-- 创建权限表
CREATE TABLE IF NOT EXISTS permissions (
    permission_id INT PRIMARY KEY AUTO_INCREMENT,
    permission_name VARCHAR(50) NOT NULL
);

-- 创建客服表
CREATE TABLE IF NOT EXISTS customer_service (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    service_name VARCHAR(50) NOT NULL,
    service_password VARCHAR(255) NOT NULL,
    service_email VARCHAR(50) NOT NULL,
    service_number VARCHAR(50) NOT NULL,
    permission_id INT NOT NULL
);

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL,
    user_mail VARCHAR(50) NOT NULL,
    user_number VARCHAR(50) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    permission_id INT NOT NULL
);

-- 创建消息表
CREATE TABLE IF NOT EXISTS messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    service_id INT,
    user_message_content TEXT NOT NULL,
    service_message_content TEXT NOT NULL,
    user_sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    service_sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建管理员表
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_name VARCHAR(50) NOT NULL,
    admin_mail VARCHAR(50) NOT NULL,
    admin_password VARCHAR(64) NOT NULL,
    permission_id INT NOT NULL
);

-- 创建课程表
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_title VARCHAR(255) NOT NULL,
    course_description TEXT NOT NULL,
    course_price DECIMAL(10, 2) NOT NULL,
    course_duration INT NOT NULL, -- 以分钟为单位
    course_rating DECIMAL(3, 2), -- 可以存储评分，例如4.5
    course_image VARCHAR(255), -- 图片路径或URL
    course_publish_date DATE, -- 默认使用当前日期
    publisher_name TEXT NOT NULL -- 发布者ID
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    cc_name VARCHAR(50) NOT NULL,
    cc_number VARCHAR(16) NOT NULL,
    cc_cvv VARCHAR(4) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_amount DECIMAL(10, 2) NOT NULL
);






-- 添加外键约束
-- ALTER TABLE customer_service ADD FOREIGN KEY (permission_id) REFERENCES permissions(permission_id);
-- ALTER TABLE customer_service ADD FOREIGN KEY (message_id) REFERENCES messages(message_id);
-- ALTER TABLE users ADD FOREIGN KEY (permission_id) REFERENCES permissions(permission_id);
-- ALTER TABLE users ADD FOREIGN KEY (message_id) REFERENCES messages(message_id);
-- ALTER TABLE admin ADD FOREIGN KEY (permission_id) REFERENCES permissions(permission_id);
