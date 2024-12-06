BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_DATA_CONNECTION_OBJECTS(HABU_ORG_NAME_ACCOUNT_NAME_COMBO VARCHAR, CUSTOMER_ACCOUNT_ID VARCHAR, SHARE_RESTRICTIONS VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$

        var customer_account_locator = CUSTOMER_ACCOUNT_ID.split(".")[0].toUpperCase();
        sqlcmd = "CREATE DATABASE IF NOT EXISTS HABU_DATA_CONNECTIONS COMMENT = 'HABU_" + customer_account_locator + "'";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "CREATE SCHEMA IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS COMMENT = 'HABU_" + customer_account_locator + "'";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "CREATE TABLE IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTIONS (" +
            "ID VARCHAR(40) NOT NULL," +
            "ORGANIZATION_ID VARCHAR(40) NOT NULL," +
            "DATABASE_NAME VARCHAR(255) NOT NULL," +
            "DB_SCHEMA_NAME VARCHAR(255) NOT NULL," +
            "DB_TABLE_NAME VARCHAR(255) NOT NULL," +
            "DATASET_TYPE VARCHAR(100)," +
            "IDENTITY_TYPE VARCHAR(50))";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "CREATE TABLE IF NOT EXISTS HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS (" +
            "ID VARCHAR(40) NOT NULL," +
            "ORGANIZATION_ID VARCHAR(40) NOT NULL," +
            "DATA_CONNECTION_ID VARCHAR(40) NOT NULL," +
            "COLUMN_NAME VARCHAR(255) NOT NULL," +
            "COLUMN_POSITION NUMBER(9,0) NOT NULL," +
            "DATA_TYPE VARCHAR NOT NULL," +
            "IS_LOOKUP_COLUMN BOOLEAN," +
            "IS_IDENTITY_COLUMN BOOLEAN)";
        snowflake.execute({ sqlText: sqlcmd });
        try {
            sqlcmd = "ALTER TABLE HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS ADD COLUMN NUMERIC_PRECISION NUMBER(9,0), NUMERIC_SCALE NUMBER(9,0);"
            snowflake.execute({ sqlText: sqlcmd });
        } catch (err) {
            // ignore columns already exists error
        }
        sqlcmd = "CREATE SHARE IF NOT EXISTS HABU_DATA_CONNECTIONS_SHARE";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "GRANT USAGE ON DATABASE HABU_DATA_CONNECTIONS TO SHARE HABU_DATA_CONNECTIONS_SHARE";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "GRANT USAGE ON SCHEMA HABU_DATA_CONNECTIONS.DATA_CONNECTIONS TO SHARE HABU_DATA_CONNECTIONS_SHARE";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "GRANT SELECT ON TABLE HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTIONS TO SHARE HABU_DATA_CONNECTIONS_SHARE";
        snowflake.execute({ sqlText: sqlcmd });
        sqlcmd = "GRANT SELECT ON TABLE HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS TO SHARE HABU_DATA_CONNECTIONS_SHARE";
        snowflake.execute({ sqlText: sqlcmd });
        snowflake.execute({
            sqlText: "ALTER SHARE HABU_DATA_CONNECTIONS_SHARE ADD ACCOUNTS = :1 SHARE_RESTRICTIONS = " + SHARE_RESTRICTIONS,
            binds: [HABU_ORG_NAME_ACCOUNT_NAME_COMBO]
        });
        return "Setup of data connection objects successful";
    $$;

end;

