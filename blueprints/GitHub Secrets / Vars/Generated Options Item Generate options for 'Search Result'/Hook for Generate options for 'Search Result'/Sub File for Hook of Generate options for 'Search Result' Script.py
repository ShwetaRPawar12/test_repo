from utilities.models import ConnectionInfo
from accounts.models import Group
from resources.models import ResourceType, Resource
from utilities.logger import ThreadLogger
from shared_modules.github_helper import GitHubManagerClient


def get_options_list(field, control_value=None, **kwargs):
    #logger = ThreadLogger("fetch_github_static")
    #logger.info(f"kwargs: {kwargs}")
    group_name = kwargs.get("group")
    #logger.info(f"kwargs: {kwargs}")
    #logger.info(f"resource: {group_name}")
    #logger.info(f"control: {control_value}")
    group = Group.objects.get(name=group_name)
    cws_type = ResourceType.objects.get(name="cloud_workspace")
    cws = Resource.objects.get(group=group, resource_type=cws_type, lifecycle="ACTIVE")
    #logger.info(f"leanix: {cws.leanix_app_id}")

    try:
        ci = ConnectionInfo.objects.get(name="GitHub Function Endpoint")
        function_base_url = f"https://{ci.ip}"
        function_code = ci.password

        if ci:
            #logger.info("Received connection info for GitHub Function Endpoint")
            github_manager_client = GitHubManagerClient(
                function_base_url, function_code
            )
            #logger.info(
            #    "GitHub Manager Client created and fetching repository environments"
            #)
            repos = github_manager_client.list_repository(
                control_value, f"{cws.leanix_app_id}"
            )
            #logger.info(f"Value: {repos}")
            #logger.info(f"Type: {type(repos)}")
            if repos and len(repos) > 0:
                result = []
                for repo in repos:
                    result.append((repo, repo))
                return result
            else:
                return [("", "--- Repository not found ---")]
        else:
            #logger.info("Connection info couldn't be received")
            return [("", "--- Cannot find connection info ---")]
    except ConnectionInfo.DoesNotExist:
        return [("", "--- Cannot find connection info ---")]
    except Exception as e:
        return [("", f"--- {str(e)} ---")]
