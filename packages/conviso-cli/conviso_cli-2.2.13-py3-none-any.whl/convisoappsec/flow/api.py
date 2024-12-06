import copy
import json
from contextlib import suppress
from os import SEEK_SET
from urllib.parse import urljoin

import jsonschema
import requests

PRODUCTION_API_URL = "https://app.convisoappsec.com"
STAGING_API_URL = "https://staging.convisoappsec.com"
DEVELOPMENT_API_URL = "http://localhost:3000"
DEFAULT_API_URL = PRODUCTION_API_URL


class RequestsSession(requests.Session):

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)

        return super().request(
            method, url, *args, **kwargs
        )


class FlowAPIException(Exception):
    pass


class FlowAPIAccessDeniedException(FlowAPIException):
    pass


class DeployNotFoundException(FlowAPIException):
    pass


class Deploys(object):
    DIFF_CONTENT_FILE_NAME = 'diff_content.txt'
    DIFF_CONTENT_MIME_TYPE = 'text/plain'
    COMMIT_AUTHORS_FILE_NAME = 'commit_authors.yaml'
    COMMIT_AUTHORS_MIME_TYPE = 'text/yaml'
    COMMIT_HISTORY_FILE_NAME = 'commit_history.yaml'
    COMMIT_HISTORY_MIME_TYPE = 'text/yaml'
    ENDPOINT = '/api/v3/deploys'
    LIST_BY_PROJECT_ENPOINT = "api/v2/deploys/deploys_by_project_api_code"

    def __init__(self, client):
        self.client = client

    def create(self, project_code, **kargs):
        current_version = kargs.get('current_version')
        previous_version = kargs.get('previous_version')
        diff_content = kargs.get('diff_content')
        project_metrics = kargs.get('project_metrics')
        commit_authors = kargs.get('commit_authors')
        commit_history = kargs.get('commit_history')

        files = {
            'api_code': (None, project_code),

            'deploy[current_version][commit]': (None, current_version.get('commit')),  # noqa: E501
            'deploy[current_version][tag]': (None, current_version.get('tag')),

            'deploy[previous_version][commit]': (None, previous_version.get('commit')),  # noqa: E501
            'deploy[previous_version][tag]': (None, previous_version.get('tag'))  # noqa: E501
        }

        if project_metrics:
            total_lines = project_metrics.get('total_lines')

            files.update({
                'deploy[project][metrics][total_lines]': (None, total_lines),
            })

        with suppress(TypeError):
            metrics = kargs.get('metrics')
            files.update({
                'deploy[metrics][new_lines]': (None, metrics['added_lines']),
                'deploy[metrics][removed_lines]': (None, metrics['deleted_lines']),  # noqa
                'deploy[metrics][changed_lines]': (None, metrics['changed_lines']),  # noqa
            })

        if diff_content:
            self._assert_filepointer_is_at_beginning(diff_content)
            diff_content_args = (
                self.DIFF_CONTENT_FILE_NAME,
                diff_content,
                self.DIFF_CONTENT_MIME_TYPE,
            )

            files.update({
                'deploy[diff_content]': diff_content_args,
            })

        if commit_authors:
            commit_authors_args = (
                self.COMMIT_AUTHORS_FILE_NAME,
                commit_authors,
                self.COMMIT_AUTHORS_MIME_TYPE,
            )

            files.update({
                'deploy[authors]': commit_authors_args,
            })

        if commit_history:
            commit_history_args = (
                self.COMMIT_HISTORY_FILE_NAME,
                commit_history,
                self.COMMIT_HISTORY_MIME_TYPE,
            )

            files.update({
                'deploy[commit_history]': commit_history_args,
            })

        session = self.client.requests_session
        response = session.post(self.ENDPOINT, files=files)

        response.raise_for_status()

        return response.json()

    def list(self, project_code, current_tag=None):
        data = {
            'api_code': project_code,
        }

        if current_tag:
            data.update({
                'current_tag': current_tag
            })

        session = self.client.requests_session
        response = session.get(self.LIST_BY_PROJECT_ENPOINT, json=data)
        response.raise_for_status()

        return {
            "deploys": response.json()
        }

    def get(self, project_code, current_tag):
        if not current_tag:
            raise ValueError(
                "current_tag is required and must be not empty"
            )

        list_result = self.list(project_code, current_tag)

        try:
            deploys = list_result.get('deploys')
            return deploys[0]
        except IndexError as e:
            raise DeployNotFoundException(
                "Deploy for current_tag[%s] not found" % current_tag
            ) from e

    def exists(self, project_code, current_tag):
        try:
            self.get(project_code, current_tag)
        except DeployNotFoundException:
            return False

        return True

    def get_latest(self, project_code):
        get_latest_endpoint = "%s/last" % self.ENDPOINT
        request_data = {
            'api_code': project_code
        }

        session = self.client.requests_session
        response = session.get(get_latest_endpoint, json=request_data)
        try:
            response.raise_for_status()
            deploy = response.json()

            if not deploy:
                raise DeployNotFoundException()

            return deploy
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise DeployNotFoundException() from error
            if error.response.status_code == 401:
                raise FlowAPIAccessDeniedException(
                    "Access denied, check if your flow api key is valid"
                ) from error

            raise error

    @staticmethod
    def _assert_filepointer_is_at_beginning(diff_content):
        def is_seekable(f):
            return hasattr(f, 'seekable') and f.seekable()

        if is_seekable(diff_content):
            diff_content.seek(SEEK_SET)


