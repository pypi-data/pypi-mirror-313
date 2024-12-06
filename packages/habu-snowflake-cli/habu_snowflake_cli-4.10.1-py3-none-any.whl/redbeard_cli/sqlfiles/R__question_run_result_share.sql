BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE()
    RETURNS STRING
    LANGUAGE JAVASCRIPT STRICT
    EXECUTE AS OWNER AS
    $$
        // Installs the handler for question result share

        try {
            var crRequestSql = "SELECT id AS request_id, request_data:clean_room_id AS clean_room_id,  " +
            " request_data:result_share_details AS result_share_details " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['QUESTION_RESULT_SHARE', 'PENDING']
            });

            var rs = stmt.execute();
            var questionDataShareParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var resultShareDetails = rs.getColumnValueAsString(3);

                questionDataShareParams.push({
                    'requestID': requestID,
                    'cleanRoomID': cleanRoomID,
                    'resultShareDetails': resultShareDetails
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < questionDataShareParams.length; i++){
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.QUESTION_RUN_RESULT_SHARE(:1, :2, :3)',
                    binds: [
                        questionDataShareParams[i]['requestID'],
                        questionDataShareParams[i]['cleanRoomID'],
                        questionDataShareParams[i]['resultShareDetails']
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.QUESTION_RUN_RESULT_SHARE
    (REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, RESULT_SHARE_DETAILS VARCHAR)
    RETURNS STRING
    LANGUAGE JAVASCRIPT STRICT
    EXECUTE AS OWNER AS
    $$
        // Installs run clean up procedure

        try {

            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();

            var JSON_RESULT = JSON.parse(RESULT_SHARE_DETAILS);

            for (var i = 0; i < JSON_RESULT.length; i++) {

                ACCOUNT_ID = JSON_RESULT[i].accountId;
                ACCOUNT_NAME = JSON_RESULT[i].accountName;
                RESULT_TABLES = String(JSON_RESULT[i].resultTables);

                var resultShare = `HABU_CRQRS_${sf_clean_room_id}_${ACCOUNT_ID}`

                snowflake.execute({
                    sqlText: `CREATE SHARE IF NOT EXISTS ${resultShare}`
                });

                snowflake.execute({
                    sqlText: `GRANT USAGE ON DATABASE HABU_CLEAN_ROOM_${sf_clean_room_id} TO SHARE ${resultShare}`
                });

                snowflake.execute({
                    sqlText: `GRANT USAGE ON SCHEMA HABU_CLEAN_ROOM_${sf_clean_room_id}.CLEAN_ROOM_RUN_RESULTS TO SHARE ${resultShare}`
                });

                if (RESULT_TABLES != null && RESULT_TABLES.trim().length != 0) {
                    resultTables = RESULT_TABLES.split(",");
                    for (var j = 0; j < resultTables.length; j++) {
                        snowflake.execute({
                            sqlText: "GRANT SELECT ON TABLE HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM_RUN_RESULTS." + resultTables[j] + " TO SHARE " + resultShare
                        });
                    }
                }

                snowflake.execute({
                    sqlText: `ALTER SHARE ${resultShare} ADD ACCOUNTS = ${ACCOUNT_NAME} SHARE_RESTRICTIONS=false`
                });

            }

            result = "COMPLETE";
            msg = "Question run result share successful"
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

