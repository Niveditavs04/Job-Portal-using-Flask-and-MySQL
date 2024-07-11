-- Create the database
CREATE DATABASE IF NOT EXISTS db1;
USE db1;

-- Create the user_type table
CREATE TABLE user_type (
    user_id INT PRIMARY KEY,
    user_type_name VARCHAR(255) NOT NULL
);

-- Create the user_account table
CREATE TABLE user_account ( 
    id INT PRIMARY KEY,
    user_type_id INT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender CHAR(1),
    is_active CHAR(1) DEFAULT 'Y',
    contact_number VARCHAR(20),
    sms_notification_active CHAR(1),
    email_notification_active CHAR(1),
    user_image BLOB,
    registration_date DATE,
    FOREIGN KEY (user_type_id) REFERENCES user_type(user_id)
);
-- ALTER TABLE user_account MODIFY id INT AUTO_INCREMENT ;

-- Create the user_log table
CREATE TABLE user_log (
    useraccount_id INT PRIMARY KEY,
    last_login_date DATETIME,
    last_job_apply_date DATETIME,
    FOREIGN KEY (useraccount_id) REFERENCES user_account(id)
);

SELECT
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    TABLE_NAME = 'user_account';
    AND TABLE_SCHEMA = 'db1';

ALTER TABLE user_account
DROP FOREIGN KEY user_account_ibfk_1;
ALTER TABLE user_account
ADD CONSTRAINT user_account_ibfk_1
FOREIGN KEY (user_type_id)
REFERENCES user_type(user_id)
ON DELETE CASCADE;


mysql> insert into user_type values(4,"new");
Query OK, 1 row affected (0.02 sec)

mysql> insert into user_account(id,user_type_id,email,password) values(9,2,'new@gmail.com','new');
Query OK, 1 row affected (0.02 sec)

mysql> delete from user_type where user_id=4;
Query OK, 1 row affected (0.02 sec)

mysql> select * from user_account;


SELECT
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    TABLE_NAME = 'user_log';
    AND TABLE_SCHEMA = 'db1';

ALTER TABLE user_log
DROP FOREIGN KEY fk_user_log_user_id;
ALTER TABLE user_log
ADD CONSTRAINT fk_user_log_user_id
FOREIGN KEY (useraccount_id)
REFERENCES user_account(id)
ON DELETE CASCADE;