class FindingReportLoader(object):
    ISSUES_FIELD = 'issues'

    def __init__(self, findings_reports, max_issues=25):
        self.max_issues = max_issues
        self._generator = self._create_generator(self, findings_reports)

    def read(self):
        return self._generator

    @classmethod
    def _create_generator(cls, loader, findings_reports):
        for report in findings_reports:
            report_data = json.load(report)
            issues = report_data.get(cls.ISSUES_FIELD, [])

            while True:
                first_n_issues, issues = (
                    issues[:loader.max_issues],
                    issues[loader.max_issues:]
                )

                if first_n_issues:
                    yield first_n_issues
                else:
                    break


class Findings(object):
    ENDPOINT = '/findings'
    REPORT_TYPE_FIELD = 'type'

    def __init__(self, client):
        self.client = client

    def create(self, project_code, commit_refs, finding_report_file, **kwargs):
        finding_report = json.load(finding_report_file)

        self.__inject_dynamic_finding_report_fields(
            finding_report, commit_refs, **kwargs
        )

        data = {
            'flow_project_id': project_code,
            'flow_deploy_id': kwargs.get('deploy_id'),
            'report': finding_report,
        }

        session = self.client.requests_session
        response = session.post(self.ENDPOINT, json=data)
        response.raise_for_status()
        return response.status_code

    @classmethod
    def __inject_dynamic_finding_report_fields(
        cls, finding_report, commit_refs, **kwargs
    ):
        report_dynamic_injected_fields = {}
        report_dynamic_injected_fields.update({
            'code_version': commit_refs,
            'source': cls.__parse_engine_reporter(finding_report)
        })

        default_report_type = kwargs.get('default_report_type')

        if default_report_type and cls.REPORT_TYPE_FIELD not in finding_report:
            report_dynamic_injected_fields.update({
                cls.REPORT_TYPE_FIELD: default_report_type
            })

        finding_report.update(report_dynamic_injected_fields)

    @classmethod
    def __parse_engine_reporter(cls, finding_report):
        report_issues = finding_report.get('issues', [])
        if len(report_issues) == 0:
            return None

        return report_issues[0].get('reporter', None)


class DockerRegistry(object):
    SAST_ENDPOINT = '/auth/public_auth'

    def __init__(self, client):
        self.client = client

    def get_sast_token(self):
        session = self.client.requests_session
        response = session.get(self.SAST_ENDPOINT)
        response.raise_for_status()
        return response.text


class SecurityGate(object):
    SEC_GATE_VULNS_ENDPOINT = '/api/v3/security_gate/vulnerabilities'
    SEC_GATE_VULNS_RULES_SCHEMA_ENDPOINT = '/api/v3/security_gate/vulnerabilities/jsonschema'  # noqa

    def __init__(self, client):
        self.client = client

    def vulnerabilities(self, project_code, rules):
        self.__validate_vulnerabilities_rules(rules)

        data = copy.deepcopy(rules)
        data['api_code'] = project_code

        session = self.client.requests_session
        response = session.post(self.SEC_GATE_VULNS_ENDPOINT, json=data)
        response.raise_for_status()
        return response.json()

    def __validate_vulnerabilities_rules(self, rules):
        try:
            vulns_rules_schema = self.__vulnerabilities_rules_schema()
            jsonschema.validate(
                schema=vulns_rules_schema,
                instance=rules
            )
        except jsonschema.exceptions.ValidationError as e:
            path = [
                str(p) for p in e.path
            ]

            path_name = '/'.join(path)

            message = "At {0}. Details: {1}".format(
                path_name, e.message
            )

            raise ValueError(message)

    def __vulnerabilities_rules_schema(self):
        session = self.client.requests_session
        response = session.get(self.SEC_GATE_VULNS_RULES_SCHEMA_ENDPOINT)
        response.raise_for_status()
        return response.json()


class RESTClient(object):

    def __init__(
        self,
        url=STAGING_API_URL,
        key=None,
        insecure=False,
        user_agent=None,
        ci_provider_name=None
    ):
        self.url = url
        self.insecure = insecure
        self.key = key
        self.user_agent = user_agent
        self.ci_provider_name = ci_provider_name

    @property
    def requests_session(self):
        session = RequestsSession(self.url)
        session.verify = not self.insecure

        session.headers.update({
            'x-api-key': self.key,
            'x-flowcli-ci-provider-name': self.ci_provider_name
        })

        if self.user_agent:
            user_agent_header = {}
            name = self.user_agent.get('name')
            version = self.user_agent.get('version')

            if name and version:
                user_agent_header_fmt = "{name}/{version}"
                user_agent_header_content = user_agent_header_fmt.format(
                    name=name,
                    version=version,
                )

                user_agent_header = {
                    'User-Agent': user_agent_header_content
                }

            session.headers.update(user_agent_header)

        return session

    @property
    def deploys(self):
        return Deploys(self)

    @property
    def findings(self):
        return Findings(self)

    @property
    def docker_registry(self):
        return DockerRegistry(self)

    @property
    def security_gate(self):
        return SecurityGate(self)

# TODO: Create Custom handle
# requests.exceptions.ConnectionError
# requests.exceptions.SSLError
# requests.exceptions.HTTPError
