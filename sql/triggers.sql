
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

CREATE OR REPLACE TRIGGER log_all_ticket
    AFTER INSERT ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION log_new_ticket();


CREATE OR REPLACE FUNCTION log_new_money()
RETURNS TRIGGER AS
    $$
    DECLARE
    total_sum float;
    serv_count int;
    BEGIN
        SELECT COUNT(service.name) INTO serv_count
        FROM
        staff
            JOIN ticket ON  ticket.doctor=staff.email
            JOIN service ON  ticket.service = service.name
		WHERE email = NEW.doctor
        GROUP BY
            staff.first_name,
            staff.last_name,   
            ticket.doctor;

        SELECT SUM(service.price) INTO total_sum
        FROM
        staff
            JOIN ticket ON  ticket.doctor=staff.email
            JOIN service ON  ticket.service = service.name
		WHERE email = NEW.doctor
        GROUP BY
            staff.first_name,
            staff.last_name,
            ticket.doctor;

        UPDATE bank
            SET services_count = serv_count,
                total_price = total_sum
            WHERE email = NEW.doctor;
        RETURN NEW;
    END
    $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER log_all_money
    AFTER INSERT ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION log_all_money();


CREATE OR REPLACE FUNCTION log_new_patient()
RETURNS TRIGGER AS
    $$
    BEGIN
        INSERT INTO medical_card (patient, gender, height, weight, address)
        VALUES (NEW.username, 'Male', '0', '0','');
        RETURN NEW;
    END
    $$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER log_new_patient
    AFTER INSERT ON patient
    FOR EACH ROW
    EXECUTE FUNCTION log_new_patient();