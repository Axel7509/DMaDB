SELECT
  ticket.patient,
  CONCAT(staff.first_name,' ', staff.last_name) as doctor,
  ticket.date,
  service.price,
  staff.status
FROM
  ticket
  JOIN service ON ticket.service = service.name
  JOIN staff ON ticket.doctor = staff.email
GROUP BY
	ticket.patient,
  ticket.date,
  service.price,
  staff.status,
  staff.first_name,
	staff.last_name


SELECT
  ticket.patient,
  CONCAT(patient.first_name,' ', patient.last_name) as patient,
  SUM(service.price) as total
FROM
  ticket
  JOIN service ON ticket.service = service.name
  JOIN patient ON ticket.patient = patient.username
GROUP BY
  ticket.patient,
  patient.first_name,
  patient.last_name
HAVING
  SUM(service.price) < 250;


  SELECT
  ticket.patient,
  CONCAT(patient.first_name,' ', patient.last_name) as patient,
  service.price
FROM
  ticket
  JOIN service ON ticket.service = service.name
  JOIN patient ON ticket.patient = patient.username
WHERE
  price = (
    SELECT
      MIN(price)
    FROM
      service
  );


------ JOINS
SELECT
  treatment.description,
  medicines.name,
  treatment.treatment_id
FROM
  treatment
  INNER JOIN treatment_medicines ON treatment.treatment_id = treatment_medicines.treatment_id
  INNER JOIN medicines ON medicines.name = treatment_medicines.medicines_name#


SELECT
  CONCAT(staff.first_name,' ', staff.last_name) as doctor,
  ticket.doctor AS ticket_email,
  ticket.service
FROM
  staff
  LEFT JOIN ticket ON  ticket.doctor=staff.email
GROUP BY
  staff.first_name,
  staff.last_name,
  ticket.doctor,
  ticket.service

SELECT * FROM ticket CROSS JOIN staff;


------ GROUP BY
  SELECT
  ticket.patient,
  CONCAT(patient.first_name,' ', patient.last_name) as patient,
  AVG(service.price) as avg_price
FROM
  ticket
  JOIN service ON ticket.service = service.name
  JOIN patient ON ticket.patient = patient.username
GROUP BY
  ticket.patient,
  patient.first_name,
  patient.last_name
HAVING
  AVG(service.price) < (select avg(price) as avg_price from service);
  

------ PARTITION BY
  SELECT username, first_name, age, 
AVG(age) OVER (PARTITION BY username ) AS user_total
FROM patient

SELECT name, price, 
RANK() OVER (PARTITION BY name ORDER BY price) AS rank
FROM service;


------ UNION
SELECT first_name, last_name 
FROM patient
UNION SELECT first_name, last_name  FROM staff;


------ EXISTS
SELECT first_name, last_name 
FROM patient
WHERE EXISTS (SELECT 1 FROM reviews WHERE rating = 5);


------ INSERT INTO SELECT
CREATE TABLE vip_users (surname VARCHAR(50));

INSERT INTO
  vip_users(surname)
SELECT
  username
FROM
  patient;


------ EXPLAIN
EXPLAIN SELECT
  ticket.patient,
  CONCAT(patient.first_name,' ', patient.last_name) as patient,
  AVG(service.price) as avg_price
FROM
  ticket
  JOIN service ON ticket.service = service.name
  JOIN patient ON ticket.patient = patient.username
GROUP BY
  ticket.patient,
  patient.first_name,
  patient.last_name
HAVING
  AVG(service.price) < (select avg(price) as avg_price from service);


  ------ CASE
SELECT
  id AS reviews_id,
  patient,
  text,
  CASE
    WHEN rating > 3 THEN 'High balelr'
    ELSE 'Low baller'
  END AS review_status
FROM
  reviews


SELECT
  CONCAT(staff.first_name,' ', staff.last_name) as doctor,
  ticket.doctor AS ticket_email,
  ticket.service,
  service.price,
  COUNT(service.name) as services_count,
  SUM(service.price) as total
FROM
  staff
  JOIN ticket ON  ticket.doctor=staff.email
  JOIN service ON  ticket.service = service.name
GROUP BY
  staff.first_name,
  staff.last_name,
  ticket.doctor,
  ticket.service,
  service.price
