import traceback
import click
import json
import subprocess
import hashlib
import asyncio
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli.common import asset_id_option
from convisoappsec.flow.graphql_api.beta.models.issues.container import CreateOrUpdateContainerFindingInput
from convisoappsec.common.graphql.errors import ResponseError
from convisoappsec.common.retry_handler import RetryHandler
from convisoappsec.logger import log_and_notify_ast_event
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from copy import deepcopy as clone
from convisoappsec.flowcli.common import (
    asset_id_option,
    project_code_option,
)


@click.command()
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False
)
@asset_id_option(required=False)
@click.option(
    '-r',
    '--repository-dir',
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
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    hidden=True,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
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
@click.argument('image_name')
@help_option
@pass_flow_context
@click.pass_context
def run(
        context, flow_context, project_code, asset_id, company_id, repository_dir, send_to_flow, asset_name, vulnerability_auto_close, image_name,

):
    """ Run command for container vulnerability scan focused on OS vulnerabilities """
    context.params['company_id'] = company_id if company_id is not None else None
    prepared_context = RequirementsVerifier.prepare_context(clone(context))

    params_to_copy = [
        'asset_id', 'send_to_flow', 'asset_name', 'vulnerability_auto_close', 'project_code', 'repository_dir'
    ]

    for param_name in params_to_copy:
        context.params[param_name] = (
                locals()[param_name] or prepared_context.params[param_name]
        )

    scan_command = f"trivy image --pkg-types os --format json --output result.json {image_name}"

    asset_id = context.params['asset_id']
    company_id = context.params['company_id']

    try:
        log_func(f"🔧 Scanning image {image_name} ...")
        run_command(scan_command)
        log_func("✅ Scan completed successfully.")
        conviso_api = flow_context.create_conviso_api_client_beta()
        send_to_conviso_plataform(conviso_api, flow_context, asset_id, company_id)
    except Exception as error:
        log_func(f"❌ Scan failed: {error}")


def run_command(command):
    """
    Runs a shell command and logs its execution.

    Args:
        command (str): The scan command to execute.

    Returns:
        The result of a subproccess execution.
    """
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result

def send_to_conviso_plataform(conviso_api, flow_context, asset_id, company_id):
    """
    Process and send result to conviso platform.

    This method read the result file, parse and try to send all founded vulnerabilities
    If in any part of the process receive an error, should notify the ast-channel on conviso slack.

    Args:
        conviso_api (object): Responsable to comunicate with conviso graphql api.
        flow_content (object): Some helper methods.
        asset_id (int): The asset where the result will be sended.
        company_id (int): The user company on conviso platform.

    Returns:
        str: Could return a message inform about no vulnerabilities or None
    """
    log_func("🔧 Processing results ...")
    result_file = "result.json"

    try:
        with open(result_file, 'r') as file:
            scan_results = json.load(file)

        results = scan_results.get("Results", [])
        if results and isinstance(results, list) and len(results) > 0:
            vulnerabilities = results[0].get("Vulnerabilities", [])
        else:
            vulnerabilities = []

        if vulnerabilities:
            log_func(f"🔍 Sending {len(vulnerabilities)} vulnerabilities to conviso platform.")

            asyncio.run(send_vulnerabilities(flow_context, conviso_api, vulnerabilities, asset_id, company_id))

        else:
            log_func("✅ No vulnerabilities found.")

    except FileNotFoundError:
        log_func(f"❌ {result_file} not found. Ensure the scan was successful.")
        full_trace = traceback.format_exc()
        log_and_notify_ast_event(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id, ast_log=full_trace
        )
    except json.JSONDecodeError:
        log_func(f"❌ Failed to parse {result_file}. Ensure it is valid JSON.")
        full_trace = traceback.format_exc()
        log_and_notify_ast_event(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id, ast_log=full_trace
        )
    except Exception:
        full_trace = traceback.format_exc()
        log_func(f"❌ An error occurred while processing results: {full_trace}")
        log_and_notify_ast_event(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id, ast_log=full_trace
        )

async def send_vulnerabilities(flow_context, conviso_api, vulnerabilities, asset_id, company_id):
    tasks = []
    for vulnerability in vulnerabilities:
        task = asyncio.create_task(process_vulnerability(flow_context, conviso_api, vulnerability, asset_id, company_id))
        tasks.append(task)

    await asyncio.gather(*tasks)

async def process_vulnerability(flow_context, conviso_api, vulnerability, asset_id, company_id):
    # Generate a unique identifier for automatic vulnerability close
    # and determine whether the detected issue is new or an existing one to update.
    hash_issue = generate_vulnerability_hash(vulnerability)

    issue_model = CreateOrUpdateContainerFindingInput(
        asset_id=asset_id,
        title=vulnerability.get("Title", ""),
        description=vulnerability.get("Description", "No description provided."),
        severity=vulnerability.get("Severity", ""),
        solution="Use latest image version",
        reference=parse_references(vulnerability.get("References", [])),
        affected_version=vulnerability.get("InstalledVersion", ""),
        package=vulnerability.get("PkgName", ""),
        cve=vulnerability.get("VulnerabilityID", ""),
        patched_version=vulnerability.get('FixedVersion', None),
        category=parse_category(vulnerability.get('CweIDs', [])),
        original_issue_id_from_tool=str(hash_issue)
    )

    try:
        conviso_api.issues.create_container(issue_model)
    except ResponseError as error:
        if error.code == 'RECORD_NOT_UNIQUE':
            pass
        else:
            retry_handler = RetryHandler(
                flow_context=flow_context, company_id=company_id, asset_id=asset_id
                                    )
            retry_handler.execute_with_retry(conviso_api.issues.create_container, issue_model)
    except Exception:
        retry_handler = RetryHandler(
            flow_context=flow_context, company_id=company_id, asset_id=asset_id
        )
        retry_handler.execute_with_retry(conviso_api.issues.create_container, issue_model)


def parse_references(references):
    """
    Parses and formats a list of references into a single string separated by newlines.

    This function takes a list of reference strings and joins them using a newline character
    as the separator, returning the resulting formatted string.

    Args:
        references (list): A list of reference strings to be formatted.

    Returns:
        str: A single string with each reference separated by a newline.
    """
    DIVIDER = "\n"

    return DIVIDER.join(references)


def parse_category(category):
    """
    Parses and converts a list of CWE values to a comma-separated string.

    This function takes a list of CWE values, joins them into a single string
    separated by commas, and returns the resulting string.

    Args:
        category (list): A list of CWE values (strings or other convertible types).

    Returns:
        str: A comma-separated string of CWE values.
    """
    category = ", ".join(category)

    return category


def generate_vulnerability_hash(data):
    """
    Generate a hash from specific immutable fields in a vulnerability dictionary.

    :param data: The dictionary representing a vulnerability.
    :return: A string representing the hash.
    """
    keys = ["Title", "PkgID", "PkgName", "InstalledVersion", "Description", "VulnerabilityID"]
    extracted_data = {key: data[key] for key in keys if key in data}
    serialized_data = json.dumps(extracted_data, sort_keys=True)

    return hashlib.sha256(serialized_data.encode('utf-8')).hexdigest()

def log_func(msg, new_line=True):
    """
    Output a message to the console with styled formatting.

    This function uses `click` to output a styled message to the console. It supports
    controlling whether the message ends with a newline and writes the output to `stderr`.

    Args:
        msg (str): The message to log.
        new_line (bool, optional): Whether to append a newline at the end of the message.
            Defaults to True.

    Returns:
        None
    """
    click.echo(click.style(msg), nl=new_line, err=True)
