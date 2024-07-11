CREATE TABLE job_seeker_profile (
    user_account_id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    current_salary DECIMAL(10, 2),
    is_annually_monthly ENUM('annually', 'monthly'),
    currency VARCHAR(3),
    FOREIGN KEY (user_account_id) REFERENCES db1.user_account(id)
);

CREATE TABLE education_detail (
    user_account_id INT,
    certificate_degree_name VARCHAR(255),
    major VARCHAR(255),
    institute_university_name VARCHAR(255),
    start_date DATE,
    completion_date DATE,
    percentage DECIMAL(5, 2),
    cgpa DECIMAL(4, 2),
    PRIMARY KEY (user_account_id, certificate_degree_name, major),
    FOREIGN KEY (user_account_id) REFERENCES db1.user_account(id)
);

CREATE TABLE experience_detail (
    user_account_id INT PRIMARY KEY,
    is_current_job BOOLEAN,
    start_date DATE,
    end_date DATE,
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    job_location_city VARCHAR(255),
    job_location_state VARCHAR(255),
    job_location_country VARCHAR(255),
    description TEXT,
    FOREIGN KEY (user_account_id) REFERENCES db1.user_account(id)
);


CREATE TABLE profile_visit_log (
    id INT PRIMARY KEY,
    seeker_profile_id INT,
    visit_date DATETIME,
    user_account_id INT,
    is_resume_downloaded BOOLEAN,
    is_job_notification_sent BOOLEAN,
    FOREIGN KEY (seeker_profile_id) REFERENCES job_seeker_profile(user_account_id),
    FOREIGN KEY (user_account_id) REFERENCES db1.user_account(id)
);

CREATE TABLE skill_set (
    user_account_id INT, 
    skill_set_id INT,
    skill_level INT CHECK (skill_level >= 1 AND skill_level <= 10),
    PRIMARY KEY(user_account_id,skill_set_id),
    FOREIGN KEY (user_account_id) REFERENCES db1.user_account(id),
    FOREIGN KEY (skill_set_id) REFERENCES seeker_skill_set(id)
);

CREATE TABLE seeker_skill_set(
    id int primary key,
    skill_set_nam varchar(50));

INSERT INTO seeker_skill_set (id, skill_set_name) VALUES 
(1, 'Language Proficiency'),
(2, 'Web Development'),
(3, 'Mobile App Development'),
(4, 'Devops'),
(5, 'Communication Skills'),
(6, 'AWS Cloud Engineer'),
(7, 'MERN Developer'),
(8, 'Payroll Management'),
(9, 'Java Full Stack Developer'),
(10, 'Backend Developer'),
(11, 'Technical Support'),
(12, 'Software Development'),
(13, 'Database Management'),
(14, 'Network Administration'),
(15, 'Cybersecurity'),
(16, 'Data Analysis'),
(17, 'Financial Reporting'),
(18, 'Auditing'),
(19, 'Taxation'),
(20, 'Financial Analysis')
ON DUPLICATE KEY UPDATE skill_set_name = VALUES(skill_set_name);



SELECT 
    jp.user_account_id,
    jp.first_name,
    jp.last_name,
    CONCAT(jp.current_salary, ', ', jp.currency, ', ', jp.is_annually_monthly) AS Salary,
    CONCAT(c.certificate_degree_name,', ', c.major, ', ', c.institute_university_name) as degree,
    c.percentage,c.cgpa,c.start_date,c.completion_date,
    l.description,l.is_current_job, l.start_date, l.end_date, l.job_title, l.job_location_city, l.job_location_country,
    l.job_location_state,s.skill_level,
    GROUP_CONCAT(f.skill_set_name) AS skill_set_names  -- Concatenate all skill set names into one column
FROM 
    job_seeker_profile jp
INNER JOIN
    education_detail c ON jp.user_account_id = c.user_account_id
INNER JOIN 
    experience_detail l ON jp.user_account_id = l.user_account_id
INNER JOIN 
    skill_set s ON jp.user_account_id = s.user_account_id
INNER JOIN 
    seeker_skill_set f ON s.skill_set_id = f.id
WHERE 
    jp.user_account_id = 3
GROUP BY 
    jp.user_account_id,jp.first_name,jp.last_name,jp.current_salary,jp.currency,jp.is_annually_monthly,
    c.certificate_degree_name,c.major,c.institute_university_name,c.percentage,c.cgpa,c.start_date,c.completion_date,
    l.description, l.is_current_job, l.start_date, l.end_date, l.job_title, l.job_location_city, l.job_location_country,
    l.job_location_state, s.skill_level;

SELECT
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
    TABLE_NAME = 'skill_set'
    AND TABLE_SCHEMA = 'db3';

ALTER TABLE skill_set
DROP FOREIGN KEY skill_set_ibfk_2;
ALTER TABLE skill_set
ADD CONSTRAINT skill_set_ibfk_2
FOREIGN KEY (skill_set_id)
REFERENCES seeker_skill_set(id)
ON DELETE CASCADE;

SELECT
    KCU.COLUMN_NAME,
    KCU.REFERENCED_TABLE_NAME,
    KCU.REFERENCED_COLUMN_NAME,
    TC.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
