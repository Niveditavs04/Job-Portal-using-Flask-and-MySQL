mysql> create database db4;
Query OK, 1 row affected (0.02 sec)

mysql> use db4;
Database changed
mysql>  create table job_post_activity(uacid int ,job_post_id int,apply_date date);
Query OK, 0 rows affected (0.06 sec)

mysql>  create table job_post(pid int ,posted_by int,job_type_id int,company_id int,is_cnm_hid char(1),createdt date,jobdesc varchar(500),joblocid int ,is_active char(1));
Query OK, 0 rows affected (0.06 sec)

mysql>  create table job_type(pid int ,job_type varchar (20));
Query OK, 0 rows affected (0.05 sec)

mysql>  create table job_post_skillset(skill_setid int ,job_post_id int,skill_level int);
Query OK, 0 rows affected (0.05 sec)

mysql> show tables;
+-------------------+
| Tables_in_db4     |
+-------------------+
| job_post          |
| job_post_activity |
| job_post_skillset |
| job_type          |
+-------------------+
4 rows in set (0.01 sec)

mysql> create table job_location (id int ,street varchar(100),city varchar(50),state varchar(50) ,country varchar(50),zip varchar(50));
Query OK, 0 rows affected (0.04 sec)

mysql> show tables;
+-------------------+
| Tables_in_db4     |
+-------------------+
| job_location      |
| job_post          |
| job_post_activity |
| job_post_skillset |
| job_type          |
+-------------------+
5 rows in set (0.00 sec)