BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_ERROR(ERROR_CODE DOUBLE, ERROR_STATE STRING, ERROR_MESSAGE STRING, ERROR_STACK_TRACE STRING, REQUEST_ID VARCHAR, PROC_NAME VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Install stored procedure that will add error to the error table.

        sqlcmd = "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_ERRORS \
            (CODE, STATE, MESSAGE, REQUEST_ID, PROC_NAME, STACK_TRACE, CREATED_AT) \
            VALUES (?,?,?,?,?,?,CURRENT_TIMESTAMP())";
        snowflake.execute({
            sqlText: sqlcmd,
            binds: [ERROR_CODE, ERROR_STATE, ERROR_MESSAGE, REQUEST_ID, PROC_NAME, ERROR_STACK_TRACE]
        });
return "SUCCESS";
$$;

end;

