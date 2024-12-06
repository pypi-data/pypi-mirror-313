import click
import git
# TODO: refactoring. all deploy create share some behavior
from convisoappsec.flow.util import project_metrics
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.deploy.create.context import pass_create_context
from convisoappsec.flow import GitAdapter
from convisoappsec.flow import api
from convisoappsec.flowcli.common import project_code_option, on_http_error
from convisoappsec.logger import LOGGER
from copy import deepcopy as clone
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier


class SameCommitException(Exception):
    pass


@click.command()
@help_option
@project_code_option()
@click.option(
    "-c",
    "--current-commit",
    required=False,
    help="If no value is given the HEAD commit of branch is used.",
)
@click.option(
    "-p",
    "--previous-commit",
    required=False,
    help="""If no value is given, the value is retrieved from the lastest
    deploy at flow application.""",
)
@click.option(
    "-r",
    "--repository-dir",
    required=False,
    type=click.Path(exists=True, resolve_path=True),
    default='.',
    show_default=True,
    help="Repository directory.",
)
@click.option(
    "--attach-diff/--no-attach-diff",
    default=True,
    show_default=True,
    required=False,
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    "--asset-id",
    required=False,
    envvar=("CONVISO_ASSET_ID", "FLOW_ASSET_ID"),
    help="Asset ID on Conviso Platform",
)
@click.option(
    '--from-ast',
    default=False,
    is_flag=True,
    hidden=True,
    help="Internal use only.",
)
@pass_create_context
@pass_flow_context
@click.pass_context
def values(
    context, flow_context, create_context, repository_dir, project_code,
    company_id, current_commit, previous_commit, attach_diff, asset_id, from_ast
):
    context.params['company_id'] = company_id if company_id is not None else None

    if not from_ast:
        prepared_context = RequirementsVerifier.prepare_context(clone(context))
        project_code = prepared_context.params['project_code']

    try:
        flow = flow_context.create_conviso_rest_api_client()
        git_adapter = GitAdapter(repository_dir)

        current_commit = current_commit or git_adapter.head_commit
        if not previous_commit:
            try:
                latest_deploy = flow.deploys.get_latest(project_code)
                previous_commit = latest_deploy.get('current_commit')

                if not previous_commit:
                    previous_tag = latest_deploy.get('current_tag')
                    previous_commit = git_adapter.show_commit_from_tag(previous_tag)
            except api.DeployNotFoundException:
                previous_commit = git_adapter.empty_repository_tree_commit

            # validating if the commit exists in the repository before creating any deploy.
            if previous_commit != '4b825dc642cb6eb9a060e54bf8d69288fbee4904':
                try:
                    git_adapter._repo.commit(previous_commit)
                except (git.exc.BadName, ValueError):
                    # If the commit doesn't exist, fetch commits from conviso platform
                    # to validate if any of then exists in the repo before scanning all repo again.
                    commits = deploys_from_asset(asset_id=context.params['asset_id'])
                    previous_commit = None

                    for commit in commits:
                        commit_hash = commit['currentCommit']
                        try:
                            # Check if the current commit exists in the repo
                            git_adapter._repo.commit(commit_hash)
                            previous_commit = commit_hash
                            break
                        except (git.exc.BadName, ValueError):
                            continue

                    if previous_commit is None:
                        previous_commit = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

        if previous_commit == current_commit:
            LOGGER.info(
                create_context.output_formatter.format(latest_deploy)
            )
            raise SameCommitException(
                "Previous commit ({0}) and Current commit ({1}) are the same, nothing to do."
                .format(previous_commit, current_commit)
            )

        diff_content = None

        if attach_diff:
            diff_content = git_adapter.diff(
                previous_commit,
                current_commit,
            )

        deploy_metrics = git_adapter.diff_stats(
            previous_commit,
            current_commit,
        ).dict

        authors_data = git_adapter.get_commit_authors_by_range(
            previous_commit, current_commit
        )

        deploy_metrics_msg_fmt = 'Fetching deploy metrics between [{}] and [{}]'
        LOGGER.debug(deploy_metrics_msg_fmt.format(
            previous_commit, current_commit))
        LOGGER.debug('Deploy metrics: {}'.format(deploy_metrics))

        project_metrics_data = project_metrics(repository_dir)
        LOGGER.debug('Project metrics: {}'.format(project_metrics_data))

        commit_history = git_adapter.get_commit_history()

        deploy = flow.deploys.create(
            project_code,
            current_version={'commit': current_commit},
            previous_version={'commit': previous_commit},
            diff_content=diff_content,
            metrics=deploy_metrics,
            project_metrics=project_metrics_data,
            commit_authors=authors_data,
            commit_history=commit_history
        )

        click.echo(
            create_context.output_formatter.format(deploy)
        )
        return deploy

    except SameCommitException as e:
        LOGGER.warning(e)

    except Exception as e:
        on_http_error(e)
        raise click.ClickException(str(e)) from e


@pass_flow_context
def deploys_from_asset(flow_context, asset_id):
    """ Returns all deploys from an asset """

    conviso_api = flow_context.create_conviso_graphql_client()

    return conviso_api.deploys.get_deploys_by_asset(asset_id=asset_id)
