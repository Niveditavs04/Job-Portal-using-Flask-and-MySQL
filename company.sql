


CREATE TABLE business_stream (
    id INT PRIMARY KEY,
    business_stream_name VARCHAR(255) NOT NULL
);
CREATE TABLE company (
    id INT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    profile_description TEXT,
    business_stream_id INT,
    establishment_date DATE,
    company_website_url VARCHAR(255) NOT NULL,
    FOREIGN KEY (business_stream_id) REFERENCES business_stream(id)
);

CREATE TABLE company_image (
    image_id INT PRIMARY KEY,
    company_id INT,
    image_url VARCHAR(255) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company(id)
);