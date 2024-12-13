CREATE DATABASE IF NOT EXISTS ecourse_db;
CREATE USER 'ecourse_user'@'localhost' IDENTIFIED BY 'ecourse_pwd';
GRANT ALL PRIVILEGES ON ecourse_db.* TO 'ecourse_user'@'localhost';
FLUSH PRIVILEGES;
