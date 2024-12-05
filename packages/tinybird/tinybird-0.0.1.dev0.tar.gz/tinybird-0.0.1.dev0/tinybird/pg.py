import base64
import hashlib
import hmac
import logging
import secrets
import stringprep
import unicodedata
from os import path
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional

import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.sql import SQL, Identifier

from tinybird.ch import (
    CHException,
    ch_create_view,
    ch_drop_view,
    ch_table_columns,
    ch_table_columns_sync,
    ch_table_details,
    ch_table_details_async,
)
from tinybird.ch_utils.engine import TableDetails
from tinybird.datasource import Datasource
from tinybird.pipe import Pipe
from tinybird.sql_template import SQLTemplateCustomError, SQLTemplateException
from tinybird.syncasync import sync_to_async
from tinybird.tornado_template import ParseError, UnClosedIfError
from tinybird_shared.redis_client.redis_client import retry_sync

if TYPE_CHECKING:  # pragma: no cover
    from tinybird.user import User as Workspace

here = path.abspath(path.dirname(__file__))
MIN_POOL_SIZE = 1
MAX_POOL_SIZE = 2
ADMIN_ROLE = "admin"
USER_ROLE = "user"

TYPES_CONVERSION = {
    "Int8": "INT2",
    "UInt8": "INT2",
    "Int16": "INT2",
    "UInt16": "INT4",
    "Int32": "INT4",
    "UInt32": "INT8",
    "Int64": "INT8",
    "UInt64": "NUMERIC",
    "Int128": "NUMERIC",
    "UInt128": "NUMERIC",
    "Int256": "NUMERIC",
    "UInt256": "NUMERIC",
    "Float32": "REAL",
    "Float64": "DOUBLE PRECISION",
    "Decimal": "NUMERIC",
    "Boolean": "BOOLEAN",
    "Bool": "BOOLEAN",
    "String": "TEXT",
    "DateTime": "TIMESTAMP",
    "Date": "DATE",
    "IPv6": "inet",
    "IPv4": "inet",
    "UUID": "UUID",
    "Nothing": "TEXT",
}


class ParseTypeException(Exception):
    pass


