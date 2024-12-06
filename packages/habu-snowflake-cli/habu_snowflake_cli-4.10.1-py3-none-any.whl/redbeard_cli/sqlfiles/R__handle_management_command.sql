BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_MANAGEMENT_COMMANDS()
    RETURNS STRING
    LANGUAGE JAVASCRIPT STRICT
    EXECUTE AS OWNER AS
    $$
        // Installs the handler for management commands
        try {
            var mgmtCmdSql = "SELECT id AS request_id, " +
            " request_data:management_command_query AS management_command_query " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";
            var stmt = snowflake.createStatement({
                sqlText: mgmtCmdSql,
                binds: ['MANAGEMENT_COMMAND', 'PENDING']
            });
            var rs = stmt.execute();
            var mgmtCmdParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var managementCommandQuery = rs.getColumnValue(2);
                mgmtCmdParams.push({
                    'requestID': requestID,
                    'managementCommandQuery': managementCommandQuery
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
}
            for (var i = 0; i < mgmtCmdParams.length; i++){
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.MANAGEMENT_COMMAND_RUNNER(:1, :2)',
                    binds: [
                        mgmtCmdParams[i]['requestID'],
                        mgmtCmdParams[i]['managementCommandQuery']
                    ]
                });
                stmt.execute();
}
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


CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.MANAGEMENT_COMMAND_RUNNER
    (REQUEST_ID VARCHAR, MANAGEMENT_COMMAND_QUERY VARCHAR)
    RETURNS STRING
    LANGUAGE JAVASCRIPT
    STRICT
    EXECUTE AS OWNER
    AS
    $$
        // Install management command runner procedure
        try {
            var resultSet = snowflake.execute({sqlText: MANAGEMENT_COMMAND_QUERY})
            result = "COMPLETE";
} catch (err) {
            result = "FAILED";
            var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, REQUEST_ID, Object.keys(this)[0]
                ]
            });
            msg = err.message
            var res = stmt.execute();
} finally {
            snowflake.execute({
                sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                binds: [result, REQUEST_ID]
            });
}
        return result;
    $$;


end;

