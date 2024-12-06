BEGIN

CREATE OR REPLACE SECURE FUNCTION HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HABU_ORCHESTRATOR(region varchar)
    returns STRING
    language JAVASCRIPT
    as
    $$
        var mapOfRegionToOrchestrator = new Map([
                  ['AZURE_EASTUS2', 'JNLZJCY.HABU_PROD_AZURE_EAST2'],
                  ['GCP_US_CENTRAL1', 'JNLZJCY.NATIVE_APP_HABU_GCP'],
                  ['AWS_US_EAST_1', 'JNLZJCY.HABU_PROD_AWS_US_EAST_1'],
                  ['AWS_US_EAST_2', 'JNLZJCY.UO60321'],
                  ['AWS_US_WEST_2', 'JNLZJCY.JYA07515'],
                  ['AZURE_WESTEUROPE', 'JNLZJCY.HABU_PROD_AZURE_WEST_EUROPE']
        ]);
        return mapOfRegionToOrchestrator.get(REGION);
    $$;


CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.INSTALLER()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS OWNER
AS
$$
    snowflake.execute({ sqlText: `CREATE SCHEMA IF NOT EXISTS HABU_SCHEMA` });
    snowflake.execute({ sqlText: `CREATE SCHEMA IF NOT EXISTS CLEAN_ROOM` });
    snowflake.execute({ sqlText: `CREATE OR REPLACE PROCEDURE
        HABU_SCHEMA.INIT_FRAMEWORK(ORGANIZATON_ID VARCHAR)
        returns string
        language javascript
        execute as owner as
        '

            sqlcmd = "SELECT HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HABU_ORCHESTRATOR(current_region())";
            rset = snowflake.execute({ sqlText: sqlcmd });
            rset.next()
            var HABU_ORG_NAME_ACCOUNT_NAME_COMBO = rset.getColumnValue(1);

            sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.HABU_SCHEMA.INIT_FRAMEWORK(''" + ORGANIZATON_ID + "'', ''" + HABU_ORG_NAME_ACCOUNT_NAME_COMBO + "'')";
            rset = snowflake.execute({ sqlText: sqlcmd });
            rset.next()

            return rset.getColumnValue(1);
        '`
    });


    snowflake.execute({ sqlText: `CREATE OR REPLACE PROCEDURE
        HABU_SCHEMA.INIT_FRAMEWORK(ORGANIZATON_ID VARCHAR, HABU_ORG_NAME_ACCOUNT_NAME_COMBO VARCHAR)
        returns string
        language javascript
        execute as owner as
        '
            sqlcmd = "SELECT current_account()";
            rset = snowflake.execute({ sqlText: sqlcmd });
            rset.next()
            var CUSTOMER_ACCOUNT_ID = rset.getColumnValue(1);

            var SHARE_RESTRICTIONS = "false";

            sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.INIT_HABU_SHARES(''" + ORGANIZATON_ID + "'', ''" + HABU_ORG_NAME_ACCOUNT_NAME_COMBO + "'', ''" + CUSTOMER_ACCOUNT_ID + "'')";
            var rset = snowflake.execute({ sqlText: sqlcmd });
            rset.next()
            if (rset.getColumnValue(1) != "Init Habu shares successful") {
                return rset.getColumnValue(1);
            }
            sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_DATA_CONNECTION_OBJECTS(''" + HABU_ORG_NAME_ACCOUNT_NAME_COMBO + "'', ''" + CUSTOMER_ACCOUNT_ID + "'', ''" + SHARE_RESTRICTIONS + "'')";
            snowflake.execute({ sqlText: sqlcmd });
            sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_CLEANROOM_COMMON(''" + HABU_ORG_NAME_ACCOUNT_NAME_COMBO + "'', ''" + CUSTOMER_ACCOUNT_ID + "'', ''" + SHARE_RESTRICTIONS + "'')";
            snowflake.execute({ sqlText: sqlcmd });
            sqlcmd = "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_STREAM_TASKS(''" + ORGANIZATON_ID + "'', ''" + HABU_ORG_NAME_ACCOUNT_NAME_COMBO + "'', ''" + CUSTOMER_ACCOUNT_ID + "'')";
            snowflake.execute({ sqlText: sqlcmd });
            return "Habu framework init successful";
        '`
    });

    return "Habu installer done";
$$;

end;


