import click
import json

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import project_code_option, on_http_error


@click.command()
@project_code_option()
@click.option(
    '-c',
    '--current-tag',
    required=False,
    help="Used to filter by current tag.",
)
@help_option
@pass_flow_context
def ls(flow_context, project_code, current_tag):
    try:
        flow = flow_context.create_conviso_rest_api_client()
        deploys = flow.deploys.list(project_code, current_tag)
        deploys_json = json.dumps(deploys, indent=2)
        click.echo(deploys_json)
    except Exception as e:
        on_http_error(e)
        raise click.ClickException(str(e)) from e
