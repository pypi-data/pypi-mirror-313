CREATE EXTENSION IF NOT EXISTS clickhouse_fdw;
CREATE SERVER IF NOT EXISTS {server_name} FOREIGN DATA WRAPPER clickhouse_fdw OPTIONS(dbname %s, host %s, port %s);
-- NOTE user password must be set by an admin from the cheriff UI, first time it just creates the user with a random password
DO
$do$
BEGIN
   IF NOT EXISTS (
        SELECT
            FROM
                pg_catalog.pg_roles  -- SELECT list can be empty for this
            WHERE
                rolname = %s
    ) THEN
        REVOKE CREATE ON SCHEMA public FROM public;
        CREATE USER {rolename} WITH PASSWORD %s;
        REVOKE CONNECT ON DATABASE {database_name} FROM public;
        GRANT CONNECT ON DATABASE {database_name} TO {rolename};
   END IF;
END
$do$;
CREATE USER MAPPING IF NOT EXISTS FOR postgres SERVER {server_name} OPTIONS (user %s, password %s);
CREATE USER MAPPING IF NOT EXISTS FOR {rolename} SERVER {server_name} OPTIONS (user %s, password %s);
