from common.methods import set_progress
from utilities.models import ConnectionInfo
from shared_modules.github_helper import GitHubManagerClient


def run(job, *args, **kwargs):
    order = job.parent_job.get_order()
    boi = order.orderitem_set.first().cast()
    barg = boi.blueprintitemarguments_set.first()

    repository_name = barg.get_value_for_custom_field("gh_environment_search_result")
    environment = barg.get_value_for_custom_field("gh_environment_name")
    secret_key = barg.get_value_for_custom_field("gh_environment_secret_key")
    secret_value = barg.get_value_for_custom_field("gh_environment_secret_value")
    kind = barg.get_value_for_custom_field("gh_environment_secret_or_var")
    scope = barg.get_value_for_custom_field("gh_environment_or_repo")
    new_secret_key = barg.get_value_for_custom_field("gh_environment_secret_key_new")
    mode = barg.get_value_for_custom_field("gh_environment_mode")
    variable_key = barg.get_value_for_custom_field("gh_environment_var_key")
    new_variable_key = barg.get_value_for_custom_field("gh_environment_var_key_new")
    variable_value = barg.get_value_for_custom_field("gh_environment_var_value")
    secret_key_env = barg.get_value_for_custom_field("gh_environment_secret_key_env")
    variable_key_env = barg.get_value_for_custom_field("gh_environment_variable_key_env")

    set_progress(f"Repository Name: {repository_name}")
    set_progress(f"Environment: {environment}")
    set_progress(f"Secret Key: {secret_key}")

    try:
        ci = ConnectionInfo.objects.get(name="GitHub Function Endpoint")
        function_base_url = f"https://{ci.ip}"
        function_code = ci.password

        if ci:
            if kind == "Secret" and scope == "Repository" and mode == "Update Existing":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_repo_secrets(
                    repository_name=repository_name,
                    secretKey=secret_key,
                    secretValue=secret_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Secret" and scope == "Repository" and mode == "Delete":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                delete_secret = github_manager_client.delete_repo_secrets(
                    repository_name=repository_name, secretKey=secret_key
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if (
                kind == "Secret"
                and scope == "Environment"
                and mode == "Update Existing"
            ):
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_env_secrets(
                    repository_name=repository_name,
                    environment_name=environment,
                    secretKey=secret_key_env,
                    secretValue=secret_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Secret" and scope == "Environment" and mode == "Delete":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                delete_secret = github_manager_client.delete_env_secrets(
                    repository_name=repository_name,
                    environment_name=environment,
                    secretKey=secret_key_env,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Secret" and scope == "Repository" and mode == "Create New":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_repo_secrets(
                    repository_name=repository_name,
                    secretKey=new_secret_key,
                    secretValue=secret_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Secret" and scope == "Environment" and mode == "Create New":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_env_secrets(
                    repository_name=repository_name,
                    environment_name=environment,
                    secretKey=new_secret_key,
                    secretValue=secret_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )

            if (
                kind == "Variable"
                and scope == "Repository"
                and mode == "Update Existing"
            ):
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_repo_variables(
                    repository_name=repository_name,
                    variableKey=variable_key,
                    variableValue=variable_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Variable" and scope == "Repository" and mode == "Delete":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.delete_repo_variables(
                    repository_name=repository_name, variableKey=variable_key
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if (
                kind == "Variable"
                and scope == "Environment"
                and mode == "Update Existing"
            ):
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_env_variables(
                    repository_name=repository_name,
                    environment_name=environment,
                    variableKey=variable_key_env,
                    variableValue=variable_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Variable" and scope == "Environment" and mode == "Delete":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.delete_env_variables(
                    repository_name=repository_name,
                    environment_name=environment,
                    variableKey=variable_key_env,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Variable" and scope == "Repository" and mode == "Create New":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_repo_variables(
                    repository_name=repository_name,
                    variableKey=new_variable_key,
                    variableValue=variable_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
            if kind == "Variable" and scope == "Environment" and mode == "Create New":
                github_manager_client = GitHubManagerClient(
                    function_base_url, function_code
                )
                set_progress("GitHub Manager Client created and creating repository.")
                update_secret = github_manager_client.post_env_variables(
                    repository_name=repository_name,
                    environment_name=environment,
                    variableKey=new_variable_key,
                    variableValue=variable_value,
                )
                return (
                    "SUCCESS",
                    f"Deployment creation triggered for https://github.com/dvag/{repository_name}",
                    "",
                )
        else:
            return "FAILURE", "", "Connection info couldn't be received"
    except ConnectionInfo.DoesNotExist:
        return "FAILURE", "", "Connection info couldn't be received"
