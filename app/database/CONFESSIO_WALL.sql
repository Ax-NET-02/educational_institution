-- 删除数据库
DROP SCHEMA IF EXISTS ConfessioWall;

-- 创建数据库
CREATE SCHEMA ConfessioWall;

-- 进入数据库
USE ConfessioWall;


-- 创建用户表
CREATE TABLE IF NOT EXISTS users
(
    userid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    mail VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    avatar VARCHAR(255)
);


-- 创建发布帖子表
CREATE TABLE IF NOT EXISTS articles
(
    articleid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userid INT NOT NULL,
    content TEXT,
    img TEXT,
    expression TEXT,
    FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE
);


-- 创建评论内容表
CREATE TABLE IF NOT EXISTS comments
(
    commentid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    comments TEXT,
    comment_img TEXT,
    comment_emoticons VARCHAR(255),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE
);
