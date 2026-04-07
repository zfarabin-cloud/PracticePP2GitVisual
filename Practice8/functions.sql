CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE (id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT * FROM contacts ORDER BY id LIMIT p_limit OFFSET p_offset;
END; $$ LANGUAGE plpgsql;

-- Функция для поиска по паттерну
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE (id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM contacts 
    WHERE username ILIKE '%' || p_pattern || '%' 
       OR phone LIKE '%' || p_pattern || '%';
END; $$ LANGUAGE plpgsql;