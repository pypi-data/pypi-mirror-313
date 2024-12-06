import jmespath
import json
import requests
from convisoappsec.flow.graphql_api.v1.models.asset import AssetInput
from convisoappsec.flow.graphql_api.v1.models.project import CreateProjectInput, UpdateProjectInput
from convisoappsec.flow.graphql_api.v1.schemas import mutations, resolvers
from urllib.parse import urlparse
from convisoappsec.version import __version__


class AssetsAPI(object):
    """ To operations on Asset's resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def create_asset(self, asset_input: AssetInput):
        graphql_variables = asset_input.to_graphql_dict()

        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.CREATE_ASSET,
            graphql_variables
        )

        expected_path = 'createAsset.asset'

        asset = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return asset

    def update_asset(self, company_id, asset_id, asset_name, technologies=None, repo_url=None):
        graphql_variables = {
            "id": asset_id,
            "companyId": company_id,
            "name": asset_name,
            "tecnologyList": technologies,
            "repoUrl": repo_url
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.UPDATE_ASSET,
            graphql_variables
        )

        expected_path = 'updateAsset.asset'

        asset = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return asset

    def get_by_company_id_or_name(self, company_id, asset_name, page, limit):
        graphql_variables = {
            "id": company_id,
            'name': asset_name,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_ASSETS,
            graphql_variables
        )

        expected_path = 'assets.collection'

        assets_by_company = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return assets_by_company

    def get_asset_url(self, company_id, asset_id):
        parsed_url = urlparse(self.__conviso_graphql_client.url)

        asset_path = '/scopes/{}/assets/{}'.format(
            company_id,
            asset_id
        )

        parsed_url = parsed_url._replace(path=asset_path)

        return parsed_url.geturl()

    def list_assets(self, params, page=1, limit=32):
        graphql_variables = {
            "id": params.company_id,
            "name": params.name,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_ASSETS,
            graphql_variables
        )

        expected_path = 'assets.collection'

        assets = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return assets


class ProjectsApi(object):
    """ To operations on Project's resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def create_project(self, project_input: CreateProjectInput):
        graphql_variables = project_input.to_graphql_dict()

        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.CREATE_PROJECT,
            graphql_variables
        )

        expected_path = 'createProject.project'

        project = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return project

    def update_project(self, project_input: UpdateProjectInput):
        graphql_variables = project_input.to_graphql_dict()

        self.__conviso_graphql_client.execute(
            mutations.UPDATE_PROJECT,
            graphql_variables
        )

    def get_by_code_or_label(self, project_code, project_label, company_id, page=1, limit=32):
        graphql_variables = {
            "project_code": project_code,
            "project_label": project_label,
            "company_id": company_id,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_PROJECTS,
            graphql_variables
        )

        expected_path = 'projects.collection'

        projects = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return projects


class CompaniesApi(object):
    """ To operations on Companies resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def get_company_by_id(self, company_id):
        graphql_variables = {
            "company_id": company_id,
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_COMPANY,
            graphql_variables
        )

        expected_path = 'company'
        company = jmespath.search(
            expected_path,
            graphql_body_response,
        )
        return company

    def get_companies(self, page=1, limit=10):
        graphql_variables = {
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_COMPANIES,
            graphql_variables
        )

        expected_path = 'companies.collection'

        companies = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return companies


class IssuesApi(object):
    """ To operations on Issue's resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def get_issues_stats(self, asset_id, company_id, statuses, end_date=None):
        """ Return issue stats filter by asset and company """

        graphql_variables = {
            'asset_id': asset_id,
            'company_id': company_id,
            'statuses': statuses,
            'end_date': end_date
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_ISSUES_STATS,
            graphql_variables
        )

        expected_path = 'issuesStats.severities'

        issues_stats = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return issues_stats


