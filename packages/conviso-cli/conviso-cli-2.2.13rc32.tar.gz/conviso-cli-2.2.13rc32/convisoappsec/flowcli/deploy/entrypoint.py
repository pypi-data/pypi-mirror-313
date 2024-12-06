import click

from convisoappsec.flowcli import help_option

from .create import create
from .show import show
from .ls import ls


@click.group()
@help_option
def deploy():
    pass


deploy.add_command(create)
deploy.add_command(ls)
deploy.add_command(show)

deploy.epilog = '''
  Run flow deploy COMMAND --help for more information on a command.
'''
