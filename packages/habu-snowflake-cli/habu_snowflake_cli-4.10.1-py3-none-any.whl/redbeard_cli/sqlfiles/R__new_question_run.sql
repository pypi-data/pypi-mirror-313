BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs the handler for new question runs

        function logStatementWithRequestID(message, request_id) {
            snowflake.createStatement({
            sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
            binds:[message, request_id, Object.keys(this)[0]]
            }).execute();
        }

        function escapeQuotes(inputString) {
            var escapedSingleQuotes = inputString.replace(/'/g, "''");
            return escapedSingleQuotes;
        }

        try {
            var crRequestSql = "SELECT id AS request_id, " +
            " request_data:clean_room_id AS clean_room_id, " +
            " request_data:result_table AS result_table, " +
            " request_data:result_table_ddl AS result_table_ddl, " +
            " request_data:accounts AS accounts, " +
            " request_data:accountNames AS accountNames, " +
            " request_data:organizationNames AS organizationNames, " +
            " request_data:compute_account_id AS compute_account_id, " +
            " request_data:statement_hash AS statement_hash, " +
            " request_data:question_run_query AS question_run_query, " +
            " request_data:procedure_sql AS procedure_sql, " +
            " request_data:task_configuration_parameters AS task_configuration_parameters " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['NEW_QUESTION_RUN', 'PENDING']
            });

            var rs = stmt.execute();
            var newQuestionRunParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var resultTable = rs.getColumnValue(3);
                var resultTableDDL = rs.getColumnValue(4);
                var accounts = rs.getColumnValue(5);
                var accountNames = rs.getColumnValue(6);
                var organizationNames = rs.getColumnValue(7);
                var computeAccountId = rs.getColumnValue(8);
                var statementHash = rs.getColumnValue(9);
                var query = rs.getColumnValue(10);
                var procedureSQL = rs.getColumnValue(11);
                var taskConfigurationParameters = rs.getColumnValue(12);

                newQuestionRunParams.push({
                    'requestID' : requestID,
                    'cleanRoomID' : cleanRoomID,
                    'resultTable' : resultTable,
                    'resultTableDDL' : resultTableDDL,
                    'accounts' : accounts,
                    'accountNames': accountNames,
                    'organizationNames': organizationNames,
                    'computeAccountId': computeAccountId,
                    'statementHash': statementHash,
                    'query' : query,
                    'procedureSQL' : procedureSQL,
                    'taskConfigurationParameters': taskConfigurationParameters
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < newQuestionRunParams.length; i++) {
                // Create new warehouse and task config
                var crqr_request_id = newQuestionRunParams[i]['requestID'];
                var sanitized_request_id = crqr_request_id.replace(/-/g, '').toUpperCase();
                var HABU_QUESTION_RUN_ROOT_TASK_NAME = "HABU_" + sanitized_request_id + "_ROOT_TASK";
                var HABU_QUESTION_RUN_FINALIZE_TASK_NAME = "HABU_" + sanitized_request_id + "_FINALIZE_TASK";

                // Retrieve passed task and warehouse configuration
                var task_configuration_parameters = JSON.parse(newQuestionRunParams[i]['taskConfigurationParameters']);
                var HABU_WAREHOUSE_NAME = task_configuration_parameters.warehouseName;
                // Logging the WH used for the run
                logStatementWithRequestID(`Using Warehouse ${HABU_WAREHOUSE_NAME} to serve to serve requestID: ${crqr_request_id}`, crqr_request_id)

                // Create & execute root CRQ run task while escaping single quotes for query
                var questionRunParam = newQuestionRunParams[i];
                var escapedResultTable = escapeQuotes(questionRunParam.resultTable);
                var escapedResultTableDDL = escapeQuotes(questionRunParam.resultTableDDL);
                var escapedQuery = escapeQuotes(questionRunParam.query);
                var updatedProcedureSQL = questionRunParam.procedureSQL === null ? '' : escapeQuotes(questionRunParam.procedureSQL);

                var new_question_runs_root_task_sql = `CREATE OR REPLACE TASK CLEAN_ROOM.${HABU_QUESTION_RUN_ROOT_TASK_NAME} \
                                                   WAREHOUSE = ${HABU_WAREHOUSE_NAME} \
                                                   USER_TASK_TIMEOUT_MS = ${task_configuration_parameters.taskTimeout} \
                                                   AS CALL CLEAN_ROOM.ADD_NEW_QUESTION_RUN(
                                                    '${questionRunParam.requestID}',
                                                    '${questionRunParam.cleanRoomID}',
                                                    '${escapedResultTable}',
                                                    '${escapedResultTableDDL}',
                                                    '${questionRunParam.accounts}',
                                                    '${questionRunParam.accountNames}',
                                                    '${questionRunParam.organizationNames}',
                                                    '${questionRunParam.computeAccountId}',
                                                    '${questionRunParam.statementHash}',
                                                    '${escapedQuery}',
                                                    '${updatedProcedureSQL}'
                                               );`;

                snowflake.execute({ sqlText: new_question_runs_root_task_sql });

                // Create and execute finalizer task for root task
                var new_question_runs_finalize_task = `CREATE OR REPLACE TASK CLEAN_ROOM.${HABU_QUESTION_RUN_FINALIZE_TASK_NAME}
                                                       WAREHOUSE = ${HABU_WAREHOUSE_NAME}
                                                       FINALIZE = ${HABU_QUESTION_RUN_ROOT_TASK_NAME}
                                                       AS
                                                           BEGIN
                                                               ALTER TASK ${HABU_QUESTION_RUN_FINALIZE_TASK_NAME} SUSPEND;
                                                               DROP TASK IF EXISTS ${HABU_QUESTION_RUN_ROOT_TASK_NAME};
                                                               DROP TASK IF EXISTS ${HABU_QUESTION_RUN_FINALIZE_TASK_NAME};
                                                           END
                                                       ;`;
                snowflake.execute({ sqlText: new_question_runs_finalize_task });

                // Resume finalizer task and execute root task
                snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM." + HABU_QUESTION_RUN_FINALIZE_TASK_NAME + " RESUME" });
                snowflake.execute({ sqlText: "EXECUTE TASK CLEAN_ROOM." + HABU_QUESTION_RUN_ROOT_TASK_NAME });
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ADD_NEW_QUESTION_RUN(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, RESULT_TABLE VARCHAR, RESULT_TABLE_DDL VARCHAR, ACCOUNTS_INPUT VARCHAR, ACCOUNT_NAMES_INPUT VARCHAR, ORG_NAMES_INPUT VARCHAR, COMPUTE_ACCOUNT_ID VARCHAR, STATEMENT_HASH VARCHAR, QUESTION_RUN_QUERY VARCHAR, PROCEDURE_SQL VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
       // Function for checking Valid JSON String or not.

        function isValidJSON(jsonString) {
            try {
                var o = JSON.parse(jsonString);
                if (o && typeof o === "object") {
                    return o;
                }
            }
            catch (e) { }
            return null;
        }

        // Install the New question run stored procedure

        try {

            var rs = snowflake.execute({sqlText: "SELECT CURRENT_WAREHOUSE()"});
            rs.next();
            var warehouse_used = rs.getColumnValue(1);

            msg = `Executing the question run report request using warehouse size - ${warehouse_used}`
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[msg, REQUEST_ID, Object.keys(this)[0]]
            }).execute();

            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();

            var habuShareDb = "HABU_CR_" + sf_clean_room_id + "_HABU_SHARE"

            snowflake.execute({
                sqlText: RESULT_TABLE_DDL
            });

            snowflake.execute({
                sqlText: "GRANT SELECT ON TABLE HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM_RUN_RESULTS." + RESULT_TABLE + " TO SHARE " + habuShareDb
            });

            if ((ACCOUNTS_INPUT != null && ACCOUNTS_INPUT.trim().length != 0) &&
                (ACCOUNT_NAMES_INPUT != null && ACCOUNT_NAMES_INPUT.trim().length != 0) &&
                (ORG_NAMES_INPUT != null && ORG_NAMES_INPUT.trim().length != 0)
                ) {
                ACCOUNTS = ACCOUNTS_INPUT.split(",");
                ACCOUNT_NAMES = ACCOUNT_NAMES_INPUT.split(",");
                ORG_NAMES = ORG_NAMES_INPUT.split(",");
                for (var i = 0; i < ACCOUNTS.length; i++) {
                    var partnerShare = "HABU_CR_" + sf_clean_room_id + "_PARTNER_SHARE"
                    var partnerShareDb = "HABU_CR_" + ACCOUNTS[i] + "_" + sf_clean_room_id + "_PARTNER_SHARE_DB"
                    var shareName = ORG_NAMES[i] + "." + ACCOUNT_NAMES[i] + "." + partnerShare

                    snowflake.execute({
                        sqlText: "CREATE DATABASE IF NOT EXISTS " + partnerShareDb + " FROM SHARE " + shareName + " COMMENT = 'HABU_" + ACCOUNTS[i] + "'"
                    });

                    snowflake.execute({
                        sqlText: "GRANT IMPORTED PRIVILEGES ON DATABASE " + partnerShareDb + " TO ROLE ACCOUNTADMIN"
                    })
                    snowflake.execute({
                        sqlText: "GRANT IMPORTED PRIVILEGES ON DATABASE " + partnerShareDb + " TO ROLE SYSADMIN"
                    });
                }
            }


            // Install procedure if exists
            if (PROCEDURE_SQL != null && PROCEDURE_SQL.trim().length != 0) {
                snowflake.execute({sqlText: PROCEDURE_SQL});
                // adding current session into statement_hash to allow own account queries
                snowflake.execute({
                    sqlText: "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS (ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH) select  '" + COMPUTE_ACCOUNT_ID + "','" + CLEAN_ROOM_ID + "', SHA2(current_session())"
                })
            } else {
                snowflake.execute({
                    sqlText: "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS (ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH) VALUES (:1, :2, :3)",
                    binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH]
                })
            }

            // Execute the actual question query
            var resultSet = snowflake.execute({sqlText: QUESTION_RUN_QUERY})
            qId = Object.keys(this)[0] + " - QUESTION_RUN_QUERY - Query ID: " + resultSet.getQueryId()

            while (resultSet.next()) {
                var runQueryResponse = resultSet.getColumnValueAsString(1);
                var json = isValidJSON(runQueryResponse);
                if (json != null) {
                    if (json.loggerMessage && json.loggerMessage.length != 0) {
                        opMsg = json.loggerMessage
                        snowflake.createStatement({
                            sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                            binds:[opMsg, REQUEST_ID, Object.keys(this)[0]]
                        }).execute();
                    }

                    // Throw Error if Message is not success for Python.
                    if (json.message && json.message != "SUCCESS") {
                        throw { code : json.code, message: json.message, state : json.state, stackTraceTxt : json.stackTraceTxt }
                    }

                }
            }

            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[qId, REQUEST_ID, Object.keys(this)[0]]
            }).execute();

            if (PROCEDURE_SQL != null && PROCEDURE_SQL.trim().length != 0) {
                snowflake.execute({
                    sqlText: "DELETE FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS where ACCOUNT_ID = :1 and CLEAN_ROOM_ID = :2 and STATEMENT_HASH = SHA2(current_session())",
                    binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID]
                })
            } else {
                snowflake.execute({
                    sqlText: "DELETE FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS where ACCOUNT_ID = :1 and CLEAN_ROOM_ID = :2 and STATEMENT_HASH = :3",
                    binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH]
                })
            }

            result = "COMPLETE";
            msg = "New question run added successfully"
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

