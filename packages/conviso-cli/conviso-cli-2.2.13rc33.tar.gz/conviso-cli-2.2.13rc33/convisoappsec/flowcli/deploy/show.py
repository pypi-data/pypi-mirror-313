import click

from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import DeployFormatter
from convisoappsec.flowcli.common import project_code_option, on_http_error


@click.command()
@help_option
@project_code_option()
@click.argument('current-tag', required=True)
@click.option(
    '-f',
    '--output-format',
    required=False,
    type=click.Choice(DeployFormatter.FORMATS()),
    default=DeployFormatter.DEFAULT,
    show_default=True,
)
@pass_flow_context
def show(flow_context, project_code, current_tag, output_format):
    try:
        flow = flow_context.create_conviso_rest_api_client()
        deploy = flow.deploys.get(project_code, current_tag)
        formatter = DeployFormatter(output_format)
        click.echo(
            formatter.format(deploy)
        )
    except Exception as e:
        on_http_error(e)
        raise click.ClickException(str(e)) from e