INNER JOIN
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
ON
    KCU.TABLE_NAME = TC.TABLE_NAME
    AND KCU.TABLE_SCHEMA = TC.TABLE_SCHEMA
    AND KCU.CONSTRAINT_NAME = TC.CONSTRAINT_NAME
WHERE
    KCU.TABLE_NAME = 'education_detail'
    AND KCU.TABLE_SCHEMA = 'db3'
    AND TC.CONSTRAINT_TYPE = 'FOREIGN KEY';

ALTER TABLE education_detail
DROP FOREIGN KEY education_detail_ibfk_1;
ALTER TABLE education_detail
ADD CONSTRAINT education_detail_ibfk_1
FOREIGN KEY (user_account_id)
REFERENCES db1.user_account(id)
ON DELETE CASCADE;

SELECT
    KCU.COLUMN_NAME,
    KCU.REFERENCED_TABLE_NAME,
    KCU.REFERENCED_COLUMN_NAME,
    TC.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
INNER JOIN
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
ON
    KCU.TABLE_NAME = TC.TABLE_NAME
    AND KCU.TABLE_SCHEMA = TC.TABLE_SCHEMA
    AND KCU.CONSTRAINT_NAME = TC.CONSTRAINT_NAME
WHERE
    KCU.TABLE_NAME = 'experience_detail'
    AND KCU.TABLE_SCHEMA = 'db3'
    AND TC.CONSTRAINT_TYPE = 'FOREIGN KEY';

ALTER TABLE experience_detail
DROP FOREIGN KEY experience_detail_ibfk_1;
ALTER TABLE experience_detail
ADD CONSTRAINT experience_detail_ibfk_1
FOREIGN KEY (user_account_id)
REFERENCES db1.user_account(id)
ON DELETE CASCADE;

SELECT
    KCU.COLUMN_NAME,
    KCU.REFERENCED_TABLE_NAME,
    KCU.REFERENCED_COLUMN_NAME,
    TC.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
INNER JOIN
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
ON
    KCU.TABLE_NAME = TC.TABLE_NAME
    AND KCU.TABLE_SCHEMA = TC.TABLE_SCHEMA
    AND KCU.CONSTRAINT_NAME = TC.CONSTRAINT_NAME
WHERE
    KCU.TABLE_NAME = 'job_seeker_profile'
    AND KCU.TABLE_SCHEMA = 'db3'
    AND TC.CONSTRAINT_TYPE = 'FOREIGN KEY';

ALTER TABLE job_seeker_profile
DROP FOREIGN KEY  job_seeker_profile_ibfk_1;
ALTER TABLE job_seeker_profile
ADD CONSTRAINT  job_seeker_profile_ibfk_1
FOREIGN KEY (user_account_id)
REFERENCES db1.user_account(id)
ON DELETE CASCADE;

SELECT
    KCU.COLUMN_NAME,
    KCU.REFERENCED_TABLE_NAME,
    KCU.REFERENCED_COLUMN_NAME,
    TC.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
INNER JOIN
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
ON
    KCU.TABLE_NAME = TC.TABLE_NAME
    AND KCU.TABLE_SCHEMA = TC.TABLE_SCHEMA
    AND KCU.CONSTRAINT_NAME = TC.CONSTRAINT_NAME
WHERE
    KCU.TABLE_NAME = 'skill_set'
    AND KCU.TABLE_SCHEMA = 'db3'
    AND TC.CONSTRAINT_TYPE = 'FOREIGN KEY';

ALTER TABLE skill_set
DROP FOREIGN KEY  skill_set_ibfk_1;
ALTER TABLE skill_set
ADD CONSTRAINT  skill_set_ibfk_1
FOREIGN KEY (user_account_id)
REFERENCES db1.user_account(id)
ON DELETE CASCADE;

SELECT
    KCU.COLUMN_NAME,
    KCU.REFERENCED_TABLE_NAME,
    KCU.REFERENCED_COLUMN_NAME,
    TC.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
INNER JOIN
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
ON
    KCU.TABLE_NAME = TC.TABLE_NAME
    AND KCU.TABLE_SCHEMA = TC.TABLE_SCHEMA
    AND KCU.CONSTRAINT_NAME = TC.CONSTRAINT_NAME
WHERE
    KCU.TABLE_NAME = 'profile_visit_log'
    AND KCU.TABLE_SCHEMA = 'db3'
    AND TC.CONSTRAINT_TYPE = 'FOREIGN KEY';

ALTER TABLE profile_visit_log 
DROP FOREIGN KEY profile_visit_log_ibfk_1;

ALTER TABLE profile_visit_log 
ADD CONSTRAINT profile_visit_log_ibfk_1 
FOREIGN KEY (seeker_profile_id) 
REFERENCES job_seeker_profile (user_account_id) 
ON DELETE CASCADE;

ALTER TABLE profile_visit_log 
DROP FOREIGN KEY profile_visit_log_ibfk_2;

ALTER TABLE profile_visit_log 
ADD CONSTRAINT profile_visit_log_ibfk_2 
FOREIGN KEY (user_account_id) 
REFERENCES db1.user_account (id) 
ON DELETE CASCADE;
