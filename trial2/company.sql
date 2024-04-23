


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


INSERT INTO company (id, company_name, profile_description, business_stream_id, establishment_date, company_website_url) 
VALUES 
(1001, 'DMART', 'DMart Ready is the mobile application through which our customers order grocery and other utility products. We seeks to be a one-stop shopping destination for the entire family, meeting all their daily household needs offering value for money. A wide selection of home utility products is offered at affordable prices, including groceries, foods, toiletries, beauty products, garments, kitchenware, bed and bath linen, home appliances and much more.', 1, '2002-05-15', 'https://www.dmart.in/'),
(1002, 'ADOBE', 'Changing the world through digital experiences is what Adobe\'s all about. We give everyone from emerging artists to global brands everything they need to design and deliver exceptional digital experiences! We’re passionate about empowering people to create beautiful and powerful images, videos, and apps, and transform how companies interact with customers across every screen.', 2, '1982-11-01', 'https://www.adobe.com/home'),
(1003, 'EATON', 'The primary function of the incumbent is to provide technical support for Electronics Products, including Magnetics products (Inductors, Transformers), Supercapacitors (Coin cells, Cylindrical Cells, Modules), Circuit Protection (Cartridge, THT &SMD Fuses, Fuse Holders, PTC Fuses, ESD Suppressors) & Terminal Blocks (Single row/ Barrier Strip, Euro mag) and select alternative energy-related products.', 2, '1911-05-01', 'https://www.eaton.com/in/en-us.html'),
(1004, 'INFOSYS', 'Infosys is a global leader in next-generation digital services and consulting. Over 300,000 of our people work to amplify human potential and create the next opportunity for people, businesses and communities. With over four decades of experience in managing the systems and workings of global enterprises, we expertly steer clients, in more than 50 countries, as they navigate their digital transformation powered by the cloud.', 2, '1981-02-07', 'https://www.infosys.com/'),
(1005, 'JP MORGAN', 'J.P. Morgan is a leader in financial services, offering solutions to clients in more than 100 countries with one of the most comprehensive global product platforms available. We have been helping our clients to do business and manage their wealth for more than 200 years. Our business has been built upon our core principle of putting our clients\' interests first.', 3, '2000-01-12', 'https://www.jpmorgan.com/global'),
(1006, 'UNACADEMY', 'Take prospect from initial contact phase to qualified phase over the phone. Present product solutions virtually. Generate revenue by counselling prospects and converting them to sales.', 4, '2015-06-30', 'https://unacademy.com/'),
(1007, 'TECH MAHINDRA', 'Tech Mahindra is an Indian multinational information technology services and consulting company. Part of the Mahindra Group, the company is headquartered in Pune and has its registered office in Mumbai. Tech Mahindra has over 146,000 employees across 90 countries', 1, '1986-07-01', 'https://www.techmahindra.com/en-in/?f=2340206617'),
(1008, 'ASIAN PAINTS', 'Asian Paints is India\'s largest paint company and ranks among the top 10 decorative coatings companies in the world with a turnover of Rs.25.6 billion. The company has a reputation in the corporate world for professionalism & fast track growth', 3, '1942-08-02', 'https://www.asianpaints.com/'),
(1009, 'COGNIZANT', 'Cognizant (Nasdaq: CTSH) engineers modern businesses. We help our clients modernize technology, reimagine processes and transform experiences so they can stay ahead in our fast-changing world. Together, we\'re improving everyday life', 4, '1994-01-26', 'www.cognizant.com'),
(1010, 'GOLDMAN SACHS', 'The Goldman Sachs Group, Inc. is an American multinational investment bank and financial services company. Founded in 1869, Goldman Sachs is headquartered in Lower Manhattan in New York City, with regional headquarters in many international financial centers', 3, '1869-02-05', 'https://www.goldmansachs.com/'),
(1011, 'BARCLAYS', 'At Barclays, each day is about being more – as a professional, and as a person. ‘Be More @ Barclays’ represents our core promise to all current and future employees. It’s the characteristic that we want to be associated with as an employer, and at the heart of every employee experience. We empower our colleagues to Be More Globally Connected, working on international projects that improve the way millions of customers handle their finances', 2, '1690-11-17', 'https://home.barclays/'),
(1012, 'BNY MELLON', 'BNY Mellon is a global investments company dedicated to helping its clients manage and service their financial assets throughout the investment lifecycle. Whether providing financial services for institutions, corporations or individual investors, BNY Mellon delivers informed investment management and investment services in 35 countries and more than 100 markets. As of Dec. 31, 2014, BNY Mellon had $28.5 trillion in assets under custody and/or administration, and $1.7 trillion in assets under management.', 3, '2007-07-01', 'https://www.bnymellon.com/apac/en.html'),
(1013, 'GOOGLE', 'At Google Operations Center, we provide caring and knowledgeable support for Google users and customers. From troubleshooting product issues to providing around-the-clock advertiser assistance, you can be part of the teams that help Google users and customers solve problems and accomplish their goals.', 3, '1998-09-04', 'https://www.google.com/'),
(1014, 'MASTERCARD', 'Mastercard is a global leader in technology and payments, committed to empowering businesses and economies to thrive. Our Global People Operations & Insights team is at the forefront of leveraging data to drive strategic decisions about our most valuable asset our talent.', 2, '1966-02-12', 'https://www.mastercard.co.in/en-in.html'),
(1015, 'INTUIT', 'Intuit is committed to diversity in the workplace and strives to support candidates with disabilities. We provide reasonable accommodation to known physical or mental limitations of otherwise qualified employees or applicants for employment, including providing alternative methods of applying for employment for individuals unable to submit an application through this site because of a disability', 3, '1983-01-01', 'https://www.intuit.com/in/');



INSERT INTO company_image (image_id, company_id, image_url) VALUES
(1, 1001, 'https://th.bing.com/th/id/OIP.gK4X1f64aEL2ymNQqAfGDAHaF0?rs=1&pid=ImgDetMain'),
(2, 1002, 'https://brandslogos.com/wp-content/uploads/images/large/adobe-logo-1.png'),
(3, 1003, 'https://th.bing.com/th/id/OIP.56Hn_izUbE9yY8XpPQKjOwHaHa?rs=1&pid=ImgDetMain'),
(4, 1004, 'https://static.vecteezy.com/system/resources/previews/024/806/527/large_2x/infosys-logo-transparent-free-png.png'),
(5, 1005, 'https://logos-world.net/wp-content/uploads/2021/02/JP-Morgan-Chase-Emblem.png'),
(6, 1006, 'https://image.pitchbook.com/OnPYJTryF0XCa2zCxvsx0PW4zse1625497501143_200x200'),
(7, 1007, 'https://example.com/tech_mahindra_logo.png'),
(8, 1008, 'https://example.com/asian_paints_logo.png'),
(9, 1009, 'https://example.com/cognizant_logo.png'),
(10, 1010, 'https://example.com/goldman_sachs_logo.png'),
(11, 1011, 'https://example.com/barclays_logo.png'),
(12, 1012, 'https://example.com/bny_mellon_logo.png'),
(13, 1013, 'https://th.bing.com/th/id/OIP.m0MnLn7tpLOVay33rPxirQHaEK?rs=1&pid=ImgDetMain'),
(14, 1014, 'https://logos-world.net/wp-content/uploads/2020/09/Mastercard-Logo-2016-2020.png'),
(15, 1015, 'https://example.com/intuit_logo.png'),
(16, 1016, 'https://th.bing.com/th/id/OIP.HKBYwPQG8tO5TI6xTpuSzAHaI_?rs=1&pid=ImgDetMain');