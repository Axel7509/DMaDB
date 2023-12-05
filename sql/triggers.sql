CREATE TABLE IF NOT EXISTS audit(
    patient varchar(64),
    doctor varchar(64),
    serv_name varchar(64),
    price float,
    date DATE,
    time TIME
);

CREATE TABLE bank(
    doctor varchar(64),
    email varchar(64),
    services_count int DEFAULT 0,
    total_price float DEFAULT 0,
    total_sum float DEFAULT 0
);

CREATE OR REPLACE FUNCTION log_new_ticket()
RETURNS TRIGGER AS
    $$
    DECLARE
    doctor_name TEXT;
    serv_price float;
    BEGIN
        SELECT CONCAT(first_name,' ', last_name) INTO doctor_name
        FROM staff
        WHERE email = NEW.doctor;
        SELECT price INTO serv_price
        FROM service
        WHERE name = NEW.service;
       
        INSERT INTO audit (patient, doctor, serv_name, price, date, time)
        VALUES (NEW.patient, doctor_name, NEW.service, serv_price, NEW.date, NEW.time);
        RETURN NEW;
    END
    $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER log_all_money
    AFTER INSERT ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION log_new_ticket();


CREATE OR REPLACE FUNCTION log_new_ticket()
RETURNS TRIGGER AS
    $$
    DECLARE
    total_sum float;
    serv_count int;
    BEGIN
        SELECT SUM(price) INTO doctor_revenue
        FROM tickets
        WHERE  = NEW.service;
    END
    $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER log_all_money
    AFTER INSERT ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION log_all_money();