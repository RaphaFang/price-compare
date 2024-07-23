CREATE DATABASE pc_db;
CREATE DATABASE task_db;
GRANT ALL PRIVILEGES ON pc_db.* TO 'test'@'%';
GRANT ALL PRIVILEGES ON task_db.* TO 'test'@'%';
FLUSH PRIVILEGES;

-- 要透過admin來提供全獻給test

CREATE TABLE main_table (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
    text VARCHAR(255) NOT NULL COMMENT 'Upload comment',
    pic VARCHAR(2048) COMMENT 'Upload pic URL';
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Builded time'
);