class EncryptPassword:
    """
    Generate the password hashes / verifiers for use in PostgreSQL

    How to use this:

    pw = EncryptPassword(
        user="username",
        password="securepassword",
        algorithm="scram-sha-256",
    )
    print(pw.encrypt())

    The output of the ``encrypt`` function can be stored in PostgreSQL in the
    password clause, e.g.

        ALTER ROLE username PASSWORD {pw.encrypt()};

    where you safely interpolate it in with a quoted literal, of course :)
    """

    ALGORITHMS = {
        "md5": {
            "encryptor": "_encrypt_md5",
            "digest": hashlib.md5,
            "defaults": {},
        },
        "scram-sha-256": {
            "encryptor": "_encrypt_scram_sha_256",
            "digest": hashlib.sha256,
            "defaults": {
                "salt_length": 16,
                "iterations": 4096,
            },
        },
    }
    # List of characters that are prohibited to be used per PostgreSQL-SASLprep
    SASLPREP_STEP3 = (
        stringprep.in_table_a1,  # PostgreSQL treats this as prohibited
        stringprep.in_table_c12,
        stringprep.in_table_c21_c22,
        stringprep.in_table_c3,
        stringprep.in_table_c4,
        stringprep.in_table_c5,
        stringprep.in_table_c6,
        stringprep.in_table_c7,
        stringprep.in_table_c8,
        stringprep.in_table_c9,
    )

    def __init__(self, user, password, algorithm="scram-sha-256", **kwargs):
        self.user = user
        self.password = password
        self.algorithm = algorithm
        self.salt = None
        self.encrypted_password = None
        self.kwargs = kwargs

    def encrypt(self):
        try:
            algorithm = self.ALGORITHMS[self.algorithm]
        except KeyError:
            raise Exception('algorithm "{}" not supported'.format(self.algorithm))
        kwargs = algorithm["defaults"].copy()  # type: ignore[attr-defined]
        kwargs.update(self.kwargs)
        return getattr(self, algorithm["encryptor"])(algorithm["digest"], **kwargs)  # type: ignore[call-overload]

    def _bytes_xor(self, a, b):
        """XOR two bytestrings together"""
        return bytes(a_i ^ b_i for a_i, b_i in zip(a, b, strict=True))

    def _encrypt_md5(self, digest, **kwargs):
        self.encrypted_password = b"md5" + digest(
            self.password.encode("utf-8") + self.user.encode("utf-8")
        ).hexdigest().encode("utf-8")
        return self.encrypted_password

    def _encrypt_scram_sha_256(self, digest, **kwargs):
        # requires SASL prep
        # password = SASLprep
        iterations = kwargs["iterations"]
        salt_length = kwargs["salt_length"]
        salted_password = self._scram_sha_256_generate_salted_password(self.password, salt_length, iterations, digest)
        client_key = hmac.HMAC(salted_password, b"Client Key", digest)
        stored_key = digest(client_key.digest()).digest()
        server_key = hmac.HMAC(salted_password, b"Server Key", digest)
        self.encrypted_password = (
            self.algorithm.upper().encode("utf-8")
            + b"$"
            + ("{}".format(iterations)).encode("utf-8")
            + b":"
            + base64.b64encode(self.salt)  # type: ignore[arg-type]
            + b"$"
            + base64.b64encode(stored_key)
            + b":"
            + base64.b64encode(server_key.digest())
        )
        return self.encrypted_password

    def _normalize_password(self, password):
        """Normalize the password using PostgreSQL-flavored SASLprep. For reference:

        https://git.postgresql.org/gitweb/?p=postgresql.git;a=blob;f=src/common/saslprep.c
        using the `pg_saslprep` function

        Implementation borrowed from asyncpg implementation:
        https://github.com/MagicStack/asyncpg/blob/master/asyncpg/protocol/scram.pyx#L263
        """
        normalized_password = password

        # if the password is an ASCII string or fails to encode as an UTF8
        # string, we can return
        try:
            normalized_password.encode("ascii")
        except UnicodeEncodeError:
            pass
        else:
            return normalized_password

        # Step 1 of SASLPrep: Map. Per the algorithm, we map non-ascii space
        # characters to ASCII spaces (\x20 or \u0020, but we will use ' ') and
        # commonly mapped to nothing characters are removed
        # Table C.1.2 -- non-ASCII spaces
        # Table B.1 -- "Commonly mapped to nothing"
        normalized_password = "".join(
            [" " if stringprep.in_table_c12(c) else c for c in normalized_password if not stringprep.in_table_b1(c)]
        )

        # If at this point the password is empty, PostgreSQL uses the original
        # password
        if not normalized_password:
            return password

        # Step 2 of SASLPrep: Normalize. Normalize the password using the
        # Unicode normalization algorithm to NFKC form
        normalized_password = unicodedata.normalize("NFKC", normalized_password)

        # If the password is not empty, PostgreSQL uses the original password
        if not normalized_password:
            return password

        # Step 3 of SASLPrep: Prohobited characters. If PostgreSQL detects any
        # of the prohibited characters in SASLPrep, it will use the original
        # password
        # We also include "unassigned code points" in the prohibited character
        # category as PostgreSQL does the same
        for c in normalized_password:
            if any([in_prohibited_table(c) for in_prohibited_table in self.SASLPREP_STEP3]):
                return password

        # Step 4 of SASLPrep: Bi-directional characters. PostgreSQL follows the
        # rules for bi-directional characters laid on in RFC3454 Sec. 6 which
        # are:
        # 1. Characters in RFC 3454 Sec 5.8 are prohibited (C.8)
        # 2. If a string contains a RandALCat character, it cannot containy any
        #    LCat character
        # 3. If the string contains any RandALCat character, an RandALCat
        #    character must be the first and last character of the string
        # RandALCat characters are found in table D.1, whereas LCat are in D.2
        if any([stringprep.in_table_d1(c) for c in normalized_password]):
            # if the first character or the last character are not in D.1,
            # return the original password
            if not (stringprep.in_table_d1(normalized_password[0]) and stringprep.in_table_d1(normalized_password[-1])):
                return password

            # if any characters are in D.2, use the original password
            if any([stringprep.in_table_d2(c) for c in normalized_password]):
                return password

        # return the normalized password
        return normalized_password

    def _scram_sha_256_generate_salted_password(self, password, salt_length, iterations, digest):
        """This follows the "Hi" algorithm specified in RFC5802"""
        # first, need to normalize the password using PostgreSQL-flavored SASLprep
        normalized_password = self._normalize_password(password)
        # convert the password to a binary string - UTF8 is safe for SASL (though there are SASLPrep rules)
        p = normalized_password.encode("utf8")
        # generate a salt
        self.salt = secrets.token_bytes(salt_length)
        # the initial signature is the salt with a terminator of a 32-bit string ending in 1
        ui = hmac.new(p, self.salt + b"\x00\x00\x00\x01", digest)
        # grab the initial digest
        u = ui.digest()
        # for X number of iterations, recompute the HMAC signature against the password
        # and the latest iteration of the hash, and XOR it with the previous version
        for _ in range(iterations - 1):
            ui = hmac.new(p, ui.digest(), hashlib.sha256)
            # this is a fancy way of XORing two byte strings together
            u = self._bytes_xor(u, ui.digest())
        return u


