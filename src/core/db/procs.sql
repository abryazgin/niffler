\c niffler

CREATE OR REPLACE FUNCTION create_user(
    iUSER_NAME VARCHAR,
    iTOKEN_CODE VARCHAR
) RETURNS INTEGER as $$
DECLARE vUSER_ID users.id%TYPE;
DECLARE vGROUP_ID groups.id%TYPE;
BEGIN

    INSERT INTO users (name, role_id) VALUES (iUSER_NAME, 2) RETURNING id INTO vUSER_ID;
    INSERT INTO tokens (user_id, code) VALUES (vUSER_ID,iTOKEN_CODE);
    INSERT INTO groups (name) VALUES (iUSER_NAME) RETURNING id INTO vGROUP_ID;
    INSERT INTO usergroup (user_id, group_id) VALUES (vUSER_ID, vGROUP_ID);

    RETURN vUSER_ID;
END;
$$ language plpgsql;