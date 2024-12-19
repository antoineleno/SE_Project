CREATE DATABASE IF NOT EXISTS ecourse_db;
CREATE DATABASE IF NOT EXISTS ecourse_test_db;
CREATE USER IF NOT EXISTS 'ecourse_user'@'localhost' IDENTIFIED BY 'ecourse_pwd';
GRANT ALL PRIVILEGES ON ecourse_db.* TO 'ecourse_user'@'localhost';
GRANT ALL PRIVILEGES ON ecourse_test_db.* TO 'ecourse_user'@'localhost';
FLUSH PRIVILEGES;