class PGPool:
    __instance = None
    pools: Dict[str, Dict[str, ThreadedConnectionPool]] = {}

    # this is a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            # Put any initialization here.
            cls.__instance.pools = {}
        return cls.__instance

    def fetch(self, user, role=ADMIN_ROLE):
        if user["database"] not in self.pools:
            admin_pool = ThreadedConnectionPool(MIN_POOL_SIZE, MAX_POOL_SIZE, **user.pg_metadata(ADMIN_ROLE))
            self.pools[user["database"]] = {ADMIN_ROLE: admin_pool}

        if role not in self.pools[user["database"]]:
            pool = ThreadedConnectionPool(MIN_POOL_SIZE, MAX_POOL_SIZE, **user.pg_metadata(USER_ROLE))
            self.pools[user["database"]][role] = pool

        conn = self.pools[user["database"]][role].getconn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if not cursor:
            conn.close()
            raise Exception("PGPool cannot create cursor!!")
        return conn, cursor

    def put(self, user, conn, role=ADMIN_ROLE):
        self.pools[user["database"]][role].putconn(conn)

    def close_all(self, user=None, role=USER_ROLE):
        if user:
            user_key = user["database"]
            if user_key in self.pools and role in self.pools[user_key]:
                self.pools[user_key][role].closeall()
                del self.pools[user_key][role]
        else:
            for user_key in list(self.pools):
                for role in list(self.pools[user_key]):
                    self.pools[user_key][role].closeall()
                    del self.pools[user_key][role]
                del self.pools[user_key]


def check_enabled_pg(func):
    def check(self, *args, **kwargs):
        if not self.user["enabled_pg"]:
            return False
        result = func(self, *args, **kwargs)
        return result or True

    return check


