create table IF NOT EXISTS user_account(
u_id INT primary key,
user_type_id INT ,
email Varchar(150),
password Varchar(150),
dob date,
gender varchar(10),
contact bigint,
email_notification varchar(10),
user_image blob,
reg_date date
);



create table if NOT EXISTS user_typen(
id int primary key ,
usertype varchar(50)
);



create table  user_log(
    user_iid int primary key,
    last_login_d date,
    last_job_d date
);