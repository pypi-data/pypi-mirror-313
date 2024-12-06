import click

from redbeard_cli import snowflake_utils
from redbeard_cli.commands.init import (
    habu_setup as habu_setup_command
)


@click.command("version")
def version():
    habu_setup_command.pkg_version()


@click.command()
@click.option('--conf-file-name', '-c', default="habu_snowflake_config.yaml",
              help="Configuration file name to generate")
@click.option('--account_name', '-a', prompt="Client account name")
@click.option('--organization_name', '-o', prompt="Client organization name")
@click.option('--role', '-r', default="ACCOUNTADMIN", prompt="Role to use")
@click.option('--warehouse', '-w', default="CLEAN_ROOM_SETUP_WH", prompt="Warehouse to use for installation")
@click.option('--user', '-u', default="clean_room_user", prompt="Clean room user")
@click.option('--auth-type',
              type=click.Choice(['sso', 'keypair', 'password'], case_sensitive=False), prompt="Authentication Type", default="sso")
def generate_config(conf_file_name: str, account_name: str, organization_name: str, role: str, warehouse: str, user: str,
                    auth_type: str):
    habu_setup_command.generate_config(conf_file_name, account_name, organization_name, role, warehouse, user, auth_type)


@click.group()
def init():
    pass


@init.command(
    help="""Initialize Full Habu Snowflake framework.\n
    This will create all the objects required to run the Habu Agent in the specified Snowflake account.\n
    This includes:\n
      * Databases:\n
        * HABU_CLEAN_ROOM_COMMON\n
        * HABU_DATA_CONNECTIONS\n
    """
)
@click.option('-o', '--organization_id', required=True, help='Habu Organization ID')
@click.option('-c', '--config-file', default="./habu_snowflake_config.yaml",
              help='Snowflake account configuration file')
@click.option('-h', '--habu-account',
              help='Habu Snowflake account details used for orchestration in following format: <HABU_ORGANIZATION_NAME>.<HABU_ACCOUNT_NAME>')
def habu_framework(habu_account: str, config_file: str, organization_id: str):
    sf_connection, connection_params = snowflake_utils.new_connection_from_yaml_file(config_file)
    habu_setup_command.init_framework(sf_connection, organization_id, habu_account, connection_params['warehouse'])
