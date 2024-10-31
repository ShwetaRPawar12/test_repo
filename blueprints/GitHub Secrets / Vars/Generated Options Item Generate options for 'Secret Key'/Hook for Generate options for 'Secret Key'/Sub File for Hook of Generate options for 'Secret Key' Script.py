from utilities.models import ConnectionInfo
from utilities.logger import ThreadLogger
from shared_modules.github_helper import GitHubManagerClient


def get_options_list(field, control_value=None, **kwargs):
    logger = ThreadLogger("fetch_github_secret_keys")
    logger.info(f"kwargs: {kwargs}")
    dict = kwargs["form_data"]
    gh_environment_secret_or_var = dict["form-0-gh_environment_secret_or_var"][0]
    gh_environment_repository_name = dict["form-0-gh_environment_search_result"][0]
    gh_environment_or_repo = dict["form-0-gh_environment_or_repo"][0]
    gh_environment_mode = dict["form-0-gh_environment_mode"][0]

    if gh_environment_secret_or_var == "Secret" and (
        gh_environment_mode == "Update Existing" or gh_environment_mode == "Delete"
    ):
        try:
            ci = ConnectionInfo.objects.get(name="GitHub Function Endpoint")
            function_base_url = f"https://{ci.ip}"
            function_code = ci.password

            # if not control_value:
            #    return [("", f"Enter a valid repository name for {control_value}")]

            if ci:
                if (
                    gh_environment_secret_or_var == "Secret"
                    and gh_environment_or_repo == "Repository"
                ):
                    logger.info("Received connection info for GitHub Function Endpoint")
                    github_manager_client = GitHubManagerClient(
                        function_base_url, function_code
                    )
                    logger.info(
                        "GitHub Manager Client created and fetching repository Secrets"
                    )
                    secrets = github_manager_client.list_repo_secrets(
                        gh_environment_repository_name
                    )
                    if secrets and len(secrets) > 0:
                        return [secret["name"] for secret in secrets]
                    else:
                        return [("", "--- Repository has no Secrets ---")]

                if (
                    gh_environment_secret_or_var == "Secret"
                    and gh_environment_or_repo == "Environment"
                ):
                    gh_environment_name = dict["form-0-gh_environment_name"][0]
                    logger.info("Received connection info for GitHub Function Endpoint")
                    github_manager_client = GitHubManagerClient(
                        function_base_url, function_code
                    )
                    logger.info(
                        "GitHub Manager Client created and fetching repository Secrets"
                    )
                    secrets = github_manager_client.list_env_secrets(
                        gh_environment_repository_name, gh_environment_name
                    )
                    if secrets and len(secrets) > 0:
                        logger.info(f"{secrets}")
                        return [secret["name"] for secret in secrets]
                    else:
                        return [("", "--- Repository Environment has no Secrets ---")]
            else:
                logger.info("Connection info couldn't be received")
                return [("", "--- Cannot find connection info ---")]
        except ConnectionInfo.DoesNotExist:
            return [("", "--- Cannot find connection info ---")]
        except Exception as e:
            return [("", f"--- {str(e)} ---")]
