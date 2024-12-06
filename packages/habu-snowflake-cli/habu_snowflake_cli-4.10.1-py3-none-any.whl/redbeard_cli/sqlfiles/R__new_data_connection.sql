BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs handler for new_data_connections

        try {
            var crRequestSql = "SELECT " +
                                    " id AS request_id, " +
                                    " request_data:data_connection_id AS data_connection_id, " +
                                    " request_data:database_name AS database_name, " +
                                    " request_data:schema_name AS schema_name, " +
                                    " request_data:dataset_type AS dataset_type, " +
                                    " request_data:organization_id AS organization_id, " +
                                    " request_data:table_name AS table_name, " +
                                    " request_data:skip_table_validation AS skip_table_validation " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";
            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['NEW_DATA_CONNECTION', 'PENDING']
            });

            var rs = stmt.execute();
            var newDatasetParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var dataconnectionId = rs.getColumnValue(2);
                var databaseName = rs.getColumnValue(3);
                var schemaName = rs.getColumnValue(4);
                var datasetType = rs.getColumnValue(5);
                var organizationId = rs.getColumnValue(6);
                var tableName = rs.getColumnValue(7);
                var skipTableValidation = rs.getColumnValue(8);

                newDatasetParams.push({
                    'requestID': requestID,
                    'dataconnectionId': dataconnectionId,
                    'databaseName': databaseName,
                    'schemaName': schemaName,
                    'datasetType': datasetType,
                    'organizationId': organizationId,
                    'tableName': tableName,
                    'skipTableValidation': skipTableValidation
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < newDatasetParams.length; i++) {
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.CREATE_DATA_CONNECTION(:1, :2, :3, :4, :5, :6, :7, :8)',
                    binds: [
                        newDatasetParams[i]['requestID'],
                        newDatasetParams[i]['organizationId'],
                        newDatasetParams[i]['dataconnectionId'],
                        newDatasetParams[i]['datasetType'],
                        newDatasetParams[i]['databaseName'],
                        newDatasetParams[i]['schemaName'],
                        newDatasetParams[i]['tableName'],
                        newDatasetParams[i]['skipTableValidation']
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CREATE_DATA_CONNECTION(REQUEST_ID VARCHAR, ORG_ID VARCHAR, DATA_CONNECTION_ID VARCHAR, DATASET_TYPE VARCHAR, DB_NM VARCHAR, SCHEMA_NM VARCHAR, TABLE_NM VARCHAR, SKIP_TABLE_VALIDATION VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        try {
            var msg = "";

            if (SKIP_TABLE_VALIDATION !== "TRUE") {
                var existsDbSchemaTable = "select 1 from " + DB_NM +"." + SCHEMA_NM + "." + TABLE_NM + " limit 1";
                var result_scan = snowflake.execute({
                    sqlText:  existsDbSchemaTable
                });
            } else {
                var msg1 = "The validation of tables is going to be skipped."
                snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                    binds:[msg1, REQUEST_ID, Object.keys(this)[0]]
                }).execute();
            }


            var deleteColumns = "DELETE FROM HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS WHERE DATA_CONNECTION_ID = '" + DATA_CONNECTION_ID + "'";
            snowflake.execute({
                sqlText:  deleteColumns
            });

            var deleteConnections = "DELETE FROM HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTIONS WHERE ID = '" + DATA_CONNECTION_ID + "'";
            snowflake.execute({
                sqlText:  deleteConnections
            });

            var dataConnectionsSql = "INSERT INTO HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTIONS (ID, ORGANIZATION_ID, DATABASE_NAME, DB_SCHEMA_NAME, DB_TABLE_NAME, DATASET_TYPE)" +
                                            "(" +
                                            "  SELECT '" + DATA_CONNECTION_ID + "', '" + ORG_ID + "', TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME,'" + DATASET_TYPE + "' FROM " + DB_NM +".INFORMATION_SCHEMA.TABLES" +
                                            "  WHERE TABLE_CATALOG = '" + DB_NM +"' AND TABLE_SCHEMA = '" +SCHEMA_NM +"' AND TABLE_NAME = '" + TABLE_NM +"'" +
                                            ")";

            snowflake.execute({
                sqlText:  dataConnectionsSql
            });

            snowflake.execute({
                sqlText: "GRANT REFERENCE_USAGE ON DATABASE " + DB_NM + " TO SHARE HABU_DATA_CONNECTIONS_SHARE"
            })

            var dataConnectionsColumnsSql = "INSERT INTO HABU_DATA_CONNECTIONS.DATA_CONNECTIONS.DATA_CONNECTION_COLUMNS" +
                                            "        (ID, ORGANIZATION_ID, DATA_CONNECTION_ID, COLUMN_NAME, COLUMN_POSITION, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE)" +
                                            "        (" +
                                            "          SELECT uuid_string(), '" + ORG_ID + "', '" + DATA_CONNECTION_ID+ "', " +
                                            "          COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE" +
                                            "          FROM "+ DB_NM +".INFORMATION_SCHEMA.COLUMNS" +
                                            "          WHERE TABLE_CATALOG = '" + DB_NM+ "' AND TABLE_SCHEMA = '" + SCHEMA_NM+ "' AND TABLE_NAME = '" + TABLE_NM+ "'  " +
                                            "        )";


            snowflake.execute({
                sqlText:  dataConnectionsColumnsSql
            });

            var stmt = snowflake.createStatement({
                sqlText: "SELECT REFERENCED_DATABASE, REFERENCED_SCHEMA, REFERENCED_OBJECT_NAME FROM SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES" +
                            " WHERE REFERENCING_DATABASE = :1  AND REFERENCING_SCHEMA = :2 AND REFERENCING_OBJECT_NAME = :3",
                binds: [DB_NM, SCHEMA_NM, TABLE_NM]
            });
            var rs = stmt.execute();
            while (rs.next()) {
                var referencedDatabase = rs.getColumnValue(1);

                var msg = "Running grant reference_usage on " + referencedDatabase + " to HABU_DATA_CONNECTIONS_SHARE share";
                snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                    binds:[msg, REQUEST_ID, Object.keys(this)[0]]
                }).execute();

                snowflake.execute({
                    sqlText: "GRANT REFERENCE_USAGE ON DATABASE " + referencedDatabase + " TO SHARE HABU_DATA_CONNECTIONS_SHARE"
                })
            }

            result = "COMPLETE";
            msg = "Data connection created successfully"
        } catch (err) {
            result = "FAILED";
            if (err.message.includes("Granting individual privileges on imported database is not allowed. Use 'GRANT IMPORTED PRIVILEGES' instead.")) {
                msg = "DATABASE: " + DB_NM + " is a shared database. Tables/Views in shared databases cannot be used as data connections";
                var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, msg, err.stackTraceTxt, REQUEST_ID, Object.keys(this)[0]
                ]
            });
            var res = stmt.execute();
            } else {
                var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, REQUEST_ID, Object.keys(this)[0]
                ]
            });
            msg = err.message
            var res = stmt.execute();
            }
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

