from utilities.models import ConnectionInfo
from utilities.logger import ThreadLogger
from shared_modules.github_helper import GitHubManagerClient


def get_options_list(field, control_value=None, **kwargs):
    logger = ThreadLogger("fetch_github_repo_environments")
    logger.info(f"kwargs: {kwargs}")

    try:
        ci = ConnectionInfo.objects.get(name="GitHub Function Endpoint")
        function_base_url = f"https://{ci.ip}"
        function_code = ci.password

        if not control_value:
            return [("", "Enter a valid repository name")]

        if ci:
            logger.info("Received connection info for GitHub Function Endpoint")
            github_manager_client = GitHubManagerClient(
                function_base_url, function_code
            )
            logger.info(
                "GitHub Manager Client created and fetching repository environments"
            )
            repo_environments = github_manager_client.list_repository_environments(
                control_value
            )

            if repo_environments and len(repo_environments) > 0:
                return repo_environments
            else:
                return [("", "--- Repository has no environments ---")]
        else:
            logger.info("Connection info couldn't be received")
            return [("", "--- Cannot find connection info ---")]
    except ConnectionInfo.DoesNotExist:
        return [("", "--- Cannot find connection info ---")]
    except Exception as e:
        return [("", f"--- {str(e)} ---")]
# https://raw.githubusercontent.com/dvag/ct-cloudbolt-scripts/develop/actions/generate_options/github/secret_key.py