class PGService:
    """
    This class allows to perform operations with a postgres database instance.
    It's handy to setup the postgresql connector, sync datasources and endpoints as foreign tables
    """

    def __init__(self, user: "Workspace"):
        self.user = user

    @retry_sync((psycopg2.errors.QueryCanceled, psycopg2.errors.OperationalError), tries=2, delay=0, backoff=2.5)
    def execute(self, query, params=None, role=ADMIN_ROLE, autocommit=False, **kwargs):
        conn = cursor = None
        try:
            result = None
            conn, cursor = PGPool().fetch(self.user, role=role)
            if autocommit:
                conn.autocommit = True
            if kwargs:
                query = SQL(query).format(**kwargs)
            cursor.execute(query, params) if params else cursor.execute(query)
            try:
                result = cursor.fetchall()
            except psycopg2.ProgrammingError:
                # no results to fetch
                pass
            if not autocommit:
                conn.commit()
            return result
        except (
            SyntaxError,
            CHException,
            SQLTemplateException,
            SQLTemplateCustomError,
            ParseError,
            UnClosedIfError,
            ValueError,
        ) as e:
            logging.warning(str(e))
        except Exception as e:
            logging.exception(f"error on execute Postgres query: {e}", extra={"sql": query})
            if not autocommit and conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
                PGPool().put(self.user, conn, role=role)

    @check_enabled_pg
    def setup_database(self, sync=False):
        try:
            logging.info(f"setup database {self.get_database_name()}")
            self.create_database()
            self.setup_fdw()
            if sync:
                self.sync_foreign_tables()
            logging.info(f"end setup database {self.get_database_name()}")
        except (
            SyntaxError,
            CHException,
            SQLTemplateException,
            SQLTemplateCustomError,
            ParseError,
            UnClosedIfError,
            ValueError,
        ) as e:
            logging.warning(str(e))
        except Exception as e:
            logging.exception(f"error on database setup: {e}")
            raise e

    @check_enabled_pg
    def create_database(self):
        try:
            exists_sql = "SELECT FROM pg_database WHERE datname = %s"
            result = self.execute(exists_sql, autocommit=True, params=[self.get_database_name()])

            if len(result) == 0:
                sql = "CREATE DATABASE {database_name};"
                self.execute(sql, autocommit=True, database_name=Identifier(self.get_database_name()))
        except Exception as e:
            logging.exception(f"error on create database: {e}")
            raise e

    @check_enabled_pg
    def setup_fdw(self):
        try:
            with open(path.join(here, "sql", "setup_pg_database.sql"), "r") as file:
                setup_database_sql = file.read()
            database_name = self.get_database_name()
            server_name = self.get_fdw_server_name()
            ch_host = self.get_pg_foreign_server()
            ch_port = self.get_pg_foreign_server_port()
            ch_user = self.get_ch_user()
            pg_user = self.get_pg_rolename()
            ch_password = self.get_ch_password()
            pg_password = self.get_pg_password()

            self.execute(
                setup_database_sql,
                params=[
                    database_name,
                    ch_host,
                    ch_port,
                    pg_user,
                    pg_password,
                    ch_user,
                    ch_password,
                    ch_user,
                    ch_password,
                ],
                role=USER_ROLE,
                server_name=Identifier(server_name),
                rolename=Identifier(pg_user),
                database_name=Identifier(database_name),
            )
        except Exception as e:
            logging.exception(f"error on setup fdw: {e}")
            raise e

    @check_enabled_pg
    def drop_database(self):
        try:
            logging.info(f"drop database {self.get_database_name()}")
            self.drop_pg_objects()
            self.do_drop_database()
            logging.info(f"end drop database {self.get_database_name()}")
        except Exception as e:
            logging.exception(f"error on drop database: {e}")

    @check_enabled_pg
    def drop_pg_objects(self):
        try:
            with open(path.join(here, "sql", "drop_pg_objects.sql"), "r") as file:
                drop_database_sql = file.read()
            database_name = self.get_database_name()
            server_name = self.get_fdw_server_name()
            pg_user = self.get_pg_rolename()

            self.execute(
                drop_database_sql,
                role=USER_ROLE,
                server_name=Identifier(server_name),
                rolename=Identifier(pg_user),
                database_name=Identifier(database_name),
            )
        except Exception as e:
            logging.exception(f"error on drop pg objects: {e}")

    @check_enabled_pg
    def do_drop_database(self):
        try:
            with open(path.join(here, "sql", "prepare_drop_pg_database.sql"), "r") as file:
                drop_database_sql = file.read()
            database_name = self.get_database_name()
            self.execute(
                drop_database_sql, autocommit=True, database_name=Identifier(database_name), params=[database_name]
            )

            PGPool().close_all(user=self.user)
            sql = "DROP DATABASE IF EXISTS {database_name};"
            self.execute(sql, autocommit=True, database_name=Identifier(database_name))
        except Exception as e:
            logging.exception(f"error on do drop database: {e}")

    @check_enabled_pg
    def sync_foreign_tables(self, datasources: Optional[List[Datasource]] = None):
        logging.info(f"sync foreign tables {self.get_database_name()}")
        datasources = datasources if datasources else self.user.get_datasources()
        for datasource in datasources:
            try:
                logging.info(f"create foreign table {datasource.name}")
                self.create_foreign_table(datasource.id, datasource.name)
                logging.info(f"end create foreign table {datasource.name}")
            except Exception as e:
                logging.exception(f"error on create foreign table {datasource.name}: {e}")

    async def sync_foreign_tables_async(
        self,
        datasources: Optional[Iterable[Datasource]] = None,
        pipes: Optional[Iterable[Pipe]] = None,
    ) -> None:
        if not self.user["enabled_pg"]:
            return
        logging.info(f"sync foreign tables {self.get_database_name()}")
        datasources = datasources if datasources else self.user.get_datasources()
        for datasource in datasources:
            try:
                logging.info(f"create foreign table {datasource.name}")
                await self.create_foreign_table_async(datasource.id, datasource.name)
                logging.info(f"end create foreign table {datasource.name}")
            except Exception as e:
                logging.exception(f"error on create foreign table {datasource.name}: {e}")

        pipes = pipes if pipes else self.user.get_pipes()
        for pipe in pipes:
            try:
                if pipe.is_published():
                    await self.on_endpoint_changed(pipe)
            except Exception as e:
                logging.exception(f"error on create foreign table {pipe.name}: {e}")

        try:
            await self.drop_non_existent_pg_tables()
        except Exception as e:
            logging.warning(f"drop_non_existent_pg_tables error {str(e)}")

    async def drop_non_existent_pg_tables(self):
        foreign_tables_sql = "SELECT relname FROM pg_class WHERE relkind = 'f';"
        result = self.execute(foreign_tables_sql, autocommit=True, role=USER_ROLE)
        for res in result:
            table_name = res["relname"]
            if not self.user.get_resource(table_name):
                try:
                    logging.info(f"drop_non_existent_pg_tables {table_name}")
                    await sync_to_async(self.drop_foreign_table)(table_name)
                    logging.info(f"drop_non_existent_pg_tables dropped {table_name}")
                except Exception as e:
                    logging.warning(f"drop_non_existent_pg_tables error {table_name} - {str(e)}")

    @check_enabled_pg
    def create_foreign_table(self, table_name, view_name):
        details = ch_table_details(
            table_name=table_name, database_server=self.user["database_server"], database=self.user["database"]
        )
        columns = ch_table_columns_sync(self.user["database_server"], self.user["database"], table_name)
        return self.do_create_foreign_table(columns, table_name, view_name, details)

    async def create_foreign_table_async(self, table_name, view_name):
        if not self.user["enabled_pg"]:
            return
        details = await ch_table_details_async(
            table_name=table_name, database_server=self.user["database_server"], database=self.user["database"]
        )
        columns = await ch_table_columns(self.user["database_server"], self.user["database"], table_name)
        return self.do_create_foreign_table(columns, table_name, view_name, details)

    def do_create_foreign_table(self, columns, table_name, view_name, details: TableDetails):
        if not columns:
            return

        columns_sql = []
        for column in columns:
            nullable = "" if self.is_nullable(column["type"]) else "NOT NULL"
            column_name = column["name"]
            try:
                column_type = self.parse_type(column["type"])
            except ParseTypeException as e:
                message = f"Failed to map column type '{column['type']}' from table '{table_name}': {e}"
                logging.warning(message)
                column_type = "TEXT"
            except Exception as e:
                raise e
            columns_sql.append(f'"{column_name}" {column_type} {nullable}')

        create_sql = f"""
            CREATE FOREIGN TABLE IF NOT EXISTS "{table_name}"
                ({(', ').join(columns_sql).strip()})
                SERVER "{self.get_fdw_server_name()}"
                OPTIONS(table_name '{table_name}', engine '{details.original_engine}')
        """
        sql = f"""
            DROP FOREIGN TABLE IF EXISTS "{table_name}" CASCADE;
            {create_sql}
        """

        self.execute(sql, role=USER_ROLE)
        self.execute(f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM {table_name};", role=USER_ROLE)
        grant_sql = SQL("GRANT SELECT ON ALL TABLES IN SCHEMA public TO {rolename};").format(
            rolename=Identifier(self.get_pg_rolename())
        )
        self.execute(grant_sql, role=USER_ROLE)
        return create_sql

    @check_enabled_pg
    def drop_foreign_table(self, name):
        try:
            logging.info(f"drop foreign table {name}")
            sql = "DROP FOREIGN TABLE IF EXISTS {table_name} CASCADE;"
            self.execute(sql, autocommit=True, role=USER_ROLE, table_name=Identifier(name))
            logging.info(f"end drop foreign table {name}")
        except Exception as e:
            logging.exception(f"error on drop foreign table {name}: {e}")

    @check_enabled_pg
    def alter_datasource_name(self, old_name, new_name):
        try:
            logging.info(f"alter foreign table {old_name} to {new_name}")
            sql = "ALTER VIEW {old_name} RENAME TO {new_name};"
            self.execute(
                sql, autocommit=True, role=USER_ROLE, old_name=Identifier(old_name), new_name=Identifier(new_name)
            )
            logging.info(f"end alter foreign table {old_name} to {new_name}")
        except Exception as e:
            logging.exception(f"error on alter foreign table view {old_name}: {e}")

    @check_enabled_pg
    def change_password(self, password):
        try:
            pg_user = self.get_pg_rolename()
            password = self.encrypt(pg_user, password)
            logging.info(f"change password {pg_user}")
            sql = "ALTER ROLE {rolename} WITH PASSWORD %s;"
            self.execute(sql, autocommit=True, role=USER_ROLE, params=[password], rolename=Identifier(pg_user))
            logging.info(f"end change password {pg_user}")
        except Exception as e:
            logging.exception(f"error changing password for user {pg_user}: {e}")

    async def on_endpoint_changed(self, pipe: Pipe):
        try:
            if not self.user["enabled_pg"]:
                return
            if pipe.endpoint:
                logging.info(f"on endpoint changed {pipe.name}")
                await ch_drop_view(
                    self.user["database_server"], self.user["database"], pipe.id, cluster=self.user.cluster
                )
                await sync_to_async(self.drop_foreign_table)(pipe.id)
                try:
                    sql = pipe.pipeline.get_sql_for_node(pipe.endpoint)
                    sql = self.user.replace_tables(sql)
                except (
                    SyntaxError,
                    CHException,
                    SQLTemplateException,
                    SQLTemplateCustomError,
                    ParseError,
                    UnClosedIfError,
                    ValueError,
                ) as e:
                    logging.warning(str(e))
                    return
                except Exception as e:
                    logging.warning(
                        f"error on endpoint change {pipe.name}: {e}. Endpoints with templates cannot be published as pg tables so we ignore this type of exceptions."
                    )
                    return
                await ch_create_view(
                    self.user["database_server"], self.user["database"], pipe.id, sql, cluster=self.user.cluster
                )
                await self.create_foreign_table_async(pipe.id, pipe.name)
                logging.info(f"end on endpoint changed {pipe.name}")
            else:
                logging.info(f"on endpoint changed - drop {pipe.name}")
                await ch_drop_view(
                    self.user["database_server"], self.user["database"], pipe.id, cluster=self.user.cluster
                )
                await sync_to_async(self.drop_foreign_table)(pipe.id)
                logging.info(f"end on endpoint changed - drop {pipe.name}")
        except (CHException, ValueError) as e:
            logging.warning(str(e))
        except Exception as e:
            logging.exception(f"error on endpoint change {pipe.name}: {e}")

    async def on_pipe_deleted(self, pipe: Pipe):
        try:
            if not self.user["enabled_pg"]:
                return
            logging.info(f"on pipe deleted {pipe.name}")
            await ch_drop_view(self.user["database_server"], self.user["database"], pipe.id, cluster=self.user.cluster)
            await sync_to_async(self.drop_foreign_table)(pipe.id)
            logging.info(f"end on pipe deleted {pipe.name}")
        except (CHException, ValueError) as e:
            logging.warning(str(e))
        except Exception as e:
            logging.exception(f"error deleting pipe {pipe.name}: {e}")

    async def on_pipe_renamed(self, old_pipe_id: str, new_pipe: Pipe):
        try:
            if not self.user["enabled_pg"]:
                return
            logging.info(f"on pipe renamed {old_pipe_id} to {new_pipe}")
            await ch_drop_view(
                self.user["database_server"], self.user["database"], old_pipe_id, cluster=self.user.cluster
            )
            await sync_to_async(self.drop_foreign_table)(old_pipe_id)
            await self.on_endpoint_changed(new_pipe)
            logging.info(f"end on pipe renamed {old_pipe_id} to {new_pipe}")
        except Exception as e:
            logging.exception(f"error renaming pipe {old_pipe_id} to {new_pipe.name}: {e}")

    def parse_type(self, column_type: str) -> str:
        """
        >>> sv = PGService(None)
        >>> sv.parse_type('AggregateFunction(sum, Int32)')
        "INT4 OPTIONS(AggregateFunction 'sum')"
        >>> sv.parse_type('SimpleAggregateFunction(sum, Int64)')
        "INT8 OPTIONS(AggregateFunction 'sum')"
        >>> sv.parse_type('AggregateFunction(sumMap, Array(Int32), Array(Int32))')
        "TEXT OPTIONS(AggregateFunction 'sumMap')"
        >>> sv.parse_type('AggregateFunction(1, sumMap, Array(Int32), Array(Int32))')
        "TEXT OPTIONS(AggregateFunction 'sumMap')"
        """
        try:
            if column_type.lower().startswith("array"):
                return f"{self.parse_type(self.get_inside_par(column_type, get_most_internal_type=False))}[]"
            elif "FixedString" in column_type:
                return f"VARCHAR({self.get_inside_par(column_type)})"
            elif (
                "LowCardinality" in column_type
                or "Enum8" in column_type
                or "Enum16" in column_type
                or "Tuple" in column_type
            ):
                return "TEXT"
            elif "DateTime" in column_type or "DateTime64" in column_type:
                return "TIMESTAMP"
            elif "Decimal" in column_type:
                return "NUMERIC"
            elif "AggregateFunction" in column_type or "SimpleAggregateFunction" in column_type:
                engine_function = (
                    "AggregateFunction" if "AggregateFunction" in column_type else "SimpleAggregateFunction"
                )
                inside = self.get_inside_par(column_type, get_most_internal_type=False)
                parts = inside.split(",")
                if parts[0].isnumeric():  # AggregateFunction may return the version in the first position.
                    parts = parts[1:]
                parts = [part.strip() for part in parts]
                func = parts[0]
                if len(parts) == 1:
                    ctype = "DOUBLE PRECISION"
                elif len(parts) == 2:
                    ctype = self.parse_type(parts[1].strip())
                else:
                    ctype = "TEXT"
                return f"{ctype} OPTIONS({engine_function} '{func}')"

            if "Nullable" in column_type:
                column_type = self.get_inside_par(column_type)

            return TYPES_CONVERSION[column_type]
        except KeyError as e:
            raise ParseTypeException(f"cannot parse type {column_type}: {e}")

    def get_inside_par(self, column_type: str, get_most_internal_type: bool = True) -> str:
        """
        >>> sv = PGService(None)
        >>> sv.get_inside_par('Array(DateTime)')
        'DateTime'
        >>> sv.get_inside_par('Nullable(FixedString(50))')
        '50'
        >>> sv.get_inside_par('Nullable(FixedString(50))', get_most_internal_type=False)
        'FixedString(50)'
        >>> sv.get_inside_par('Array(Tuple(String, Float32))', get_most_internal_type=False)
        'Tuple(String, Float32)'
        >>> sv.get_inside_par('SimpleAggregateFunction(sum, Float64)', get_most_internal_type=True)
        'sum, Float64'
        """
        if "(" in column_type:
            if get_most_internal_type:
                return column_type.split("(")[-1].replace(")", "").strip()
            else:
                without_first_type = column_type.split("(", 1)[-1]
                without_last_parenthesis = without_first_type[::-1].split(")", 1)[-1][::-1]
                return without_last_parenthesis.strip()
        return column_type

    def is_nullable(self, column_type):
        return "nullable" in column_type.lower()

    def get_fdw_server_name(self):
        return f"fdw_{self.user.pg_metadata(USER_ROLE)['database']}"

    def get_database_name(self):
        return self.user.pg_metadata(USER_ROLE)["database"]

    def get_pg_foreign_server(self):
        return self.user["pg_foreign_server"]

    def get_pg_foreign_server_port(self):
        try:
            return self.user["pg_foreign_server_port"]
        except Exception:
            return "8123"

    def get_ch_user(self):
        return "postgres"

    def get_ch_password(self):
        return ""

    def get_pg_rolename(self):
        return f"user_{self.user['database']}"

    def get_pg_password(self):
        # we create a random password on user creation
        # but the actual password must be set by the admin from cheriff
        # in any case we don't store it in our metadata database
        import string
        from random import choice, randint

        characters = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(characters) for x in range(randint(15, 30)))
        return self.encrypt(self.get_pg_rolename(), password)

    def encrypt(self, user, password):
        pw = EncryptPassword(
            user=user,
            password=password,
            algorithm="scram-sha-256",
        )
        return str(pw.encrypt(), "utf-8")

    def alter_server(self, db_name=None, host=None):
        if not db_name and not host:
            return False

        options = ""
        if host:
            options += f"SET host '{host}',"

        if db_name:
            options += f"SET dbname '{db_name}',"

        try:
            logging.info(f"alter server {self.get_fdw_server_name()}")
            sql = f"ALTER SERVER {self.get_fdw_server_name()} OPTIONS ({options[:-1]});"
            self.execute(sql, autocommit=True, role=USER_ROLE)
        except Exception as e:
            logging.exception(f"error on alter server {self.get_fdw_server_name()}: {e}")
