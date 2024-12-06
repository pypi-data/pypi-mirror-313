BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SP_LOGGER(LOG_MESSAGE VARCHAR, REQUEST_ID VARCHAR, PROC_NAME VARCHAR)
returns string
language javascript
execute as owner as
$$
// Install stored procedure that will add log messages to log table.

sqlcmd = "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_LOGS \
            (LOG_MESSAGE, REQUEST_ID, PROC_NAME, CREATED_AT) \
            VALUES (?, ?, ?, CURRENT_TIMESTAMP())";
snowflake.execute({
            sqlText: sqlcmd,
            binds: [LOG_MESSAGE, REQUEST_ID, PROC_NAME]
        });
return "SUCCESS";
$$;

end;

