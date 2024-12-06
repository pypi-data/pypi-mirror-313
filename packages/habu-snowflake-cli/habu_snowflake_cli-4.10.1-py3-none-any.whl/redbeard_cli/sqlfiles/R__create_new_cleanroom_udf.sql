BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOM_UDF()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs handler for create_new_cleanroom_udf

        try {
            var crRequestSql = "SELECT " +
                                    " id AS request_id, " +
                                    " request_data:clean_room_id AS clean_room_id, " +
                                    " request_data:source_db AS source_db, " +
                                    " request_data:function_name AS function_name, " +
                                    " request_data:function_sql AS function_sql, " +
                                    " request_data:source_udf_name AS source_udf_name, " +
                                    " request_data:source_schema_name AS source_schema_name, " +
                                    " request_data:function_usage_string AS function_usage_string " +
                                    " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
                                    " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";
            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['NEW_CLEAN_ROOM_UDF', 'PENDING']
            });

            var rs = stmt.execute();
            var newCleanRoomUDFParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var sourceDB = rs.getColumnValue(3);
                var functionName = rs.getColumnValue(4);
                var functionSql = rs.getColumnValue(5);
                var sourceViewOrFunctionName = rs.getColumnValue(6);
                var sourceSchemaName = rs.getColumnValue(7);
                var functionUsageString = rs.getColumnValue(8);

                newCleanRoomUDFParams.push({
                    'rID': requestID,
                    'crID': cleanRoomID,
                    'sourceDB': sourceDB,
                    'fn': functionName,
                    'fs': functionSql,
                    'sourceFunctionName': sourceViewOrFunctionName,
                    'sourceSchemaName': sourceSchemaName,
                    'functionUsageString': functionUsageString,
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < newCleanRoomUDFParams.length; i++) {
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.CREATE_NEW_CLEAN_ROOM_UDF(:1, :2, :3, :4, :5, :6, :7, :8)',
                    binds: [
                        newCleanRoomUDFParams[i]['rID'],
                        newCleanRoomUDFParams[i]['crID'],
                        newCleanRoomUDFParams[i]['sourceDB'],
                        newCleanRoomUDFParams[i]['fn'],
                        newCleanRoomUDFParams[i]['fs'],
                        newCleanRoomUDFParams[i]['sourceFunctionName'],
                        newCleanRoomUDFParams[i]['sourceSchemaName'],
                        newCleanRoomUDFParams[i]['functionUsageString'],
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CREATE_NEW_CLEAN_ROOM_UDF(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, SOURCE_DB VARCHAR, FUNCTION_NAME VARCHAR, FUNCTION_SQL VARCHAR, SOURCE_FUNCTION_NAME VARCHAR, SOURCE_SCHEMA_NAME VARCHAR, FUNCTION_USAGE_STRING VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Handles new cleanroom udf command

        function logStatement(message) {
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[message, REQUEST_ID, Object.keys(this)[0]]
            }).execute();
        }

        var MAX_DEPTH = 10;


        function recursivelyFindDependencies(db, schema, functionName, depth) {
            logStatement(`recursivelyFindDependencies: db: ${db}, schema: ${schema}, function: ${functionName}, depth: ${depth}`)

            let dbList = [];
            if(depth >= MAX_DEPTH) {
                logStatement(`reached maximum depth at ${depth} for db: ${db}, schema: ${schema}, function: ${functionName}`)
                return dbList;
            }
            var stmt = snowflake.createStatement({
                sqlText: `SELECT REFERENCED_DATABASE, REFERENCED_SCHEMA, REFERENCED_OBJECT_NAME
                      FROM SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES
                      WHERE REFERENCING_DATABASE = :1
                      AND REFERENCING_SCHEMA = :2
                      AND REFERENCING_OBJECT_NAME = :3
                      AND (REFERENCED_OBJECT_DOMAIN = 'TABLE'
                            OR REFERENCED_OBJECT_DOMAIN = 'VIEW'
                            OR REFERENCED_OBJECT_DOMAIN = 'FUNCTION'
                            OR REFERENCED_OBJECT_DOMAIN = 'EXTERNAL TABLE')`,
                binds: [db, schema, functionName]
            });
            var rs = stmt.execute();

            while (rs.next()) {
                var referencedDatabase = rs.getColumnValue(1);
                var referencedSchema = rs.getColumnValue(2);
                var referencedFunction = rs.getColumnValue(3);

                dbList.push(referencedDatabase);

                let newList = recursivelyFindDependencies(referencedDatabase, referencedSchema, referencedFunction, depth + 1);
                dbList = dbList.concat(newList);
            }

            return dbList;
        }


        try {

            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();
            var partnerShareDb = `HABU_CR_${sf_clean_room_id}_PARTNER_SHARE`

            snowflake.execute({
                sqlText: `GRANT REFERENCE_USAGE ON DATABASE ${SOURCE_DB} TO SHARE ${partnerShareDb}`
            })

            // Function SQL will contain inbuilt access check
            snowflake.execute({sqlText: FUNCTION_SQL});

            var dbList = recursivelyFindDependencies(SOURCE_DB, SOURCE_SCHEMA_NAME, SOURCE_FUNCTION_NAME, 1);
            logStatement(`Found dependencies: ${dbList}`)

            for(let referencedDatabase of new Set(dbList)){
                if(referencedDatabase && referencedDatabase !== SOURCE_DB) {
                    logStatement(`Granting REFERENCE_USAGE on database ${referencedDatabase} to share ${partnerShareDb}`)

                    snowflake.execute({
                        sqlText: `GRANT REFERENCE_USAGE ON DATABASE ${referencedDatabase} TO SHARE ${partnerShareDb}`
                    })
                } else {
                    logStatement(`Skipping grant REFERENCE_USAGE on database ${referencedDatabase} to share ${partnerShareDb}`)
                }
            }

            // Grant usage on the function to the shareDb - partner will have access to the function, but execution will fail because of internal access check
            snowflake.execute({
                sqlText: `GRANT USAGE ON FUNCTION HABU_CLEAN_ROOM_${sf_clean_room_id}.CLEAN_ROOM.${FUNCTION_USAGE_STRING} TO SHARE ${partnerShareDb}`
            });

            result = "COMPLETE";
            msg = "Clean Room UDF created successfully"
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


