import shutil
import tempfile
import click
import click_log
import json
from base64 import b64decode
from re import search as regex_search
from os.path import abspath
from copy import deepcopy as clone
from convisoappsec.common.box import convert_sarif_to_sastbox1
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import project_code_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.logger import LOGGER
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from convisoappsec.flow.graphql_api.beta.models.issues.sast import (CreateSastFindingInput)
from convisoappsec.common.graphql.errors import ResponseError

click_log.basic_config(LOGGER)


@click.command()
@project_code_option()
@click.option(
    "-i",
    "--input-file",
    required=True,
    type=click.Path(exists=True),
    help='The path to SARIF file.',
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    "-r",
    "--repository-dir",
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    '--asset-name',
    required=False,
    envvar=("CONVISO_ASSET_NAME", "FLOW_ASSET_NAME"),
    help="Provides a asset name.",
)
@help_option
@pass_flow_context
@click.pass_context
def import_sarif(context, flow_context, project_code, input_file, company_id, repository_dir, asset_name):
    context.params['company_id'] = company_id if company_id is not None else None
    context.params['repository_dir'] = repository_dir
    asset_id = None
    experimental = False

    if project_code is None:
        prepared_context = RequirementsVerifier.prepare_context(clone(context))
        asset_id = prepared_context.params['asset_id']
        experimental = prepared_context.params['experimental']

    try:
        perform_command(
            flow_context,
            input_file,
            project_code,
            asset_id,
            experimental
        )

    except Exception as err:
        raise click.ClickException(str(err)) from err


def perform_command(flow_context, input_file, project_code=None, asset_id=None, experimental=False, internal=False):
    container_registry_token = flow_context.create_conviso_rest_api_client().docker_registry.get_sast_token()
    temporary_dir_path = tempfile.mkdtemp(prefix='conviso_')
    temporary_sarif_path = copy_file_to_dir(input_file, temporary_dir_path)

    sastboxv1_filepath = convert_sarif_to_sastbox1(
        temporary_sarif_path,
        temporary_dir_path,
        container_registry_token
    )

    if internal:
        # check if this function is called by the cli itself, then returns only the converted file.
        return sastboxv1_filepath

    print('Initializing the importation of SARIF results to the Conviso Platform...')

    if experimental:
        conviso_api = flow_context.create_conviso_api_client_beta()
        create_conviso_findings_from_sarif_on_new_flow(
            conviso_api=conviso_api,
            sastboxv1_filepath=sastboxv1_filepath,
            asset_id=asset_id,
            sarif_file=input_file
        )
    else:
        conviso_api = flow_context.create_conviso_rest_api_client()

        create_conviso_findings_from_sarif(
            conviso_api=conviso_api,
            sastboxv1_filepath=sastboxv1_filepath,
            project_code=project_code
        )


def create_conviso_findings_from_sarif(conviso_api, sastboxv1_filepath, project_code):
    with open(sastboxv1_filepath) as report_file:
        status_code = conviso_api.findings.create(
            project_code=project_code,
            finding_report_file=report_file,
            default_report_type="sast",
            commit_refs=None,
            deploy_id=None,
        )

        if status_code < 210:
            print('The results were successfully imported!')
        else:
            print(
                'Results were not imported. Conviso will be notified of this error.')

def create_conviso_findings_from_sarif_on_new_flow(conviso_api, sastboxv1_filepath, asset_id, sarif_file):
    duplicated_issues = 0

    with open(sastboxv1_filepath) as report_file, open(sarif_file) as file:
        issues = json.loads(report_file.read()).get("issues", [])
        results = json.load(file)['runs'][0]['results']

        for issue in issues:
            for result in results:
                issue_model = CreateSastFindingInput(
                    asset_id=asset_id,
                    file_name=issue.get("filename"),
                    vulnerable_line=issue.get("line") or 0,
                    title=issue.get("title") or result['ruleId'],
                    description=issue.get("description"),
                    severity=issue.get("severity"),
                    commit_ref=None,
                    deploy_id=None,
                    code_snippet=parse_code_snippet(issue.get("evidence")),
                    reference=parse_conviso_references(issue.get("references")),
                    first_line=parse_first_line_number(issue.get("evidence")),
                    original_issue_id_from_tool=None
                )

            try:
                conviso_api.issues.create_sast(issue_model)
            except ResponseError as error:
                if error.code == 'RECORD_NOT_UNIQUE':
                    duplicated_issues += 1
                else:
                    raise error

    msg = "💬 %s Issue/Issues ignored during duplication." % duplicated_issues
    LOGGER.info(msg)
    LOGGER.info("Successful importation of the SARIF file.")

def parse_code_snippet(encoded_base64):
    decoded_text = b64decode(encoded_base64).decode("utf-8")

    lines = decoded_text.split("\n")

    cleaned_lines = []
    for line in lines:
        cleaned_line = line.split(": ", 1)[-1]
        cleaned_lines.append(cleaned_line)

    code_snippet = "\n".join(cleaned_lines)

    return code_snippet

def parse_conviso_references(references=[]):
    DIVIDER = "\n"

    references_to_join = []

    for reference in references:
        if reference:
            references_to_join.append(reference)

    return DIVIDER.join(references_to_join)

def parse_first_line_number(encoded_base64):
    decoded_text = b64decode(encoded_base64).decode("utf-8")

    regex = r"^(\d+):"

    result = regex_search(regex, decoded_text)

    if result and result.group(1):
        return result.group(1)

    LINE_NUMBER_WHEN_NOT_FOUND = 1
    return LINE_NUMBER_WHEN_NOT_FOUND

def copy_file_to_dir(filepath, dir):
    source = abspath(filepath)

    filename = filepath.split('/')[-1]
    destination = '{}/{}'.format(abspath(dir), filename)

    shutil.copy(source, destination)
    return destination


import_sarif.epilog = '''
'''
EPILOG = '''
Examples:

  \b
  1 - Import results on SARIF file to Conviso Platform:
    $ export CONVISO_API_KEY='your-api-key'
    $ export CONVISO_PROJECT_CODE='your-project-code'
    $ {command} --input-file /path/to/file.sarif

'''  # noqa: E501

SHORT_HELP = "Perform import of vulnerabilities from SARIF file to Conviso Platform"

command = 'conviso findings import-sarif'
import_sarif.short_help = SHORT_HELP
import_sarif.epilog = EPILOG.format(
    command=command,
)
