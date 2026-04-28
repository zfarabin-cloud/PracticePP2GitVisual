-- functions.sql — TSIS 1: All PL/pgSQL Functions

-- ────────────────────────────────────────────────────────────
-- FROM PRACTICE 8  (return type extended to include new fields)
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INT, p_offset INT)
RETURNS TABLE (
    id         INT,
    username   VARCHAR,
    phone      VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.phone,
        c.email,
        c.birthday,
        g.name        AS group_name,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;


-- ────────────────────────────────────────────────────────────
-- TSIS 1 — Extended search_contacts
-- Matches: username, contacts.phone, email, and every row
--          in the phones table (multiple numbers per contact).
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id          INT,
    username    VARCHAR,
    phone       VARCHAR,
    email       VARCHAR,
    birthday    DATE,
    group_name  VARCHAR,
    extra_phones TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.username,
        c.phone,
        c.email,
        c.birthday,
        g.name                                                            AS group_name,
        STRING_AGG(ph.phone || ' (' || COALESCE(ph.type, '?') || ')', ', ')
                                                                          AS extra_phones
    FROM contacts c
    LEFT JOIN groups  g  ON c.group_id   = g.id
    LEFT JOIN phones  ph ON c.id         = ph.contact_id
    WHERE c.username ILIKE '%' || p_query || '%'
       OR c.email    ILIKE '%' || p_query || '%'
       OR c.phone    ILIKE '%' || p_query || '%'
       OR ph.phone   ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.username, c.phone, c.email, c.birthday, g.name;
END;
$$ LANGUAGE plpgsql;
