BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_POST_RUN_QUERY()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs the handler for post run query

    try {
            var crRequestSql = "SELECT id AS request_id, request_data:post_run_result_table_name AS post_run_result_table_name,  " +
            " request_data:post_run_query AS post_run_query, " +
            " request_data:external_id AS external_id, " +
            " request_data:insert_query_count AS insert_query_count " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['POST_RUN_QUERY', 'PENDING']
            });

            var rs = stmt.execute();
            var postRunQueryParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var postRunResultTableName = rs.getColumnValue(2);
                var postRunQuery = rs.getColumnValue(3);
                var externalID = rs.getColumnValue(4);
                var insertQueryCount = rs.getColumnValue(5);

                postRunQueryParams.push({
                    'requestID': requestID,
                    'postRunResultTableName': postRunResultTableName,
                    'postRunQuery': postRunQuery,
                    'externalID': externalID,
                    'insertQueryCount': insertQueryCount
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
}

            for (var i = 0; i < postRunQueryParams.length; i++){
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.POST_RUN_QUERY(:1, :2, :3, :4, :5)',
                    binds: [
                        postRunQueryParams[i]['requestID'],
                        postRunQueryParams[i]['postRunResultTableName'],
                        postRunQueryParams[i]['postRunQuery'],
                        postRunQueryParams[i]['externalID'],
                        postRunQueryParams[i]['insertQueryCount']
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.POST_RUN_QUERY(REQUEST_ID VARCHAR, POST_RUN_RESULT_TABLE_NAME VARCHAR, POST_RUN_QUERY VARCHAR, EXTERNAL_ID VARCHAR, INSERT_QUERY_COUNT VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Installs post run query procedure

        try {

            snowflake.execute({sqlText: POST_RUN_QUERY});

            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:["Post Run query executed", REQUEST_ID, Object.keys(this)[0]]
            }).execute();

            snowflake.execute({sqlText: INSERT_QUERY_COUNT})

            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:["Query count inserted", REQUEST_ID, Object.keys(this)[0]]
            }).execute();

            result = "COMPLETE";
            msg = "Post Run Query successful"
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

