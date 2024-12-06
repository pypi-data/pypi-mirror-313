BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_STREAM_TASKS(ORGANIZATON_ID VARCHAR, HABU_ACCOUNT_ID  VARCHAR, CUSTOMER_ACCOUNT_ID VARCHAR)
returns string
language javascript
execute as owner as
$$
    // at this point, we have accepted the share for the organization database from the habu account
    // habu_org_xxx_db contains a table called clean_room_requests that is shared with the customer
    // we are now going to setup a stream for the clean_room_requests table so that we can setup
    // the machinery for db-rpc
    var sf_org_id = ORGANIZATON_ID.replace(/-/g, '').toUpperCase();
    var setup_stream_sql = "CREATE OR REPLACE STREAM CLEAN_ROOM.CLEAN_ROOM_REQUESTS_STREAM \
        ON TABLE HABU_ORG_" + sf_org_id + "_SHARE_DB.CLEAN_ROOM.CLEAN_ROOM_REQUESTS \
        APPEND_ONLY=TRUE \
        COMMENT = 'HABU_" + CUSTOMER_ACCOUNT_ID + "'";
    snowflake.execute({ sqlText: setup_stream_sql });
    // stream has been setup, now create a task that listens to the stream and triggers the
    // PROCESS_ORG_REQUEST stored procedure to process pending clean room requests
    var copy_task_sql = "CREATE OR REPLACE TASK CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        SCHEDULE = '1 MINUTE' \
        ALLOW_OVERLAPPING_EXECUTION = TRUE \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        WHEN SYSTEM$STREAM_HAS_DATA('CLEAN_ROOM.CLEAN_ROOM_REQUESTS_STREAM') \
        AS CALL CLEAN_ROOM.PROCESS_ORG_REQUEST()"
    snowflake.execute({ sqlText: copy_task_sql });
    var new_clean_rooms_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOMS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOMS()"
    snowflake.execute({ sqlText: new_clean_rooms_task });
    var new_datasets_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_DATASETS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_NEW_DATASETS()"
    snowflake.execute({ sqlText: new_datasets_task });
    var question_run_data_share_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE()"
    snowflake.execute({ sqlText: question_run_data_share_task });
    var question_run_cleanup_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP()"
    snowflake.execute({ sqlText: question_run_cleanup_task });
    var question_run_result_share_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE()"
    snowflake.execute({ sqlText: question_run_result_share_task });
    var question_run_accept_result_share_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE()"
    snowflake.execute({ sqlText: question_run_accept_result_share_task });
    var new_question_runs_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS_TASK \
        WAREHOUSE = HABU_CLEAN_ROOM_COMMON_XLARGE_WH \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS()"
    snowflake.execute({ sqlText: new_question_runs_task });
    var post_run_query_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_POST_RUN_QUERY_TASK \
        WAREHOUSE = HABU_CLEAN_ROOM_COMMON_XLARGE_WH \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_POST_RUN_QUERY()"
    snowflake.execute({ sqlText: post_run_query_task });
    mgmt_commands_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_MGMT_COMMANDS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_MANAGEMENT_COMMANDS()"
    snowflake.execute({ sqlText: mgmt_commands_task });
    add_data_connection_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION_TASK \
            USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
            AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
            AS CALL CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION()"
    snowflake.execute({ sqlText: add_data_connection_task });
    add_user_defined_function_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_USER_DEFINED_FUNCTION_TASK \
            USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
            AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
            AS CALL CLEAN_ROOM.HANDLE_NEW_USER_DEFINED_FUNCTION()"
    snowflake.execute({ sqlText: add_user_defined_function_task });
    add_clean_room_udf_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOM_UDF_TASK \
            USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
            AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
            AS CALL CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOM_UDF()"
    snowflake.execute({ sqlText: add_clean_room_udf_task });
    var new_warehouse_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_WAREHOUSE_OPERATIONS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_WAREHOUSE_OPERATIONS()"
    snowflake.execute({ sqlText: new_warehouse_task });
    // tasks are created in 'suspend' mode root and all dependent tasks need to be enabled explicitly
    // TODO: fails with error - SQL compilation error: Query called from a stored procedure contains a function with side effects [SYSTEM$TASK_DEPENDENTS_ENABLE]
    // snowflake.execute({ sqlText: "SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK')" });
    // Since recursively resuming all the dependent task tied to root task is not working,
    // explicitly resuming all the tasks in reverse order. Children tasks muste be started before the root task.
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_POST_RUN_QUERY_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_USER_DEFINED_FUNCTION_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_MGMT_COMMANDS_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_DATASETS_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOMS_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOM_UDF_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_WAREHOUSE_OPERATIONS_TASK RESUME" });

    // DROP EXISTING WAREHOUSE BASED TASKS - Not required as it is handles by the root task
    let warehouseSizes = ["XSMALL", "XLARGE", "X2LARGE", "X3LARGE", "X4LARGE", "SNOWPARK_X2LARGE", "SNOWPARK_XLARGE"];

    // Loop through each warehouse size and drop the corresponding task
    for (let size of warehouseSizes) {
        let taskName = `CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS_WITH_${size}_TASK`;
        let sqlText = `DROP TASK IF EXISTS ${taskName}`;
        snowflake.execute({ sqlText: sqlText });
        let pendingMessageTaskName = `CLEAN_ROOM.CHECK_QUESTION_RUN_REQUESTS_FOR_${size}_TASK`;
        let pendingMessageSqlText = `DROP TASK IF EXISTS ${pendingMessageTaskName}`;
        snowflake.execute({ sqlText: pendingMessageSqlText });
    }

    // Drop pending messages procedure
    var dropPendingMessageProcedureSql = "DROP PROCEDURE IF EXISTS CLEAN_ROOM.PENDING_MESSAGE_COUNT_FOR_WAREHOUSE_TYPE(VARCHAR)";
    snowflake.execute({ sqlText: dropPendingMessageProcedureSql });

    // Resuming root task
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK RESUME" });

return "Setup of stream and tasks successful";
$$;
end;

