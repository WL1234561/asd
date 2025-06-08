# Library Management System

这是一个简单的图书管理系统示例，使用 **Flask** 作为后端框架，数据存储在 MySQL 数据库 `database3` 中。系统提供三种角色：管理员（admin）、普通用户（user）和游客（guest）。

## 功能

- 游客可以浏览书籍列表；
- 用户可以登录并借阅书籍；
- 管理员可以登录并添加新书；
- 简单的页面界面，位于 `templates/` 目录。

## 运行

1. 安装依赖：
   ```bash
   pip install flask mysql-connector-python
   ```
2. 创建数据库 `database3` 并初始化表：
   ```sql
   CREATE DATABASE database3;

   USE database3;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100) UNIQUE,
       password VARCHAR(100),
       role ENUM('admin','user')
   );

   CREATE TABLE books (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(200),
       author VARCHAR(200)
   );

   CREATE TABLE borrow (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100),
       book_id INT,
       FOREIGN KEY (book_id) REFERENCES books(id)
   );
   ```
3. 运行应用：
   ```bash
   python library_app/app.py
   ```

运行后访问 `http://localhost:5000` 即可。
