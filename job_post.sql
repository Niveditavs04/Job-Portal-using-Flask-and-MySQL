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
// salary and status can be added
-- create job_application_status, to hold all possible application statuses. Some statuses might be ‘submitted’, ‘under review’, ‘archived’, ‘rejected’, ‘shortlisted for interview’, ‘under recruitment process’, and so on
create table job_application_status(id int primary key ,status_desc varchar(20));
create table job_app_action(id int primary key, actionname varchar(20));
-- create table job post activity log
create table jpal(id int primary key,jpactivity_id int, jpaction_id int,actiondt date ,userid int,
 FOREIGN KEY (jpactivity_id) REFERENCES job_post_activity(activity_id),
 FOREIGN KEY (jpaction_id) REFERENCES job_app_action(id),
FOREIGN KEY (userid) REFERENCES db1.user_account(id)
);
-- Convert existing columns into foreign keys

ALTER TABLE job_post_activity
add job_app_status_id int,
ADD FOREIGN KEY (job_app_status_id) REFERENCES job_application_status(id),
ADD FOREIGN KEY (job_post_id) REFERENCES job_post(pid),
ADD FOREIGN KEY (uacid) REFERENCES db3.skill_set(user_account_id);

 Alter table job_post add foreign key(posted_by) references db1.user_account(id),add foreign key(company_id) references db2.company(id);

 --  job portals : wellfound
