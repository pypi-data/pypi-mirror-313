DROP USER MAPPING IF EXISTS FOR postgres SERVER {server_name};
DROP USER MAPPING IF EXISTS FOR {rolename} SERVER {server_name};
REASSIGN OWNED BY {rolename} TO postgres;
DROP OWNED BY {rolename};
DROP USER IF EXISTS {rolename};
DROP SERVER IF EXISTS {server_name} CASCADE;
DROP EXTENSION IF EXISTS clickhouse_fdw;
