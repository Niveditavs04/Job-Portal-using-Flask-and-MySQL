mysql> create database db4;
Query OK, 1 row affected (0.02 sec)

mysql> use db4;
Database changed
mysql>  create table job_post_activity(uacid int ,job_post_id int,apply_date date);
Query OK, 0 rows affected (0.06 sec)

mysql>  create table job_post(pid int ,posted_by int,job_type_id int,company_id int,is_cnm_hid char(1),createdt date,jobdesc varchar(500),joblocid int ,is_active char(1));
Query OK, 0 rows affected (0.06 sec)

mysql>  create table job_type(pid int ,job_type varchar (40));
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

INSERT INTO job_location (id, street, city, state, country, zip) VALUES
(1, 'ABC Street', 'Mumbai', 'Maharashtra', 'India', '400001'), -- DMART
(2, 'XYZ Street', 'Noida', 'Uttar Pradesh', 'India', '201301'), -- ADOBE
(3, 'Eaton Avenue', 'Dublin', 'Ohio', 'USA', '43017'), -- EATON
(4, 'Infosys Avenue', 'Bengaluru', 'Karnataka', 'India', '560100'), -- INFOSYS
(5, 'JP Morgan Street', 'New York', 'New York', 'USA', '10005'), -- JP MORGAN
(6, 'Unacademy Road', 'Bengaluru', 'Karnataka', 'India', '560001'), -- UNACADEMY
(7, 'Tech Mahindra Street', 'Pune', 'Maharashtra', 'India', '411004'), -- TECH MAHINDRA
(8, 'Asian Paints Avenue', 'Mumbai', 'Maharashtra', 'India', '400093'), -- ASIAN PAINTS
(9, 'Cognizant Street', 'Chennai', 'Tamil Nadu', 'India', '600006'), -- COGNIZANT
(10, 'Goldman Sachs Street', 'New York', 'New York', 'USA', '10004'), -- GOLDMAN SACHS
(11, 'Barclays Avenue', 'London', NULL, 'United Kingdom', 'E14 5HP'), -- BARCLAYS
(12, 'BNY Mellon Street', 'New York', 'New York', 'USA', '10005'), -- BNY MELLON
(13, 'Google Avenue', 'Mountain View', 'California', 'USA', '94043'), -- GOOGLE
(14, 'Mastercard Avenue', 'Purchase', 'New York', 'USA', '10577'), -- MASTERCARD
(15, 'Intuit Street', 'Mountain View', 'California', 'USA', '94043'); -- INTUIT

INSERT INTO job_location (id, street, city, state, country, zip) VALUES
(19,'9th Street, T Nagar','Chennai','Tamil Nadu','India','600001')
INSERT INTO job_type (pid, job_type) VALUES
(1, 'Full Time'), -- Human Resources
(2, 'Part Time'), -- Human Resources
(3, 'contract based');-- Human Resources

SELECT
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    TABLE_NAME = 'job_post_skillset'
    AND TABLE_SCHEMA = 'db4';

INSERT INTO job_app_action (id, actionname) 
VALUES 
    (1, 'submitted'),
    (2, 'under review'),
    (3, 'archived'),
    (4, 'rejected'),
    (5, 'shortlisted '),
    (6, 'under scrutiny'),
    (7, 'selected');

INSERT INTO job_application_status (id, status_desc) 
VALUES 
    (1, 'submitted'),
    (2, 'under review'),
    (3, 'archived'),
    (4, 'rejected'),
    (5, 'shortlisted '),
    (6, 'under scrutiny'),
    (7, 'selected');

insert into job_post values(4,2,1,1005,'y',curdate(),'Financial Analyst:We are hiring a Financial Analyst to join our finance team in Chennai, Tamil Nadu, India. The successful candidate will analyze financial data, prepare reports, and provide insights to support business decision-making. You will collaborate with various departments to forecast budgets, track expenses, and optimize financial processes. Proficiency in Microsoft Excel and financial analysis is required, along with medium-level knowledge of accounting principles.',19,'y');

