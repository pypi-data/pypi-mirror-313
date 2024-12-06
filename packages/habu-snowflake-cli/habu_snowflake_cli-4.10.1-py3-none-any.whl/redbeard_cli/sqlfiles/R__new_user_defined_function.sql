BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_NEW_USER_DEFINED_FUNCTION()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs handler for new_user_defined_functions
        try {
            var crRequestSql = "SELECT " +
                                    " id AS request_id, " +
                                    " request_data:udf_id AS udf_id, " +
                                    " request_data:database_name AS database_name, " +
                                    " request_data:schema_name AS schema_name, " +
                                    " request_data:organization_id AS organization_id, " +
                                    " request_data:udf_name AS udf_name " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";
            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['NEW_USER_DEFINED_FUNCTION', 'PENDING']
            });

            var rs = stmt.execute();
            var newUdfParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var udfId = rs.getColumnValue(2);
                var databaseName = rs.getColumnValue(3);
                var schemaName = rs.getColumnValue(4);
                var organizationId = rs.getColumnValue(5);
                var udfName = rs.getColumnValue(6);

                newUdfParams.push({
                    'requestID': requestID,
                    'udfId': udfId,
                    'databaseName': databaseName,
                    'schemaName': schemaName,
                    'organizationId': organizationId,
                    'udfName': udfName
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            for (var i = 0; i < newUdfParams.length; i++) {
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.NEW_USER_DEFINED_FUNCTION(:1, :2, :3, :4, :5, :6)',
                    binds: [
                        newUdfParams[i]['requestID'],
                        newUdfParams[i]['organizationId'],
                        newUdfParams[i]['udfId'],
                        newUdfParams[i]['databaseName'],
                        newUdfParams[i]['schemaName'],
                        newUdfParams[i]['udfName'],
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

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.NEW_USER_DEFINED_FUNCTION(REQUEST_ID VARCHAR, ORG_ID VARCHAR, UDF_ID VARCHAR, DB_NM VARCHAR, SCHEMA_NM VARCHAR, UDF_NM VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        function logStatement(message) {
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[message, REQUEST_ID, Object.keys(this)[0]]
            }).execute();
        }
        // Error function to help throw custom error messages
        function throwError(errMessage, errCode, errState) {
            logStatement(errMessage);
            throw {
                code: errCode, // Snowflake's error code for Object does not exist
                message: errMessage,
                state: errState, // Snowflake's error state for Object does not exist
                stackTraceTxt: errMessage
            };
        }

    var MAX_DEPTH = 10;

    function recursivelyFindDependentFunctions(db, schema, functionName, depth) {
        logStatement(`recursivelyFindDependentFunctions: db: ${db}, schema: ${schema}, function: ${functionName}, depth: ${depth}`)

        let functionList = [];
        if (depth >= MAX_DEPTH) {
            logStatement(`reached maximum depth at ${depth} for db: ${db}, schema: ${schema}, function: ${functionName}`)
            return functionList;
        }

        let preparedSql = `SELECT REFERENCED_DATABASE, REFERENCED_SCHEMA, REFERENCED_OBJECT_NAME
                          FROM SNOWFLAKE.ACCOUNT_USAGE.OBJECT_DEPENDENCIES
                          WHERE REFERENCING_DATABASE = :1
                          AND REFERENCING_SCHEMA = :2
                          AND REFERENCING_OBJECT_NAME = :3
                          AND REFERENCED_OBJECT_DOMAIN = 'FUNCTION';`;


        var getDependentFunctionsSQL = snowflake.createStatement({
            sqlText: preparedSql,
            binds: [db, schema, functionName]
        });

        var rs = getDependentFunctionsSQL.execute();
        while (rs.next()) {
            var referencedDatabase = rs.getColumnValue(1);
            var referencedSchema = rs.getColumnValue(2);
            var referencedFunction = rs.getColumnValue(3);
            var dbSchemaFunctionObject = {
                referencedDatabaseName: referencedDatabase,
                referencedSchemaName: referencedSchema,
                referencedFunctionName: referencedFunction,
            };
            functionList.push(dbSchemaFunctionObject);

            let newList = recursivelyFindDependentFunctions(referencedDatabase, referencedSchema, referencedFunction, depth + 1);
            functionList = functionList.concat(newList);
        }
        return functionList;
    }

    try {

        var msg = "";

        var existsDbSchemaUdf = `SELECT * FROM ${DB_NM}.INFORMATION_SCHEMA.FUNCTIONS WHERE FUNCTION_SCHEMA = '${SCHEMA_NM}' AND FUNCTION_NAME = '${UDF_NM}' LIMIT 1`;
        var result_scan = snowflake.execute({sqlText: existsDbSchemaUdf});

        // Attempt to read the result set and store the result in a variable
        if (!result_scan.next()) {
            var errStatement = `UDF: ${DB_NM}.${SCHEMA_NM}.${UDF_NM} does not exist!`;
            // Snowflake's error code and state for Object does not exist
            throwError(errStatement, "2003", "02000");
        }

        // Check if the imported function is secure
        var isSecure = result_scan.getColumnValue("IS_SECURE");
        if (isSecure !== "YES") {
            var secureFunctionError = `UDF: ${DB_NM}.${SCHEMA_NM}.${UDF_NM} is not a secure function, and cannot be imported.`;
            // Snowflake's error code and state for Object does not exist
            throwError(secureFunctionError, "2003", "02000");
        }
        // Check if the function has dependencies on other functions and ensure they are secure
        var functionList = recursivelyFindDependentFunctions(DB_NM, SCHEMA_NM, UDF_NM, 1);
        logStatement(`Found dependentFunctions with length: ${functionList.length}`)

        for (let i = 0; i < functionList.length; i++) {
            let func = functionList[i];
            let dependentDB = func.referencedDatabaseName;
            let dependentSchema = func.referencedSchemaName;
            let dependentFunctionName = func.referencedFunctionName;

            logStatement(`Validating dependent function: ${dependentDB}.${dependentSchema}.${dependentFunctionName}`);

            var checkDependentFunctionSecureSQL = `SELECT * FROM ${dependentDB}.INFORMATION_SCHEMA.FUNCTIONS WHERE FUNCTION_SCHEMA = '${dependentSchema}' AND FUNCTION_NAME = '${dependentFunctionName}' LIMIT 1`;
            var dependentFunctionScan = snowflake.execute({sqlText: checkDependentFunctionSecureSQL});

            // Check if the dependent UDF exists
            if (!dependentFunctionScan.next()) {
                var errStatement = `Input UDF: ${DB_NM}.${SCHEMA_NM}.${UDF_NM} depends on UDF: ${dependentDB}.${dependentSchema}.${dependentFunctionName} which does not exist!`;
                throwError(errStatement, "2003", "02000");
            }

            // Check if the dependent UDF is secure
            var isSecure = dependentFunctionScan.getColumnValue("IS_SECURE");
            if (isSecure !== "YES") {
                var secureFunctionError = `Input UDF: ${DB_NM}.${SCHEMA_NM}.${UDF_NM} depends on UDF: ${dependentDB}.${dependentSchema}.${dependentFunctionName} which is not a secure function. All dependent functions must be secure functions!`;
                throwError(secureFunctionError, "2003", "02000");
            }
        }

            // If the UDF exists, add response packet to get UDF Metadata
        var udfSql = `
                UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS
                SET RESPONSE = (
                    SELECT OBJECT_CONSTRUCT(
                        'UDF_ID', '${UDF_ID}',
                        'ORG_ID', '${ORG_ID}',
                        'FUNCTION_CATALOG', FUNCTION_CATALOG,
                        'FUNCTION_SCHEMA', FUNCTION_SCHEMA,
                        'FUNCTION_NAME', FUNCTION_NAME,
                        'ARGUMENT_SIGNATURE', ARGUMENT_SIGNATURE,
                        'DATA_TYPE', DATA_TYPE,
                        'FUNCTION_LANGUAGE', FUNCTION_LANGUAGE
                    )
                FROM ${DB_NM}.INFORMATION_SCHEMA.FUNCTIONS
                WHERE FUNCTION_CATALOG = '${DB_NM}'
                AND FUNCTION_SCHEMA = '${SCHEMA_NM}'
                AND FUNCTION_NAME = '${UDF_NM}'
                LIMIT 1
              )
              WHERE ID = '${REQUEST_ID}';
            `;

        snowflake.execute({sqlText: udfSql});
        // Logging message for response
        logStatement("Updating response and setting UDF Metadata JSON");
        result = "COMPLETE";
        msg = "UDF created successfully"
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
            binds: [opMsg, REQUEST_ID, Object.keys(this)[0]]
        }).execute();
    }
    return result;
    $$;

end;


