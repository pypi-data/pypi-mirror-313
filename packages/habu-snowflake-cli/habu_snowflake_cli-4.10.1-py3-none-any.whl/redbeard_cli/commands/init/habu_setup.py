from redbeard_cli import snowflake_utils, file_utils
import pkg_resources
from redbeard_cli.commands.init.clean_room_setup import install_clean_room_objects
import getpass


def init_framework(sf_connection, organization_id: str, habu_org_name_account_name_combo: str, warehouse: str):

    version = pkg_resources.require("habu-snowflake-cli")[0].version
    print("Going to install/upgrade to " + version)

    sp_sql = file_utils.get_file_contents('sqlfiles/V1_0_0_create.sql')
    snowflake_utils.run_multiple_statements(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__setup_cleanroom_common.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__setup_data_connection_objects.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__1init_habu_installer.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    sp_sql = file_utils.get_file_contents('sqlfiles/R__init_habu_shares.sql')
    snowflake_utils.run_query(sf_connection, sp_sql)

    result = snowflake_utils.fetch_one_query(sf_connection, "CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.INSTALLER()")
    print(result)
    install_clean_room_objects(sf_connection)
    if habu_org_name_account_name_combo is None:
        result = snowflake_utils.fetch_one_query(sf_connection,
                                                 "CALL HABU_CLEAN_ROOM_COMMON.HABU_SCHEMA.INIT_FRAMEWORK('%s')" % (
                                                     organization_id))
    else:
        result = snowflake_utils.fetch_one_query(sf_connection,
                                                 "CALL HABU_CLEAN_ROOM_COMMON.HABU_SCHEMA.INIT_FRAMEWORK('%s', '%s')" % (
                                                 organization_id, habu_org_name_account_name_combo))

    print(result)

    if "Habu framework init successful" in result:
        snowflake_utils.run_query(sf_connection, "USE WAREHOUSE %s" % warehouse)
        snowflake_utils.run_query(
            sf_connection,
            """
            merge into HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.APP_METADATA d using (select 'VERSION_INFO' as METADATA_NAME, '%s' as METADATA_VALUE ) s
                on d.METADATA_NAME = s.METADATA_NAME
                when matched then update set d.METADATA_VALUE = s.METADATA_VALUE, d.UPDATED_AT = current_timestamp()
                when not matched then insert (ID, METADATA_NAME, METADATA_VALUE, CREATED_AT) values (uuid_string(), s.METADATA_NAME, s.METADATA_VALUE, current_timestamp()
            );""" % version
        )
        return 0
    else:
        return 1


def pkg_version():
    version = pkg_resources.require("habu-snowflake-cli")[0].version
    print("Package version: " + version)


def generate_config(conf_file_name: str, account_name: str, organization_name: str, role: str, warehouse: str, user: str,
                    auth_type: str):

    f = open(conf_file_name, "w")
    f.write('''accountName: {accountName}
organizationName: {organizationName}
role: {role}
warehouse: {warehouse}
user: {user}'''.format(accountName=account_name, organizationName=organization_name, role=role, warehouse=warehouse, user=user))

    if auth_type == "password":
        password = getpass.getpass("Please enter password: ")
        f.write(f'\npassword: {password}')

    if auth_type == "keypair":
        key_path = input("Please enter keypair file path: ")
        key_pass = getpass.getpass("Please enter keypair file password: ")
        f.write(f'\nkey_path: {key_path}')
        f.write(f'\nkey_pass: {key_pass}')

    f.write("\n")
    f.close()
    return None
