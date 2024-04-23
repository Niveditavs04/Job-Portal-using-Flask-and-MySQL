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

INSERT INTO seeker_skill_set (id, skill_set_name) VALUES 
(1, 'Language Proficiency'),
(2, 'Employee Relations Mnagement'),
(3, 'Coaching'),
(4, 'Performance Management'),
(5, 'Communication Skills'),
(6, 'HRIS (Human Resources Information System)'),
(7, 'Talent Acquisition'),
(8, 'Payroll Management'),
(9, 'Organizational Development'),
(10, 'Change Management'),
(11, 'Technical Support'),
(12, 'Software Development'),
(13, 'Database Management'),
(14, 'Network Administration'),
(15, 'Cybersecurity'),
(16, 'Data Analysis'),
(17, 'Financial Reporting'),
(18, 'Auditing'),
(19, 'Taxation'),
(20, 'Financial Analysis');

