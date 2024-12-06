BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_NEW_DATASETS()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs handler for new_datasets

        try {
            var crRequestSql = "SELECT " +
                                    " id AS request_id, " +
                                    " request_data:clean_room_id AS clean_room_id, " +
                                    " request_data:source_db AS source_db, " +
                                    " request_data:view_name AS view_name, " +
                                    " request_data:view_sql AS view_sql, " +
                                    " request_data:available_values_sql AS available_values_sql, " +
                                    " request_data:source_table_name AS source_table_name, " +
                                    " request_data:source_schema_name AS source_schema_name " +
                                    " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
                                    " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";
            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['NEW_DATASET', 'PENDING']
            });

            var rs = stmt.execute();
            var newDatasetParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var sourceDB = rs.getColumnValue(3);
                var viewName = rs.getColumnValue(4);
                var viewSql = rs.getColumnValue(5);
                var availableValuesSql = rs.getColumnValue(6);
                var sourceViewOrTableName = rs.getColumnValue(7);
                var sourceSchemaName = rs.getColumnValue(8);

                newDatasetParams.push({
                    'rID': requestID,
                    'crID': cleanRoomID,
                    'sourceDB': sourceDB,
                    'vn': viewName,
                    'vs': viewSql,
                    'avs': availableValuesSql,
                    'sourceTableName': sourceViewOrTableName,
                    'sourceSchemaName': sourceSchemaName,
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < newDatasetParams.length; i++) {
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.CREATE_NEW_DATASET(:1, :2, :3, :4, :5, :6, :7, :8)',
                    binds: [
                        newDatasetParams[i]['rID'],
                        newDatasetParams[i]['crID'],
                        newDatasetParams[i]['sourceDB'],
                        newDatasetParams[i]['vn'],
                        newDatasetParams[i]['vs'],
                        newDatasetParams[i]['avs'],
                        newDatasetParams[i]['sourceTableName'],
                        newDatasetParams[i]['sourceSchemaName']
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CREATE_NEW_DATASET(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, SOURCE_DB VARCHAR, VIEW_NAME VARCHAR, VIEW_SQL VARCHAR, AVAILABLE_VALUES_SQL VARCHAR, SOURCE_TABLE_NAME VARCHAR, SOURCE_SCHEMA_NAME VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Handles new data set command

        function logStatement(message) {
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[message, REQUEST_ID, Object.keys(this)[0]]
            }).execute();
        }

        var MAX_DEPTH = 10;


        function recursivelyFindDependencies(db, schema, table) {
            logStatement(`recursivelyFindDependencies: db: ${db}, schema: ${schema}, table: ${table}`)

            let dbList = [];
            var stmt = snowflake.createStatement({
                sqlText: `
                    WITH RECURSIVE object_dependencies_cte AS (
                        -- default case to start the recursion
                        SELECT
                            REFERENCED_DATABASE,
                            REFERENCED_SCHEMA,
                            REFERENCED_OBJECT_NAME,
                            REFERENCED_OBJECT_DOMAIN,
                            REFERENCING_DATABASE,
                            REFERENCING_SCHEMA,
                            REFERENCING_OBJECT_NAME,
                            REFERENCING_OBJECT_DOMAIN,
                            1 AS DEPTH
                        FROM
                            SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES
                        WHERE
                            REFERENCING_DATABASE = :1
                            AND REFERENCING_SCHEMA = :2
                            AND REFERENCING_OBJECT_NAME = :3
                            AND REFERENCED_OBJECT_DOMAIN IN ('TABLE', 'VIEW', 'FUNCTION', 'EXTERNAL TABLE') -- allow only few types of objects

                        UNION ALL

                        -- recursive case to find the dependencies
                        SELECT
                            d.REFERENCED_DATABASE,
                            d.REFERENCED_SCHEMA,
                            d.REFERENCED_OBJECT_NAME,
                            d.REFERENCED_OBJECT_DOMAIN,
                            d.REFERENCING_DATABASE,
                            d.REFERENCING_SCHEMA,
                            d.REFERENCING_OBJECT_NAME,
                            d.REFERENCING_OBJECT_DOMAIN,
                            cte.DEPTH + 1 AS DEPTH
                        FROM
                            SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES d
                        INNER JOIN
                            object_dependencies_cte cte
                        ON
                            d.REFERENCING_DATABASE = cte.REFERENCED_DATABASE
                            AND d.REFERENCING_SCHEMA = cte.REFERENCED_SCHEMA
                            AND d.REFERENCING_OBJECT_NAME = cte.REFERENCED_OBJECT_NAME
                            AND d.REFERENCED_OBJECT_DOMAIN IN ('TABLE', 'VIEW', 'FUNCTION', 'EXTERNAL TABLE')
                        WHERE cte.DEPTH < :4 -- filtering by MAX_DEPTH to avoid infinite recursion
                    )

                    SELECT
                        REFERENCED_DATABASE,
                        REFERENCED_SCHEMA,
                        REFERENCED_OBJECT_NAME,
                        DEPTH
                    FROM
                        object_dependencies_cte
                    ORDER BY
                    DEPTH;
                 `,
                binds: [db, schema, table, MAX_DEPTH]
            });
            var rs = stmt.execute();

            while (rs.next()) {
                var referencedDatabase = rs.getColumnValue(1);
                var referencedSchema = rs.getColumnValue(2);
                var referencedTable = rs.getColumnValue(3);
                var depth = rs.getColumnValue(4);

                logStatement(`Found dependency: ${referencedDatabase}.${referencedSchema}.${referencedTable} at depth ${depth}`)
                dbList.push(referencedDatabase);
            }

            return dbList;
        }

        try {
            var msg = "";
            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();

            var habuShareDb = "HABU_CR_" + sf_clean_room_id + "_HABU_SHARE"
            var partnerShareDb = "HABU_CR_" + sf_clean_room_id + "_PARTNER_SHARE"

            snowflake.execute({
                sqlText: "GRANT REFERENCE_USAGE ON DATABASE " + SOURCE_DB + " TO SHARE " + habuShareDb
            })

            snowflake.execute({
                sqlText: "GRANT REFERENCE_USAGE ON DATABASE " + SOURCE_DB + " TO SHARE " + partnerShareDb
            })

            snowflake.execute({
                sqlText: "GRANT REFERENCE_USAGE ON DATABASE HABU_DATA_CONNECTIONS  TO SHARE " + habuShareDb
            })

            snowflake.execute({sqlText: VIEW_SQL});

            if (AVAILABLE_VALUES_SQL !== "NONE") {
                snowflake.execute({sqlText: AVAILABLE_VALUES_SQL});

                snowflake.execute({
                    sqlText: "GRANT SELECT ON VIEW HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM." + VIEW_NAME + "_AVAILABLE_VALUES TO SHARE " + habuShareDb
                });
            }

            var policySql = "CREATE OR REPLACE ROW ACCESS POLICY HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM." + VIEW_NAME + "_POLICY AS (query_clean_room_id VARCHAR) " +
            "RETURNS BOOLEAN -> " +
            "CASE " +
            " WHEN EXISTS (SELECT 1 FROM HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM.V_ALLOWED_STATEMENTS WHERE " +
            " account_id = CURRENT_ACCOUNT() AND (statement_hash = SHA2(CURRENT_STATEMENT()) or statement_hash = SHA2(CURRENT_SESSION()) )" +
            " AND clean_room_id = QUERY_CLEAN_ROOM_ID) " +
            " THEN TRUE END;";

            var policyStmt = snowflake.createStatement({sqlText: policySql});
            policyStmt.execute();

            snowflake.execute({
                sqlText: "ALTER VIEW HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM." + VIEW_NAME + " ADD ROW ACCESS POLICY HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM." + VIEW_NAME + "_POLICY ON (clean_room_id)"
            });

            var dbList = recursivelyFindDependencies(SOURCE_DB, SOURCE_SCHEMA_NAME, SOURCE_TABLE_NAME, 1);
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

            snowflake.execute({
                sqlText: "GRANT SELECT ON VIEW HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM." + VIEW_NAME + " TO SHARE " + partnerShareDb
            });

            result = "COMPLETE";
            msg = "Dataset created successfully"
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

