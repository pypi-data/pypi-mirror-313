from redbeard_cli import snowflake_utils, file_utils


def install_clean_room_objects(sf_connection):

    sp_sql = file_utils.get_file_contents('sqlfiles/R__handle_error.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__sp_logger.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__process_request.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__handle_new_cleanrooms.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__handle_new_cleanrooms.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__create_new_dataset.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__create_new_dataset.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__create_new_cleanroom_udf.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__question_run_data_share.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__new_question_run.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__new_question_run.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__question_run_cleanup.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__handle_management_command.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__new_data_connection.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)
 
    sp_sql = file_utils.get_file_contents('sqlfiles/R__new_user_defined_function.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__handle_warehouse_operations.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__post_run_query.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__question_run_result_share.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__question_run_accept_result_share.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__setup_streams_tasks.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

