BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.PROCESS_ORG_REQUEST()
returns string
language javascript
execute as owner as
$$
    // Install stored procedure that will be called when a new clean room request is generated
    // via the Habu application. The procedure copies the requests from the stream to the table
    // so that after tasks can process the request.

    try {
        // copy all new requests from stream into a local table to reset the stream
        var sqlCommand = "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS (ID, REQUEST_TYPE, REQUEST_DATA, CREATED_AT, UPDATED_AT, REQUEST_STATUS) (SELECT ID, REQUEST_TYPE, REQUEST_DATA, CREATED_AT, UPDATED_AT, REQUEST_STATUS FROM CLEAN_ROOM.CLEAN_ROOM_REQUESTS_STREAM)";
        snowflake.execute({sqlText: sqlCommand});

        result = "SUCCESS";
} catch (err) {
        result = "FAILED";
        var stmt = snowflake.createStatement({
            sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
            binds: [
                err.code, err.state, err.message, err.stackTraceTxt, "", Object.keys(this)[0]
            ]
        });
        var res = stmt.execute();
}
    return result;
$$;

end;

