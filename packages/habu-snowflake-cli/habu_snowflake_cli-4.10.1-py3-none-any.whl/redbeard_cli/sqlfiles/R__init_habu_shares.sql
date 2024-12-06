BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.INIT_HABU_SHARES(ORGANIZATON_ID VARCHAR, HABU_ACCOUNT VARCHAR, CUSTOMER_ACCOUNT_ID VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Since "SHOW SHARES" does not work within native app just try to accept shares
        // if it works we are good and else initialization fails as desired.
        var sf_org_id = ORGANIZATON_ID.replace(/-/g, '').toUpperCase();
        var org_share_name = "HABU_ORG_" + sf_org_id + "_SHARE";
        var org_share_db_name = org_share_name + "_DB";
        var customer_account_locator = CUSTOMER_ACCOUNT_ID.split(".")[0].toUpperCase()
        try {
            // Accept share of HABU Org DB
            sqlcmd = "CREATE DATABASE IF NOT EXISTS " + org_share_db_name + " FROM SHARE " + HABU_ACCOUNT + "." + org_share_name + " COMMENT = 'HABU_" + customer_account_locator + "'";
            snowflake.execute({ sqlText: sqlcmd });
            sqlcmd = "GRANT IMPORTED PRIVILEGES ON DATABASE " + org_share_db_name + " TO ROLE ACCOUNTADMIN";
            snowflake.execute({ sqlText: sqlcmd });
            sqlcmd = "GRANT IMPORTED PRIVILEGES ON DATABASE " + org_share_db_name + " TO ROLE SYSADMIN";
            snowflake.execute({ sqlText: sqlcmd });
            // Accept share of HABU Identity graph
            sqlcmd = "CREATE OR REPLACE DATABASE HABU_ID_GRAPH_SHARE_DB FROM SHARE " + HABU_ACCOUNT + "." + "HABU_ID_GRAPH_SHARE COMMENT = 'HABU_" + customer_account_locator + "'";
            snowflake.execute({ sqlText: sqlcmd });
            sqlcmd = "GRANT IMPORTED PRIVILEGES ON DATABASE HABU_ID_GRAPH_SHARE_DB TO ROLE ACCOUNTADMIN";
            snowflake.execute({ sqlText: sqlcmd });
            sqlcmd = "GRANT IMPORTED PRIVILEGES ON DATABASE HABU_ID_GRAPH_SHARE_DB TO ROLE SYSADMIN";
            snowflake.execute({ sqlText: sqlcmd });
        } catch (err) {
            return "Init Habu Shares failed for the following command: [" + sqlcmd + "], error message: " + err.message;
        }
        return "Init Habu shares successful";
	$$;

end;

