CREATE OR REPLACE PROCEDURE insert_or_update_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO contacts (username, phone) VALUES (p_name, p_phone)
    ON CONFLICT (phone) DO UPDATE SET username = EXCLUDED.username;
END; $$;

-- Процедура удаления
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_target VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE username = p_target OR phone = p_target;
END; $$;

-- Процедура массовой вставки с проверкой (ДЛЯ ЗАДАНИЯ С ЦИКЛОМ)
CREATE OR REPLACE PROCEDURE bulk_insert_with_validation(
    p_names VARCHAR[], 
    p_phones VARCHAR[],
    OUT p_errors TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    p_errors := '';
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Простая проверка: номер должен состоять только из цифр и быть длиннее 5 символов
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) > 5 THEN
            INSERT INTO contacts (username, phone) 
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone) DO UPDATE SET username = EXCLUDED.username;
        ELSE
            p_errors := p_errors || 'Invalid: ' || p_names[i] || '(' || p_phones[i] || '); ';
        END IF;
    END LOOP;
END; $$;