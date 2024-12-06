import click
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import CreateDeployException, DeployFormatter, PerformDeployException, \
    project_code_option, asset_id_option
from convisoappsec.flowcli.deploy.create.context import pass_create_context
from convisoappsec.flowcli.deploy.create.with_.values import values
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from convisoappsec.flowcli.sast import sast
from convisoappsec.flowcli.sca import sca
from convisoappsec.flowcli.iac import iac
from convisoappsec.flowcli.vulnerability import vulnerability
from convisoappsec.logger import LOGGER
from copy import deepcopy as clone
from convisoappsec.flow import GitAdapter
from convisoappsec.flowcli.context import pass_flow_context


def get_default_params_values(cmd_params):
    """ Further information in https://click.palletsprojects.com/en/8.1.x/api/?highlight=params#click.Command.params

    Args:
        cmd_params (List[click.core.Parameter]):

    Returns:
        dict: default params values dictionarie
    """
    default_params = {}
    for param in cmd_params:
        unwanted = param.name in ['help', 'verbosity']
        if not unwanted:
            default_params.update({param.name: param.default})
    return default_params


def parse_params(ctx_params: dict, expected_params: list):
    """ Parse the params from the context extracting the expected params values to the context.

    Args:
        ctx_params (dict): context params: Further information at https://click.palletsprojects.com/en/8.1.x/api/?highlight=context%20param#click.Context.params
        expected_params (list): Further information at https://click.palletsprojects.com/en/8.1.x/api/?highlight=params#click.Command.params

    Returns:
        dict: parsed_params: parsed params as key and value
    """
    parsed_params = get_default_params_values(expected_params)
    for param in ctx_params:
        if param in parsed_params:
            parsed_params.update({param: ctx_params.get(param)})
    return parsed_params


def perform_sast(context) -> None:
    """Setup and runs the "sast run" command.

    Args:
        context (<class 'click.core.Context'>): cloned context
    """
    sast_run = sast.commands.get('run')

    specific_params = {
        "deploy_id": context.obj.deploy['id'],
        "start_commit": context.obj.deploy['previous_commit'],
        "end_commit": context.obj.deploy['current_commit'],
    }
    context.params.update(specific_params)
    context.params = parse_params(context.params, sast_run.params)
    try:
        LOGGER.info(
            'Running SAST on deploy ID "{deploy_id}"...'
            .format(deploy_id=context.params["deploy_id"])
        )
        sast_run.invoke(context)

    except Exception as err:
        raise click.ClickException(str(err)) from err


def perform_sca(context) -> None:
    """Setup and runs the "sca run" command.

    Args:
        context (<class 'click.core.Context'>): cloned context
    """
    sca_run = sca.commands.get('run')
    context.params.update({"deploy_id": context.obj.deploy['id']})
    context.params = parse_params(context.params, sca_run.params)
    try:
        LOGGER.info(
            'Running SCA on deploy ID "{deploy_id}"...'
            .format(deploy_id=context.params["deploy_id"])
        )
        sca_run.invoke(context)

    except Exception as err:
        raise click.ClickException(str(err)) from err


def perform_iac(context) -> None:
    """Setup and runs the "iac run" command.

    Args:
        context (<class 'click.core.Context'>): clonned context
    """
    iac_run = iac.commands.get('run')
    context.params.update({"deploy_id": context.obj.deploy['id']})
    context.params = parse_params(context.params, iac_run.params)

    try:
        LOGGER.info(
            'Running IAC on deploy ID "{deploy_id}"...'
            .format(deploy_id=context.params["deploy_id"])
        )
        iac_run.invoke(context)
    except Exception as err:
        raise click.ClickException(str(err)) from err


