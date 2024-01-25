CREATE OR REPLACE PROCEDURE change_review(
    select_id integer,
    new_text text,
    new_rating int
)
AS
    $$
        BEGIN
            UPDATE reviews
            SET
                text = COALESCE(new_text, text),
                rating = COALESCE(new_rating, rating)
            WHERE reviews.id = select_id;
            COMMIT;
        END;
    $$
LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE add_review(
    select_name text,
    new_text text,
    new_rating int
)
AS
    $$
        BEGIN
            INSERT INTO reviews (patient, text, rating)
            VALUES (select_name, new_text, new_rating);
            COMMIT;
        END;
    $$
LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE update_med_card(
    select_patient text,
    new_gender text,
    new_height float4,
    new_weight float4,
    new_address text
)
AS
    $$
        BEGIN
            UPDATE medical_card
            SET
               gender = COALESCE(new_gender, gender),
               height = COALESCE(new_height, height),
               weight = COALESCE(new_weight, weight),
               address = COALESCE(new_address, address)
            WHERE select_patient = medical_card.patient;
            COMMIT;
        END;
    $$
LANGUAGE plpgsql;
