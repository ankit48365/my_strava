https://dlthub.com/docs/tutorial/rest-api

postgres=# CREATE DATABASE test_dblx;
CREATE DATABASE
postgres=# CREATE USER tst_user WITH PASSWORD '';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE  test_dblx TO tst_user;
GRANT
postgres=# ALTER USER tst_user SET search_path = public;
ALTER ROLE
postgres=# ALTER DATABASE test_dblx OWNER TO tst_user;
ALTER DATABASE