def perform_vulnerabilities_service(context) -> None:
    auto_close_run = vulnerability.commands.get('run')

    specific_params = {
        "deploy_id": context.obj.deploy['id'],
        "start_commit": context.obj.deploy['previous_commit'],
        "end_commit": context.obj.deploy['current_commit'],
        "company_id": context.params['company_id']
    }
    context.params.update(specific_params)
    context.params = parse_params(context.params, auto_close_run.params)

    try:
        LOGGER.info("[*] Verifying if any vulnerability was fixed...")
        auto_close_run.invoke(context)
    except Exception as err:
        raise click.ClickException(str(err)) from err


def perform_deploy(context, flow_context, prepared_context):
    """Setup and runs the "deploy create with values" command.

    Args:
        context (<class 'click.core.Context'>): clonned context
        flow_context:

    Returns:
        dict: deploy
         int: deploy.id
         int: deploy.project_id
         str: deploy.current_tag
         str: deploy.previous_tag
         str: deploy.current_commit
         str: deploy.previous_commit
         str: deploy.created_at
    """
    context.obj.output_formatter = DeployFormatter(
        format=DeployFormatter.DEFAULT
    )
    context.params = parse_params(context.params, values.params)
    try:
        LOGGER.info("Creating new deploy...")
        created_deploy = values.invoke(context)
        try:

            conviso_api = flow_context.create_conviso_graphql_client()
            api_key = flow_context.key
            git_adapter = GitAdapter(context.params['repository_dir'])
            zipped_file = git_adapter.zip_git_folder()
            branch_name = git_adapter.get_branch_name()

            response = conviso_api.deploys.create_deploy(
                asset_id=prepared_context.params['asset_id'],
                previous_commit=created_deploy['previous_commit'],
                current_commit=created_deploy['current_commit'],
                branch_name=branch_name,
                diff_content=zipped_file,
                api_key=api_key
            )

            response_deploy_id = response['createDeploy']['deploy']['id']
            deploy_id = { "deploy_id": response_deploy_id }
            created_deploy.update(deploy_id)
        except:
            pass

        if created_deploy:
            return created_deploy

        raise CreateDeployException("Deploy not created.")

    except CreateDeployException as err:
        raise PerformDeployException(err)

    except Exception as err:
        raise click.ClickException(str(err)) from err


@click.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True
    )
)
@asset_id_option(
    required=False
)
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
    hidden=True
)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(exists=True, resolve_path=True),
    required=False,
    help="""The source code repository directory.""",
)
@click.option(
    "-c",
    "--current-commit",
    required=False,
    help="If no value is given the HEAD commit of branch is used. [DEPLOY]",
)
@click.option(
    "-p",
    "--previous-commit",
    required=False,
    help="""If no value is given, the value is retrieved from the lastest
    deploy at flow application. [DEPLOY]""",
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    '--asset-name',
    required=False,
    envvar=("CONVISO_ASSET_NAME", "FLOW_ASSET_NAME"),
    help="Provides a asset name.",
)
@click.option(
    '--vulnerability-auto-close',
    default=False,
    is_flag=True,
    hidden=True,
    help="Enable auto fixing vulnerabilities on cp.",
)
@help_option
@pass_flow_context
@pass_create_context
@click.pass_context
def run(context, create_context, flow_context, **kwargs):
    """ AST - Application Security Testing. Unifies deploy issue, SAST and SCA analyses.  """
    try:
        prepared_context = RequirementsVerifier.prepare_context(clone(context), from_ast=True)
        try:
            prepared_context.obj.deploy = perform_deploy(clone(prepared_context), flow_context, prepared_context)
        except:
            return

        perform_sast(clone(prepared_context))
        perform_sca(clone(prepared_context))
        perform_iac(clone(prepared_context))

        if context.params['vulnerability_auto_close'] is True:
            perform_vulnerabilities_service(clone(prepared_context))

    except PerformDeployException as err:
        LOGGER.warning(err)

    except Exception as err:
        raise click.ClickException(str(err)) from err


@click.group()
def ast():
    pass


ast.add_command(run)
