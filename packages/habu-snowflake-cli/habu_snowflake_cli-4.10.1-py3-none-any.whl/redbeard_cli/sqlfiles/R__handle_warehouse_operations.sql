BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_WAREHOUSE_OPERATIONS()
    RETURNS STRING
    LANGUAGE JAVASCRIPT STRICT
    EXECUTE AS OWNER AS
    $$
    // Installs the handler for creating a new warehouse
    try {
        var warehouseRequestSql = "SELECT id AS request_id, " +
            " request_data:clean_room_id AS clean_room_id, " +
            " request_data:warehouse_name AS warehouse_name, " +
            " request_data:warehouse_size AS warehouse_size, " +
            " request_data:warehouse_type AS warehouse_type, " +
            " request_data:auto_suspend AS auto_suspend, " +
            " request_data:auto_resume AS auto_resume, " +
            " request_data:initially_suspended AS initially_suspended, " +
            " request_data:min_cluster_count AS min_cluster_count, " +
            " request_data:max_cluster_count AS max_cluster_count, " +
            " request_data:scaling_policy AS scaling_policy, " +
            " request_data:enable_query_acceleration AS enable_query_acceleration, " +
            " request_data:query_acceleration_scaling_factor AS query_acceleration_scaling_factor, " +
            " request_data:max_concurrency_level AS max_concurrency_level, " +
            " request_data:warehouse_operation AS warehouse_operation " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

        var stmt = snowflake.createStatement({
            sqlText: warehouseRequestSql,
            binds: ['NEW_WAREHOUSE_OPERATION', 'PENDING']
        });

        var rs = stmt.execute();
        var createWarehouseCommandParams = [];
        var deleteWarehouseCommandParams = [];
        while (rs.next()) {
            var warehouseOperation = rs.getColumnValue(15); // warehouse operation
            switch (warehouseOperation) {
                case 'CREATE': {
                    var requestID = rs.getColumnValue(1);
                    var cleanRoomID = rs.getColumnValue(2);
                    var warehouseName = rs.getColumnValue(3);
                    var warehouseSize = rs.getColumnValue(4);
                    var warehouseType = rs.getColumnValue(5);
                    var autoSuspend = rs.getColumnValue(6);
                    var autoResume = rs.getColumnValue(7);
                    var initiallySuspended = rs.getColumnValue(8);
                    var minClusterCount = rs.getColumnValue(9);
                    var maxClusterCount = rs.getColumnValue(10);
                    var scalingPolicy = rs.getColumnValue(11);
                    var enableQueryAcceleration = rs.getColumnValue(12);
                    var queryAccelerationScalingFactor = rs.getColumnValue(13);
                    var maxConcurrencyLevel = rs.getColumnValue(14);

                    createWarehouseCommandParams.push({
                        'requestID': requestID,
                        'cleanRoomID': cleanRoomID,
                        'warehouseName': warehouseName,
                        'warehouseSize': warehouseSize,
                        'warehouseType': warehouseType,
                        'autoSuspend': autoSuspend,
                        'autoResume': autoResume,
                        'initiallySuspended': initiallySuspended,
                        'minClusterCount': minClusterCount,
                        'maxClusterCount': maxClusterCount,
                        'scalingPolicy': scalingPolicy,
                        'enableQueryAcceleration': enableQueryAcceleration,
                        'queryAccelerationScalingFactor': queryAccelerationScalingFactor,
                        'maxConcurrencyLevel': maxConcurrencyLevel,
                    })
                    snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                    });
                    break;
                }

                case 'DELETE': {
                    var requestID = rs.getColumnValue(1);
                    var cleanRoomID = rs.getColumnValue(2);
                    var warehouseName = rs.getColumnValue(3);
                    deleteWarehouseCommandParams.push({
                        'requestID': requestID,
                        'cleanRoomID': cleanRoomID,
                        'warehouseName': warehouseName,
                    })
                    snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                    });
                    break;
                }
            }
        }

        for (const warehouseparam of createWarehouseCommandParams) {
            var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.CREATE_NEW_WAREHOUSE(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)',
                binds: [
                    warehouseparam['requestID'],
                    warehouseparam['cleanRoomID'],
                    warehouseparam['warehouseName'],
                    warehouseparam['warehouseSize'],
                    warehouseparam['warehouseType'],
                    warehouseparam['autoSuspend'],
                    warehouseparam['autoResume'],
                    warehouseparam['initiallySuspended'],
                    warehouseparam['minClusterCount'],
                    warehouseparam['maxClusterCount'],
                    warehouseparam['scalingPolicy'],
                    warehouseparam['enableQueryAcceleration'],
                    warehouseparam['queryAccelerationScalingFactor'],
                    warehouseparam['maxConcurrencyLevel'],
                ]
            });
            stmt.execute();
        }
        for (const warehouseparam of deleteWarehouseCommandParams) {
            var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.DELETE_WAREHOUSE(:1, :2, :3)',
                binds: [
                    warehouseparam['requestID'],
                    warehouseparam['cleanRoomID'],
                    warehouseparam['warehouseName'],
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


CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CREATE_NEW_WAREHOUSE(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, WH_NAME VARCHAR, WH_SIZE VARCHAR, WH_TYPE VARCHAR, AUTO_SUSPEND VARCHAR, AUTO_RESUME VARCHAR, INITIALLY_SUSPENDED VARCHAR, MIN_CLUSTER_COUNT VARCHAR, MAX_CLUSTER_COUNT VARCHAR, SCALING_POLICY VARCHAR, ENABLE_QUERY_ACCELERATION VARCHAR, QUERY_ACCELERATION_SCALING_FACTOR VARCHAR, MAX_CONCURRENCY_LEVEL VARCHAR)
    RETURNS STRING
    LANGUAGE JAVASCRIPT
    STRICT
    EXECUTE AS OWNER
    AS
    $$
    function logStatement(message) {
        snowflake.createStatement({
            sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
            binds: [message, REQUEST_ID, Object.keys(this)[0]]
        }).execute();
    }

    try {
        // Create Warehouse per cleanRoom
        var create_warehouse_sql = `CREATE WAREHOUSE IF NOT EXISTS ${WH_NAME} \
                                            WITH WAREHOUSE_SIZE = ${WH_SIZE} \
                                            WAREHOUSE_TYPE = ${WH_TYPE} \
                                            AUTO_SUSPEND = ${AUTO_SUSPEND} \
                                            AUTO_RESUME = ${AUTO_RESUME} \
                                            INITIALLY_SUSPENDED = ${INITIALLY_SUSPENDED} \
                                            MIN_CLUSTER_COUNT = ${MIN_CLUSTER_COUNT} \
                                            MAX_CLUSTER_COUNT = ${MAX_CLUSTER_COUNT} \
                                            SCALING_POLICY = ${SCALING_POLICY} \
                                            ENABLE_QUERY_ACCELERATION = ${ENABLE_QUERY_ACCELERATION} \
                                            QUERY_ACCELERATION_MAX_SCALE_FACTOR = ${QUERY_ACCELERATION_SCALING_FACTOR} \
                                            MAX_CONCURRENCY_LEVEL = ${MAX_CONCURRENCY_LEVEL} \
                                            COMMENT = '${CLEAN_ROOM_ID}';`
        logStatement(`Logging create_warehouse_sql for - ${WH_NAME} is - ${create_warehouse_sql}`);
        var resultSet = snowflake.execute({ sqlText: create_warehouse_sql });
        logStatement(`Created Warehouse - ${WH_NAME} for cleanroomID - ${CLEAN_ROOM_ID}`);
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


CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.DELETE_WAREHOUSE(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, WH_NAME VARCHAR)
    RETURNS STRING
    LANGUAGE JAVASCRIPT
    STRICT
    EXECUTE AS OWNER
    AS
    $$
    function logStatement(message) {
        snowflake.createStatement({
            sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
            binds: [message, REQUEST_ID, Object.keys(this)[0]]
        }).execute();
    }

    try {
        // Drop Warehouse SQL
        var drop_warehouse_sql = `DROP WAREHOUSE IF EXISTS ${WH_NAME};`
        logStatement(`Logging drop warehouse sql for - ${WH_NAME} is - ${drop_warehouse_sql}`);
        var resultSet = snowflake.execute({ sqlText: drop_warehouse_sql });
        logStatement(`Dropped Warehouse - ${WH_NAME} for cleanroomID - ${CLEAN_ROOM_ID}`);
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

