import sys
from dotenv import load_dotenv

sys.path.append(".")
sys.path.append("..")

import click

from redbeard_cli.commands.init import cli as init_cli


@click.group()
def cli():
    pass


load_dotenv(dotenv_path="./.env", override=True)
cli.add_command(init_cli.init)
cli.add_command(init_cli.version)
cli.add_command(init_cli.generate_config)
