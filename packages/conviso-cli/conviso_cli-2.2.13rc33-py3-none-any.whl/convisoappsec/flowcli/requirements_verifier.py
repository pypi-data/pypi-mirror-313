import re
from convisoappsec.flowcli.common import CreateDeployException
from convisoappsec.logger import LOGGER
from convisoappsec.flowcli.projects.ls import Projects
from convisoappsec.flowcli.companies.ls import Companies
from convisoappsec.flow.graphql_api.v1.models.asset import AssetInput
from convisoappsec.flow.graphql_api.v1.models.project import CreateProjectInput, UpdateProjectInput
from convisoappsec.common.git_data_parser import GitDataParser
from .context import pass_flow_context


class RequirementsVerifier:

    @staticmethod
    @pass_flow_context
    def list_assets(flow_context, company_id, asset_name, scan_type):
        conviso_api = flow_context.create_conviso_graphql_client()

        asset_model = AssetInput(
            int(company_id),
            asset_name,
            scan_type
        )

        return conviso_api.assets.list_assets(asset_model)

    @staticmethod
    @pass_flow_context
    def create_asset(flow_context, company_id, asset_name, scan_type):
        conviso_api = flow_context.create_conviso_graphql_client()

        asset_model = AssetInput(
            int(company_id),
            asset_name,
            scan_type
        )

        return conviso_api.assets.create_asset(asset_model)

    @staticmethod
    @pass_flow_context
    def create_project(flow_context, company_id, asset_id, label):
        conviso_api = flow_context.create_conviso_graphql_client()

        project_model = CreateProjectInput(
            company_id,
            asset_id,
            label
            )

        return conviso_api.projects.create_project(project_model)

    @staticmethod
    @pass_flow_context
    def update_project(flow_context, project_id, asset_id):
        conviso_api = flow_context.create_conviso_graphql_client()

        project_model = UpdateProjectInput(
            project_id,
            asset_id,
        )

        conviso_api.projects.update_project(project_model)

    @staticmethod
    def sarif_asset_assignment(context, asset):
        """ assignment asset when is a sarif import """
        context.params['asset_id'] = asset['id']
        context.params['experimental'] = True

        return context

    @staticmethod
    def find_or_create_asset(context, company_id, old_name, new_name):
        """ Method to find or create asset on conviso platform """
        try:
            existing_assets = RequirementsVerifier.list_assets(company_id, new_name, 'SAST')
            if not existing_assets:
                existing_assets = RequirementsVerifier.list_assets(company_id, old_name, 'SAST')
            for asset in existing_assets:
                if asset['name'] == old_name or asset['name'] == new_name:
                    LOGGER.info('✅ Asset found...')
                    context.params['asset_name'] = asset['name']
                    return [asset]
            LOGGER.info('💬 Asset not found; creating...')
            new_asset = RequirementsVerifier.create_asset(company_id, new_name, 'SAST')
            context.params['asset_name'] = new_name
            return [new_asset]
        except Exception as e:
            raise Exception("Error: {}".format(e))

    @staticmethod
    def create_asset_with_custom_name(context, company_id, asset_name):
        """ Create an asset with custom name pass with a custom name """

        # we need to verify if already has an asset with the name provided.
        # because graphql will return an error if already has.
        existing_asset = RequirementsVerifier.list_assets(company_id, asset_name, 'SAST')

        if not existing_asset:
            LOGGER.info("💬 Asset not found; creating with name {}...".format(asset_name))
            asset = RequirementsVerifier.create_asset(company_id, asset_name, 'SAST')
        else:
            LOGGER.info('✅ Asset found...')
            asset = existing_asset[0]

        context.params['asset_name'] = asset_name

        return asset

    @staticmethod
    def find_or_create_project(context, project_label, company_id, asset_id):
        """ find or create a project to perform a deployment """
        projects = Projects()
        existing_project = projects.ls(flow_context=context, project_label=project_label, company_id=company_id)

        if not existing_project:
            project = RequirementsVerifier.create_project(company_id, asset_id, project_label)
            return [project]
        elif len(existing_project) > 1:
            error_msg = 'You need to specify the project using --project-code.'
            raise CreateDeployException(error_msg)

        return existing_project

    @staticmethod
    @pass_flow_context
    def prepare_context(flow_context, context, from_ast=False):
        """ Due to the new vulnerability management we need to do some checks before continuing the flow """
        project_code = context.params['project_code']
        new_management_flag = 'CONVISO_NEW_ISSUE_MANAGEMENT_ALLOWED_COMPANY'
        asset_target = None

        if from_ast is True:
            context.params['from_ast'] = True

        if project_code:
            projects = Projects()
            projects_filtered = projects.ls(
                flow_context=flow_context,
                project_code=project_code
                )

            if len(projects_filtered) == 0:
                raise CreateDeployException("⚠️ Project doesn't exists!")

            LOGGER.info('💬 Project found ...')

            project = projects_filtered[0]
            custom_features = project['company']['customFeatures']

            if new_management_flag not in custom_features:
                context.params['experimental'] = False

                return context

            assets = project['assets']
            asset_name = GitDataParser(context.params['repository_dir']).parse_name()

            if len(assets) == 0:
                LOGGER.info('💬 Asset not found, creating ...')
                asset_target = RequirementsVerifier.create_asset(project['company']['id'], asset_name, 'SAST')
                RequirementsVerifier.update_project(project['id'], asset_target['id'])

            elif len(assets) == 1:
                LOGGER.info('✅ Asset found...')
                asset_target = assets[0]
            elif len(assets) > 1:
                for asset in assets:
                    if asset['name'] == asset_name:
                        LOGGER.info('✅ Asset found...')
                        asset_target = asset
                        break

            if not asset_target:
                LOGGER.info('⚠️ Asset not found')
                raise CreateDeployException("❌ Sorry, was not possible find the asset")

            context.params['asset_id'] = asset_target['id']
            context.params['experimental'] = True

            return context
        else:  # New flow
            companies = Companies()
            company_id = context.params['company_id']

            if company_id is not None:
                companies_filtered = [companies.ls(flow_context, company_id=company_id)]
            else:
                companies_filtered = companies.ls(flow_context)

            if len(companies_filtered) > 1:
                raise CreateDeployException(
                    "❌ Deploy not created. You have access to multiple companies; please specify one using CONVISO_COMPANY_ID."
                )

            company = companies_filtered[0]
            company_id = company['id']

            if new_management_flag not in company['customFeatures']:
                error_msg = "Deploy not created. The company '{}' does not have access to the new vulnerability management.".format(company['label'])
                raise CreateDeployException(error_msg)

            if context.params['asset_name'] is not None:
                # if user use --asset-name param or envvar CONVISO_ASSET_NAME, FLOW_ASSET_NAME
                asset_name = context.params['asset_name']
                asset = RequirementsVerifier.create_asset_with_custom_name(context, company_id, asset_name)
            else:
                pattern = r"\([^)]*\)"  # eliminating what is in parentheses
                old_asset_name = GitDataParser(context.params['repository_dir']).parse_name()
                new_asset_name = re.sub(pattern, '', old_asset_name).strip()

                assets = RequirementsVerifier.find_or_create_asset(context, company_id, old_asset_name, new_asset_name)
                asset = assets[0]

            if 'input_file' in context.params:
                # sarif only uses assets, not requiring the creation of a project.
                RequirementsVerifier.sarif_asset_assignment(context, asset)

                return context

            asset_name = asset['name']
            project_label = asset_name + '_ast'

            if 'projects' not in asset or len(asset['projects']) == 0:
                LOGGER.info('💬 AST Project not found; creating...')
                project = RequirementsVerifier.find_or_create_project(
                    flow_context, project_label, company_id, asset['id']
                )
                project = project[0]
                RequirementsVerifier.update_project(project['id'], asset['id'])
                project_code = project['apiCode']
            else:
                projects = asset['projects']

                for project in projects:
                    if project['type'] == 'ast' and project['label'] == project_label:
                        LOGGER.info('✅ AST Project found...')
                        project_code = project['apiCode']
                        break
                else:
                    LOGGER.info('💬 AST Project not found; we will create one...')
                    project = RequirementsVerifier.find_or_create_project(
                        flow_context, project_label, company_id, asset['id']
                    )
                    project_code = project[0]['apiCode']

            context.params['project_code'] = project_code
            context.params['asset_id'] = asset['id']
            context.params['experimental'] = True
            context.params['company_id'] = company_id

            return context