SELECT 
    jp.pid,
    jp.createdt,
    jp.jobdesc,
    c.company_name,
    l.job_type,
    CONCAT(ad.street, ', ', ad.city, ', ', ad.state, ', ', ad.country, ', ', ad.zip) AS address,
    GROUP_CONCAT(f.skill_set_name) AS skill_set_names
FROM 
    db4.job_post jp
INNER JOIN
    db2.company c ON jp.company_id = c.id
INNER JOIN 
    db4.job_type l ON jp.job_type_id = l.pid
INNER JOIN 
    db4.job_location ad ON jp.joblocid = ad.id
INNER JOIN 
    db4.job_post_skillset s ON s.job_post_id = jp.pid
INNER JOIN 
    db3.seeker_skill_set f ON s.skill_setid = f.id
   
where 
    jp.posted_by = 2
     group by jp.pid order by jp.pid;

insert into job_post_skillset values(17,4,2),(18,4,2),(19,4,2),(20,4,2);

SELECT 
    jp.pid,
    GROUP_CONCAT(f.skill_set_name) AS skill_set_names
FROM 
    db4.job_post jp
INNER JOIN
    db2.company c ON jp.company_id = c.id
INNER JOIN 
    job_type l ON jp.job_type_id = l.pid
INNER JOIN 
    job_post_skillset s ON s.job_post_id = jp.pid
INNER JOIN 
    db3.seeker_skill_set f ON s.skill_setid = f.id
WHERE 
    jp.posted_by = 2  
GROUP BY 
    jp.pid;

SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    REFERENCED_TABLE_NAME = 'job_post';

-- foriegn key constraints
-- Drop the existing foreign key constraint
ALTER TABLE job_post_activity
DROP FOREIGN KEY job_post_activity_ibfk_2;

-- Add the new foreign key constraint with ON DELETE CASCADE
ALTER TABLE job_post_activity
ADD CONSTRAINT job_post_activity_ibfk_2
FOREIGN KEY (job_post_id)
REFERENCES job_post(pid)
ON DELETE CASCADE;

ALTER TABLE job_post_skillset
DROP FOREIGN KEY job_post_skillset_ibfk_1;
ALTER TABLE job_post_skillset
ADD CONSTRAINT job_post_skillset_ibfk_1
FOREIGN KEY (job_post_id)
REFERENCES job_post(pid)
ON DELETE CASCADE;

SELECT 
    jp.pid,
    l.uacid,
    l.apply_date,
    c.status_desc
   FROM 
    job_post jp
INNER JOIN 
    job_post_activity l ON jp.pid = l.job_post_id
INNER JOIN
    job_application_status c ON l.job_app_status_id = c.id
   
where 
    jp.posted_by = 2
    order by l.activity_id;

SELECT 
    jp.pid,
    GROUP_CONCAT(l.uacid) AS uacids,
    GROUP_CONCAT(l.apply_date) AS apply_dates,
    GROUP_CONCAT(c.status_desc) AS status_descs
FROM 
    job_post jp
INNER JOIN 
    job_post_activity l ON jp.pid = l.job_post_id
INNER JOIN
    job_application_status c ON l.job_app_status_id = c.id
WHERE 
    jp.posted_by = 2
GROUP BY 
    jp.pid
ORDER BY 
    jp.pid;

SELECT
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    REFERENCED_TABLE_NAME = 'job_post_activity';

ALTER TABLE jpal
DROP FOREIGN KEY jpal_ibfk_1;

ALTER TABLE jpal
ADD CONSTRAINT jpal_ibfk_1
FOREIGN KEY (jpactivity_id)
REFERENCES job_post_activity(activity_id)
ON DELETE CASCADE;

SELECT DISTINCT jps.job_post_id
FROM db4.job_post_skillset jps
INNER JOIN db3.skill_set sss ON jps.skill_setid = sss.skill_set_id
WHERE sss.user_account_id = 3
AND jps.skill_level <= sss.skill_level and sss.skill_set_id in (jps.skill_setid);


SELECT DISTINCT jps.job_post_id
FROM db4.job_post_skillset jps
WHERE EXISTS (
    SELECT 1
    FROM db3.skill_set sss 
    WHERE sss.user_account_id = 3
    AND sss.skill_set_id = jps.skill_setid
    AND sss.skill_level <= jps.skill_level
);