class DeploysApi(object):
    """ Class for deploys resources """

    def __init__(self, conviso_graphql_client):
        self._conviso_graphql_client = conviso_graphql_client

    def get_deploys_by_asset(self, asset_id):
        """ Returns deploys based on the provided asset id """

        graphql_variables = {
            'asset_id': asset_id
        }

        graphql_body_response = self._conviso_graphql_client.execute(
            resolvers.GET_DEPLOYS_BY_ASSET,
            graphql_variables
        )

        expected_path = 'deploysByAsset.collection'

        deploys = jmespath.search(
            expected_path,
            graphql_body_response
        )

        return deploys

    def create_deploy(self, asset_id, previous_commit, current_commit, branch_name, diff_content, api_key):
        """create a deployment"""

        url = self._conviso_graphql_client.url

        operations = {
            "query": mutations.CREATE_DEPLOY,
            "variables": {
                "assetId": asset_id,
                "previousCommit": previous_commit,
                "currentCommit": current_commit,
                "branchName": branch_name,
                "diffContent": None
            }
        }

        file_map = {
            "0": ["variables.diffContent"]
        }

        with open(diff_content, 'rb') as diff_content_data:
            files = {
                'operations': (None, json.dumps(operations), 'application/json'),
                'map': (None, json.dumps(file_map), 'application/json'),
                '0': (diff_content, diff_content_data, 'application/octet-stream')
            }

            headers = {
                'x-api-key': f'{api_key}',
                "User-Agent": "AST:{version}".format(version=__version__)
            }

            response = requests.post(url, files=files, headers=headers)

            response.raise_for_status()
            json_response = response.json()

            self._handle_graphql_errors(json_response)

            return json_response.get('data')

    # TODO: extract
    @staticmethod
    def _handle_graphql_errors(json_response):
        """ Handle GraphQL errors """
        if 'errors' in json_response:
            errors = json_response['errors']
            for error in errors:
                print(f"GraphQL Error: {error.get('message')}")
            raise Exception("GraphQL request failed with errors.")


class SbomApi(object):
    """ Class for sbom file resources """

    def __init__(self, conviso_graphql_client):
        self._conviso_graphql_client = conviso_graphql_client

    def send_sbom_file(self, company_id, asset_id, file_path, api_key):
        """ Send SBOM file to Conviso platform """

        url = self._conviso_graphql_client.url

        operations = {
            "query": mutations.IMPORT_SBOM,
            "variables": {
                "companyId": company_id,
                "assetId": asset_id,
                "file": None
            }
        }

        file_map = {
            "0": ["variables.file"]
        }

        with open(file_path, 'rb') as sbom_file:
            files = {
                'operations': (None, json.dumps(operations), 'application/json'),
                'map': (None, json.dumps(file_map), 'application/json'),
                '0': (file_path, sbom_file, 'application/octet-stream')
            }

            headers = {
                'x-api-key': f'{api_key}',
                "User-Agent": "AST:{version}".format(version=__version__)
            }

            response = requests.post(url, files=files, headers=headers)

            response.raise_for_status()
            json_response = response.json()

            self._handle_graphql_errors(json_response)

            return json_response.get('data')

    @staticmethod
    def _handle_graphql_errors(json_response):
        """ Handle GraphQL errors """
        if 'errors' in json_response:
            errors = json_response['errors']
            for error in errors:
                print(f"GraphQL Error: {error.get('message')}")
            raise Exception("GraphQL request failed with errors.")


class LogAstError(object):
    """ Class to send AST errors to Conviso Platform """
    def __init__(self, conviso_graphql_client):
        self._conviso_graphql_client = conviso_graphql_client

    def send_ast_error(self, company_id, asset_id, log):
        """ send log with company and asset to Conviso Platform """

        graphql_variables = {
            'companyId': str(company_id),
            'assetId': str(asset_id),
            'log': log
        }

        graphql_body_response = self._conviso_graphql_client.execute(
            mutations.LOG_AST_ERROR,
            graphql_variables
        )

        expected_path = 'success'

        success = jmespath.search(
            expected_path,
            graphql_body_response
        )

        return success
