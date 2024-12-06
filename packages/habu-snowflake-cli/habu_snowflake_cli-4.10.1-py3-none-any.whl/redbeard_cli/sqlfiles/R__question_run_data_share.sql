BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs the handler for question run data share

        try {
            var crRequestSql = "SELECT id AS request_id, request_data:clean_room_id AS clean_room_id,  " +
            " request_data:compute_account_id AS compute_account_id, " +
            " request_data:statement_hash AS statement_hash, " +
            " request_data:procedure_name AS procedure_name, " +
            " request_data:procedure_sql AS procedure_sql " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['QUESTION_DATA_SHARE', 'PENDING']
            });

            var rs = stmt.execute();
            var questionDataShareParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var computeAccountId = rs.getColumnValue(3);
                var statementHash = rs.getColumnValue(4);
                var procedureName = rs.getColumnValue(5);
                var procedureSql = rs.getColumnValue(6);

                questionDataShareParams.push({
                    'requestID': requestID,
                    'cleanRoomID': cleanRoomID,
                    'computeAccountId': computeAccountId,
                    'statementHash': statementHash,
                    'procedureName': procedureName,
                    'procedureSql': procedureSql

                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
}

            for (var i = 0; i < questionDataShareParams.length; i++){
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.QUESTION_RUN_DATA_SHARE(:1, :2, :3, :4, :5, :6)',
                    binds: [
                        questionDataShareParams[i]['requestID'],
                        questionDataShareParams[i]['cleanRoomID'],
                        questionDataShareParams[i]['computeAccountId'],
                        questionDataShareParams[i]['statementHash'],
                        questionDataShareParams[i]['procedureName'],
                        questionDataShareParams[i]['procedureSql']
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

-- TODO: this requires share_restriction to be passed, how to do??
CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.QUESTION_RUN_DATA_SHARE(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, COMPUTE_ACCOUNT_ID VARCHAR, STATEMENT_HASH VARCHAR, PROCEDURE_NAME VARCHAR, PROCEDURE_SQL VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Installs question run data share procedure

        try {

            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();
            var partnerShareDb = "HABU_CR_" + sf_clean_room_id + "_PARTNER_SHARE"

            snowflake.execute({
                sqlText: "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS (ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH) VALUES (:1, :2, :3)",
                binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH]
            })

            // TODO: for now hardcoding SHARE_RESTRICTIONS to false
            snowflake.execute({
                sqlText: "ALTER SHARE " + partnerShareDb + " ADD ACCOUNTS = :1 SHARE_RESTRICTIONS=false",
                binds: [COMPUTE_ACCOUNT_ID]
            });

            result = "COMPLETE";
            msg = "Question run data share successful"
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

            opMsg = Object.keys(this)[0] + " - OPERATION STATUS - " + result + " - Detail: " + msg
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[opMsg, REQUEST_ID, Object.keys(this)[0]]
            }).execute();
}
        return result;
    $$;

end;

