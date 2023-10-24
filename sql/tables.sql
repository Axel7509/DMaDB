CREATE TABLE patient
(
	username varchar(32) UNIQUE,
    email varchar(64) UNIQUE,
    password varchar(32) NOT NULL UNIQUE,
    first_name varchar(64) NOT NULL,
    last_name varchar(64) NOT NULL,  
	Age INTEGER,
    phone varchar(12) UNIQUE,

    CONSTRAINT patient_usname PRIMARY KEY(username),
    CONSTRAINT min_password_length CHECK ( char_length(password) >= 8 ),
    CONSTRAINT phone_length CHECK ( char_length(phone) >= 12 )
);

CREATE TABLE Reviews
(
    Id SERIAL PRIMARY KEY,
    patient VARCHAR(64),
    text VARCHAR(64),
	rating INTEGER DEFAULT 0,
    FOREIGN KEY (patient) REFERENCES patient (username) ON DELETE CASCADE,
	
	CONSTRAINT rating_check CHECK(rating >= 0 AND rating <= 5)
);

CREATE TABLE medical_card (
    card_id SERIAL PRIMARY KEY,
    patient VARCHAR(60) NOT NULL,
    gender VARCHAR(10) NOT NULL,
	height float4 NOT NULL,
    weight float4 NOT NULL,
    address VARCHAR(255),
	
	FOREIGN KEY (patient) REFERENCES patient (username) ON DELETE CASCADE,
	CONSTRAINT valid_name CHECK ( gender in ('Male', 'Female') )
);


CREATE TABLE staff_status
(
    name varchar(24) UNIQUE PRIMARY KEY,

    CONSTRAINT valid_role CHECK ( name in ('Admin', 'Therapist', 'Surgeon', 'Gynecologist', 'Pediatrician',
                                            'Cardiologist', 'Oncologist', 'Neurologist', 'Orthopedist', 'Ophthalmologist', 'Dantist') )
);


CREATE TABLE staff
(
    email varchar(64) PRIMARY KEY,
    password varchar(32) NOT NULL UNIQUE,
    first_name varchar(64) NOT NULL,
    last_name varchar(64) NOT NULL,
    phone varchar(16) UNIQUE,
    status varchar(64),

    CONSTRAINT min_password_length CHECK ( char_length(password) >= 8 ),
    CONSTRAINT phone_length CHECK ( char_length(phone) >= 12 ),
    CONSTRAINT fk_staff_status FOREIGN KEY (status) REFERENCES staff_status(name) ON DELETE SET NULL
);


CREATE TABLE med_card_doctor (
    med_card_id INT,
    email varchar(64),
    FOREIGN KEY (med_card_id) REFERENCES medical_card(card_id),
    FOREIGN KEY (email) REFERENCES staff(email),
    PRIMARY KEY (med_card_id, email)
);


CREATE TABLE service(
    name varchar(64) UNIQUE,
    description text,
    price float NOT NULL,

    CONSTRAINT service_name PRIMARY KEY(name),
);


CREATE TABLE ticket (
    ticket_id SERIAL,
    time TIME,
    date DATE,
    doctor VARCHAR(64),
    patient VARCHAR(50),
    service VARCHAR(50),
	PRIMARY KEY(ticket_id),
    CONSTRAINT fk_service_status FOREIGN KEY (service) REFERENCES service (name),
    CONSTRAINT fk_patient_status FOREIGN KEY (patient) REFERENCES patient (username) ON DELETE CASCADE,
    CONSTRAINT fk_doctor_status FOREIGN KEY (doctor) REFERENCES staff (email) ON DELETE CASCADE
);


CREATE TABLE disease(
    name varchar(64) UNIQUE,
    description text,

    CONSTRAINT disease_name PRIMARY KEY(name)
);