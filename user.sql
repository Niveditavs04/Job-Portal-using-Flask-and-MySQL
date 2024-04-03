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
    email_notification_active CHAR(1),
    user_image BLOB,
    registration_date DATE,
    FOREIGN KEY (user_type_id) REFERENCES user_type(user_id)
);

-- Create the user_log table
CREATE TABLE user_log (
    useraccount_id INT PRIMARY KEY,
    last_login_date DATETIME,
    last_job_apply_date DATETIME,
    FOREIGN KEY (useraccount_id) REFERENCES user_account(id)
);
