-- procedures.sql — TSIS 1: All Stored Procedures

-- ════════════════════════════════════════════════════════════
-- FROM PRACTICE 8  (unchanged)
-- ════════════════════════════════════════════════════════════

-- Upsert a single contact
CREATE OR REPLACE PROCEDURE insert_or_update_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO contacts (username, phone) VALUES (p_name, p_phone)
    ON CONFLICT (phone) DO UPDATE SET username = EXCLUDED.username;
END;
$$;

-- Delete contact by exact name or phone
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_target VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE username = p_target OR phone = p_target;
END;
$$;

-- Bulk insert with loop + validation (phones must be numeric and > 5 chars)
CREATE OR REPLACE PROCEDURE bulk_insert_with_validation(
    p_names  VARCHAR[],
    p_phones VARCHAR[],
    OUT p_errors TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    p_errors := '';
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) > 5 THEN
            INSERT INTO contacts (username, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone) DO UPDATE SET username = EXCLUDED.username;
        ELSE
            p_errors := p_errors || 'Invalid: ' || p_names[i]
                        || ' (' || p_phones[i] || '); ';
        END IF;
    END LOOP;
END;
$$;


-- ════════════════════════════════════════════════════════════
-- NEW IN TSIS 1
-- ════════════════════════════════════════════════════════════

-- Add a phone number (with type) to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR   -- 'home' | 'work' | 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id
    FROM contacts
    WHERE username = p_contact_name
    LIMIT 1;

    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;


-- Move a contact to a group; create the group if it does not exist
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id   INT;
    v_contact_id INT;
BEGIN
    -- Ensure the group exists
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id  FROM groups   WHERE name     = p_group_name;
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;
