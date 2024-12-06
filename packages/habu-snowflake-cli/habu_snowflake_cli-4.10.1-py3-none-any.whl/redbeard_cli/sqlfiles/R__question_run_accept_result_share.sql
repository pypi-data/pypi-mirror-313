BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE()
    RETURNS STRING
    LANGUAGE JAVASCRIPT STRICT
    EXECUTE AS OWNER AS
    $$
        // Installs the handler for accept question result share

        try {
            var crRequestSql = "SELECT id AS request_id, request_data:clean_room_id AS clean_room_id,  " +
            " request_data:owner_account_id AS owner_account_id, " +
            " request_data:share_name AS share_name " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['ACCEPT_QUESTION_RESULT_SHARE', 'PENDING']
            });

            var rs = stmt.execute();
            var questionDataShareParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var ownerAccountID = rs.getColumnValue(3);
                var shareName = rs.getColumnValue(4);

                questionDataShareParams.push({
                    'requestID': requestID,
                    'cleanRoomID': cleanRoomID,
                    'ownerAccountID': ownerAccountID,
                    'shareName': shareName
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < questionDataShareParams.length; i++){
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.QUESTION_RUN_ACCEPT_RESULT_SHARE(:1, :2, :3, :4)',
                    binds: [
                        questionDataShareParams[i]['requestID'],
                        questionDataShareParams[i]['cleanRoomID'],
                        questionDataShareParams[i]['ownerAccountID'],
                        questionDataShareParams[i]['shareName']
                    ]
                });
                stmt.execute();
            }
            result = "SUCCESS";
        } catch (err) {

            result = "FAILED";
            var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4,)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, "", Object.keys(this)[0]
                ]
            });
            var res = stmt.execute();
        }
        return result;
    $$;

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.QUESTION_RUN_ACCEPT_RESULT_SHARE
    (REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, OWNER_ACCOUNT_ID VARCHAR, SHARE_NAME VARCHAR)
    RETURNS STRING
    LANGUAGE JAVASCRIPT STRICT
    EXECUTE AS OWNER AS
    $$
        // Installs run accept result share procedure

        try {
            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();

            var dbName = `HABU_CRQRS_${sf_clean_room_id}_${OWNER_ACCOUNT_ID}_DB`

            snowflake.execute({
                sqlText: `CREATE DATABASE IF NOT EXISTS ${dbName} FROM SHARE ${SHARE_NAME}`
            });

            result = "COMPLETE";
            msg = "Question run accept result share successful"
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

