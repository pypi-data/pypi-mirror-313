import click
import click_log

from convisoappsec.flowcli.common import on_http_error
from convisoappsec.common import safe_join_url
from convisoappsec.logger import LOGGER
from convisoappsec.flow.graphql_api.v1.client import ConvisoGraphQLClient

click_log.basic_config(LOGGER)


class Projects:
    def ls(self, flow_context, project_code="", project_label="", company_id="", page=1, limit=10):
        try:
            url = safe_join_url(flow_context.url, "/graphql")
            conviso_api = ConvisoGraphQLClient(api_url=url, api_key=flow_context.key)

            return perform_command(conviso_api, project_code, project_label, company_id, page, limit)

        except Exception as exception:
            on_http_error(exception)
            raise click.ClickException(str(exception)) from exception


def perform_command(conviso_api, project_code, project_label, company_id, page, limit):
    projects_found = conviso_api.projects.get_by_code_or_label(
        project_code,
        project_label,
        company_id,
        page,
        limit
    )

    return projects_found
