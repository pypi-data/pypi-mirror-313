import os
import json
import requests
import aiohttp
import asyncio


CACHE_DIR = ".gitlab_cache/"
APPROVAL_SETTINGS_CACHE_FILE = os.path.join(CACHE_DIR, "approval_settings.json")
MERGE_REQUESTS_CACHE_FILE = os.path.join(CACHE_DIR, "merge_requests.json")
MR_NOTES_CACHE_FILE = os.path.join(CACHE_DIR, "mr_notes.json")
PROTECTED_BRANCHES_CACHE_FILE = os.path.join(CACHE_DIR, "protected_branches.json")
BRANCHES_CACHE_FILE = os.path.join(CACHE_DIR, "branches.json")
PUSH_RULES_CACHE_FILE = os.path.join(CACHE_DIR, "push_rules.json")

# Ensure cache directory exists once
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def fetch_gitlab_data(project_id, token):
    """Fetch all project data from GitLab API, with caching in GitLab CI."""
    project_data_cache_file = os.path.join(CACHE_DIR, f"project_data_{project_id}.json")

    # Check if cached project data exists
    if os.path.exists(project_data_cache_file):
        print(f"Using cached project data from {project_data_cache_file}")
        with open(project_data_cache_file, "r") as f:
            return json.load(f)

    # If not cached, fetch from the general project API
    url = f"https://gitlab.com/api/v4/projects/{project_id}"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch project data: {e}")
        return None

    project_data = response.json()

    # Cache the project data
    with open(project_data_cache_file, "w") as f:
        json.dump(project_data, f)

    return project_data


def fetch_approval_settings(project_id, token):
    """Fetch approval settings from GitLab API, with caching."""
    if os.path.exists(APPROVAL_SETTINGS_CACHE_FILE):
        print(f"Using cached approval settings from {APPROVAL_SETTINGS_CACHE_FILE}")
        with open(APPROVAL_SETTINGS_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://gitlab.com/api/v4/projects/{project_id}/approval_settings"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch approval settings: {e}")
        return None

    approval_settings = response.json()

    # Cache the data
    with open(APPROVAL_SETTINGS_CACHE_FILE, "w") as f:
        json.dump(approval_settings, f)

    return approval_settings


def fetch_merge_requests(project_id, token):
    """Fetch merge requests from GitLab API, with caching in GitLab CI."""
    if os.path.exists(MERGE_REQUESTS_CACHE_FILE):
        print(f"Using cached merge requests from {MERGE_REQUESTS_CACHE_FILE}")
        with open(MERGE_REQUESTS_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch merge requests: {e}")
        return None

    data = response.json()

    # Cache the data
    with open(MERGE_REQUESTS_CACHE_FILE, "w") as f:
        json.dump(data, f)

    return data


def fetch_merge_request_notes(project_id, mr_iid, token):
    """Fetch notes for a specific merge request, with caching in GitLab CI."""
    cache_file = os.path.join(CACHE_DIR, f"mr_notes_{mr_iid}.json")
    if os.path.exists(cache_file):
        print(f"Using cached merge request notes for MR {mr_iid} from {cache_file}")
        with open(cache_file, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = (
        f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    )
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch merge request notes: {e}")
        return None

    data = response.json()

    # Cache the data
    with open(cache_file, "w") as f:
        json.dump(data, f)

    return data


# Define the URL to fetch the CODEOWNERS file
def fetch_codeowners_file(project_id, token, branch="main"):
    """Fetch the CODEOWNERS file from GitLab API, with caching in GitLab CI."""
    codeowners_cache_file = os.path.join(CACHE_DIR, "codeowners.json")

    if os.path.exists(codeowners_cache_file):
        print(f"Using cached CODEOWNERS data from {codeowners_cache_file}")
        with open(codeowners_cache_file, "r") as f:
            return json.load(f)

    possible_paths = ["/CODEOWNERS", "/.gitlab/CODEOWNERS", "/docs/CODEOWNERS"]
    headers = {"PRIVATE-TOKEN": token}

    # Try fetching from 'main' branch first
    for path in possible_paths:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files{path}/raw?ref={branch}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            codeowners_data = response.text
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(codeowners_cache_file, "w") as f:
                json.dump(codeowners_data, f)
            return codeowners_data

    # If CODEOWNERS file is not found on 'main', try fetching from 'master'
    print(f"CODEOWNERS file not found in branch '{branch}'. Trying 'master' branch.")
    for path in possible_paths:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files{path}/raw?ref=master"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            codeowners_data = response.text
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(codeowners_cache_file, "w") as f:
                json.dump(codeowners_data, f)
            return codeowners_data

    print("CODEOWNERS file not found in 'main' or 'master' branches.")
    return None


def fetch_protected_branches(project_id, token):
    """Fetch the protected branches and check if code owner approval is required."""
    # Check if cached protected branches data exists
    if os.path.exists(PROTECTED_BRANCHES_CACHE_FILE):
        print(f"Using cached protected branches from {PROTECTED_BRANCHES_CACHE_FILE}")
        with open(PROTECTED_BRANCHES_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches"
    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    protected_branches = response.json()

    # Cache the data
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(PROTECTED_BRANCHES_CACHE_FILE, "w") as f:
        json.dump(protected_branches, f)

    return protected_branches


def fetch_branches(project_id, token):
    """Fetch branches from GitLab API, with caching in GitLab CI."""
    if os.path.exists(BRANCHES_CACHE_FILE):
        print(f"Using cached branches from {BRANCHES_CACHE_FILE}")
        with open(BRANCHES_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/branches"
    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    branches_data = response.json()

    # Cache the data
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(BRANCHES_CACHE_FILE, "w") as f:
        json.dump(branches_data, f)

    return branches_data


def fetch_jira_integration(project_id, token):
    """
    Fetch Jira integration data for a GitLab project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): The GitLab private token for authentication.

    Returns:
        dict: Jira integration data if available, otherwise None.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/services/jira"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()  # Return the Jira integration data as a JSON dictionary
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch Jira integration data: {e}")
        return None


def fetch_push_rules(project_id, token):
    """
    Fetch the push rules for the project from GitLab API, with caching.
    """
    # Check if cached push rules data exists
    if os.path.exists(PUSH_RULES_CACHE_FILE):
        print(f"Using cached push rules from {PUSH_RULES_CACHE_FILE}")
        with open(PUSH_RULES_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://gitlab.com/api/v4/projects/{project_id}/push_rule"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch push rules: {e}")
        return None

    push_rules = response.json()

    # Cache the data
    with open(PUSH_RULES_CACHE_FILE, "w") as f:
        json.dump(push_rules, f)

    return push_rules


def fetch_audit_events(project_id, token):
    """
    Fetch audit events from GitLab for a given project.
    Returns the JSON response containing the audit events.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/audit_events"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching audit events: {e}")
        return None


def fetch_security_md_file(project_id, token, branch="main"):
    """
    Fetch the SECURITY.md file from a GitLab project repository.

    Args:
        project_id (int): The ID of the project in GitLab.
        token (str): The GitLab personal access token.
        branch (str): The branch to fetch the SECURITY.md from (default: 'main').

    Returns:
        str: Content of the SECURITY.md file or an appropriate message if it does not exist.
    """
    headers = {"PRIVATE-TOKEN": token}

    # URL to fetch the raw content of the SECURITY.md file
    file_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/SECURITY.md/raw?ref={branch}"

    try:
        response = requests.get(file_url, headers=headers)

        if response.status_code == 200:
            return response.text  # Return the raw content of the SECURITY.md file
        elif response.status_code == 404:
            return "SECURITY.md file not found."
        else:
            return f"Error: Received unexpected status code {response.status_code}."

    except requests.RequestException as e:
        return f"An error occurred: {e}"


def fetch_forks_data(project_id, token):
    """
    Fetch forks data for a project using the GitLab API.
    """
    headers = {"PRIVATE-TOKEN": token}
    base_url = f"https://gitlab.com/api/v4/projects/{project_id}/forks"

    # Make a request to the GitLab API to get the list of forks
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        forks_data = response.json()
        return forks_data
    else:
        print(f"Failed to retrieve forks. Status code: {response.status_code}")
        return None


def fetch_project_events(project_id, token):
    """
    Fetch the events related to a specific project from GitLab API.

    Args:
    token (str): GitLab API token.
    project_id (int): GitLab Project ID.

    Returns:
    list: A list of project events.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/events"
    headers = {"PRIVATE-TOKEN": token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Error 401: Unauthorized. Please check the GitLab token and permissions.")
    else:
        print(f"Failed to fetch project events, status code: {response.status_code}")

    return []


def fetch_project_members(project_id, token):
    """
    Fetch the members of a project from GitLab API.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/members"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()  # Return the list of members
    except requests.exceptions.RequestException as e:
        print(f"Error fetching project members: {e}")
        return None


def fetch_is_self_managed(token, gitlab_url="https://gitlab.com"):
    """
    Check if the GitLab instance is self-managed by querying the instance information.
    """
    url = f"{gitlab_url}/api/v4/version"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        instance_info = response.json()
        if instance_info.get("instance_administration_project"):
            return True
        else:
            return False

    except requests.RequestException as e:
        print(f"Error checking if self-managed: {e}")
        return False


def fetch_check_ip_restrictions(group_id, token, gitlab_url="https://gitlab.com"):
    """
    Check if Git access is limited based on allowed IP addresses for a self-managed instance.
    """
    url = f"{gitlab_url}/api/v4/groups/{group_id}/allowed_ip_ranges"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print("Allowed IP ranges endpoint not found. Skipping this check.")
            return None  # Or a default value indicating the check is not applicable
        response.raise_for_status()

        ip_ranges = response.json()

        if ip_ranges:
            print(
                f"Compliant: IP access is restricted to the following IP ranges: {ip_ranges}"
            )
            compliance_score = 5  # Full compliance
        else:
            print("Non-compliant: No IP restrictions found.")
            compliance_score = 0  # Non-compliance if no restrictions are set

        return compliance_score

    except requests.RequestException as e:
        print(f"Failed to retrieve IP restriction data: {e}")
        return None  # Adjust as necessary


def fetch_installed_applications(project_id, token):
    """
    Fetch installed applications (project services/integrations) for a given project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        list: Installed applications.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/services"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        services = response.json()

        installed_apps = []
        for service in services:
            if service.get("active", False):
                installed_apps.append(service["title"])

        return installed_apps

    except requests.RequestException as e:
        print(f"Error fetching installed applications: {e}")
        return []


def fetch_project_webhooks(project_id, token):
    """Fetch all webhooks for a specific project."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/hooks"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching project webhooks: {e}")
        return None


def fetch_pipeline_configuration(project_id, token):
    """
    Fetch the pipeline configuration of a GitLab project.

    Args:
        project_id (str): The ID of the GitLab project.
        token (str): The GitLab private token for authentication.

    Returns:
        dict: The pipeline configuration details.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/pipeline"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching pipeline configuration: {e}")
        return None


def fetch_gitlab_config(project_id, token, branch="main"):
    """
    Fetch the .gitlab-ci.yml file from a GitLab project repository.

    Args:
        project_id (int): The ID of the project in GitLab.
        token (str): The GitLab personal access token.
        branch (str): The branch to fetch the .gitlab-ci.yml from (default: 'main').

    Returns:
        str: Content of the .gitlab-ci.yml file or an appropriate message if it does not exist.
    """
    headers = {"PRIVATE-TOKEN": token}

    # URL to fetch the raw content of the .gitlab-ci.yml file
    file_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/.gitlab-ci.yml/raw?ref={branch}"

    try:
        response = requests.get(file_url, headers=headers)

        if response.status_code == 200:
            return response.text  # Return the raw content of the SECURITY.md file
        elif response.status_code == 404:
            return ".gitlab-ci.yml file not found."
        else:
            return f"Error: Received unexpected status code {response.status_code}."

    except requests.RequestException as e:
        return f"An error occurred: {e}"


def fetch_pipelines(project_id, token):
    """
    Fetch the pipelines of a project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): The GitLab private token for authentication.

    Returns:
        list: List of pipelines for the project.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/pipelines"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch pipelines: {e}")
        return []


def fetch_pipeline_jobs(project_id, pipeline_id, token):
    """
    Fetch jobs in a given pipeline.

    Args:
        project_id (int): The GitLab project ID.
        pipeline_id (int): The pipeline ID.
        token (str): The GitLab private token for authentication.

    Returns:
        list: List of jobs in the pipeline.
    """
    url = (
        f"https://gitlab.com/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
    )
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch pipeline jobs: {e}")
        return []


def fetch_latest_pipeline_jobs(project_id, token, num_jobs=10):
    """
    Fetch the last 'num_jobs' pipeline jobs for a given GitLab project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): The GitLab private token for authentication.
        num_jobs (int): The number of pipeline jobs to fetch (default 10).

    Returns:
        list: List of the latest pipeline jobs.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs"
    headers = {"PRIVATE-TOKEN": token}
    params = {"per_page": num_jobs}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch pipeline jobs: {e}")
        return []


def fetch_repository_tree(project_id, token, ref="main"):
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/tree"
    headers = {"PRIVATE-TOKEN": token}
    params = {"ref": ref, "recursive": "true", "per_page": 100}

    all_items = []
    page = 1

    while True:
        params["page"] = page
        try:
            response = requests.get(url, headers=headers, params=params, timeout=120)
            response.raise_for_status()
            items = response.json()
            if not items:
                break
            all_items.extend(items)

            next_page = response.headers.get("X-Next-Page")
            if next_page:
                page = int(next_page)
            else:
                break
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    return all_items


def fetch_job_logs(project_id, token, job_id):
    """
    Fetch logs for a specific job in a GitLab project.

    Args:
        project_id (int): The GitLab project ID.
        job_id (int): The job ID to fetch logs for.
        token (str): GitLab personal access token.

    Returns:
        str: The job log as a string.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/{job_id}/trace"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text  # The job log as a string
    except requests.RequestException as e:
        print(f"Failed to fetch job logs for job ID {job_id}: {e}")
        return None


def fetch_environments(project_id, token):
    """
    Fetch the environments for a specific project in GitLab.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        list: List of environments in the project.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/environments"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # The environments data as a list of dictionaries
    except requests.RequestException as e:
        print(f"Failed to fetch environments for project ID {project_id}: {e}")
        return None


def fetch_gitlab_runners(project_id, token):
    """
    Fetch GitLab Runner data for the given project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        list: List of runners associated with the project.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/runners"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        runners = response.json()
        return runners
    except requests.RequestException as e:
        print(f"Failed to fetch runners: {e}")
        return []


def fetch_prometheus_metrics(runners):
    """
    Fetch Prometheus metrics for each GitLab runner in the list.

    Args:
        runners (list): List of runner dictionaries retrieved from the GitLab API.

    Returns:
        dict: Dictionary of runner IDs with their respective Prometheus metrics or error messages.
    """
    prometheus_metrics = {}

    for runner in runners:
        runner_id = runner.get("id")
        description = runner.get("description", "Unknown")

        # Only try to fetch metrics for online runners
        if runner.get("online", False):
            # Construct a mock Prometheus metrics URL (this may depend on your infrastructure)
            prometheus_url = f"http://{runner['description']}:9252/metrics"

            try:
                response = requests.get(prometheus_url, timeout=10)
                response.raise_for_status()
                prometheus_metrics[runner_id] = response.text
                print(
                    f"Fetched Prometheus metrics for runner {runner_id} ({description})"
                )
            except requests.RequestException as e:
                prometheus_metrics[runner_id] = f"Error fetching metrics: {e}"
                print(
                    f"Error fetching Prometheus metrics for runner {runner_id} ({description}): {e}"
                )
        else:
            prometheus_metrics[runner_id] = (
                "Runner is offline or metrics not available."
            )
            print(
                f"Runner {runner_id} ({description}) is offline or does not have Prometheus metrics enabled."
            )

    return prometheus_metrics


def fetch_gitlab_commit_history(project_id, token, file_path=".gitlab-ci.yml"):
    """
    Fetch the commit history for a specific file in a GitLab project.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): Your GitLab personal access token.
        file_path (str): The path to the file (e.g., '.gitlab-ci.yml').

    Returns:
        list: A list of commits containing information about changes made to the file, or None if an error occurs.
    """
    headers = {"Private-Token": token}

    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"

    params = {
        "path": file_path,
        "per_page": 100,  # Adjust this as necessary to fetch more or fewer commits
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch commit history: {response.status_code} {response.text}")
        return None


def fetch_release_artifacts(project_id, token):
    """
    Fetch all artifacts from all releases of a GitLab project.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.

    Returns:
        list: List of release artifacts.
    """
    headers = {"PRIVATE-TOKEN": token}
    url = f"https://gitlab.com/api/v4/projects/{project_id}/releases"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        releases = response.json()

        artifacts = []
        for release in releases:
            tag_name = release.get("tag_name")
            if tag_name:
                # Fetch artifacts for each release
                artifacts_url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/artifacts/{tag_name}/download"
                artifact_response = requests.get(artifacts_url, headers=headers)

                if artifact_response.status_code == 200:
                    artifacts.append(
                        {
                            "tag_name": tag_name,
                            "artifact": artifact_response.content,
                            "signed": "signature.asc"
                            in artifact_response.text,  # Check if a signature file exists
                        }
                    )
                else:
                    print(f"⚠️ Could not fetch artifacts for tag '{tag_name}'")

        return artifacts

    except requests.RequestException as e:
        print(f"Error fetching release artifacts: {e}")
        return []


def fetch_dependency_files(project_id, token, branch="main"):
    """
    Fetch the dependency files (Gemfile.lock, package-lock.json, yarn.lock, go.sum) from the GitLab repository.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.
        branch (str): Branch of the project to fetch the files from.

    Returns:
        dict: A dictionary containing the content of dependency files.
    """
    dependency_files = ["Gemfile.lock", "package-lock.json", "yarn.lock", "go.sum"]
    headers = {"PRIVATE-TOKEN": token}
    file_contents = {}

    for file_name in dependency_files:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/{file_name}/raw?ref={branch}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_contents[file_name] = response.text
                print(f"✅ Successfully fetched {file_name}")
            else:
                print(
                    f"⚠️ Could not fetch {file_name}: {response.status_code} {response.text}"
                )
        except requests.RequestException as e:
            print(f"Error fetching {file_name}: {e}")

    return file_contents


def fetch_pipeline_artifacts(project_id, token, job_id):
    """
    Fetch the artifacts associated with a specific job in a pipeline.

    Args:
        project_id (str): The ID of the GitLab project.
        token (str): GitLab personal access token.
        job_id (str): The ID of the job for which to fetch artifacts.

    Returns:
        list: List of artifacts associated with the job or an empty list if none found.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/{job_id}/artifacts"
    headers = {"PRIVATE-TOKEN": token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content  # Return the actual artifact content (binary data)
    elif response.status_code == 404:
        print(f"No artifacts found for job ID {job_id}.")
        return None
    else:
        print(
            f"Error fetching artifacts for job ID {job_id}: {response.status_code} - {response.text}"
        )
        return None


def fetch_sbom_artifacts(project_id, token):
    """
    Fetch all SBOM artifacts from all releases of a GitLab project.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.

    Returns:
        list: List of SBOM artifacts with metadata indicating if they are signed.
    """
    headers = {"PRIVATE-TOKEN": token}
    url = f"https://gitlab.com/api/v4/projects/{project_id}/releases"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        releases = response.json()

        sbom_artifacts = []
        for release in releases:
            tag_name = release.get("tag_name")
            if tag_name:
                # Fetch artifacts for each release
                artifacts_url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/artifacts/{tag_name}/download"
                artifact_response = requests.get(artifacts_url, headers=headers)

                if artifact_response.status_code == 200:
                    # Check for SBOM artifact files (e.g., "*.sbom.json")
                    if "sbom.json" in artifact_response.headers.get(
                        "Content-Disposition", ""
                    ):
                        sbom_artifacts.append(
                            {
                                "tag_name": tag_name,
                                "file_name": f"{tag_name}.sbom.json",
                                "is_signed": "signature.asc" in artifact_response.text,
                            }
                        )
                else:
                    print(f"⚠️ Could not fetch SBOM artifacts for tag '{tag_name}'")

        return sbom_artifacts

    except requests.RequestException as e:
        print(f"Error fetching SBOM artifacts: {e}")
        return []


def fetch_npm_package_info(package_name):
    """Fetch package information from the npm registry."""
    url = f"https://registry.npmjs.org/{package_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching npm package info for {package_name}: {e}")
        return None


def fetch_pypi_package_info(package_name):
    """Fetch package information from the PyPI registry."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching PyPI package info for {package_name}: {e}")
        return None


def check_package_age(package_name, registry="npm"):
    """
    Check if a package is older than 60 days.

    Args:
        package_name (str): The name of the package.
        registry (str): The package registry to check ("npm" or "pypi").

    Returns:
        bool: True if the package is more than 60 days old, False otherwise.
    """
    if registry == "npm":
        package_info = fetch_npm_package_info(package_name)
        if not package_info or "time" not in package_info:
            return False
        latest_version = package_info["dist-tags"]["latest"]
        latest_version_date = package_info["time"][latest_version]
    elif registry == "pypi":
        package_info = fetch_pypi_package_info(package_name)
        if not package_info:
            return False
        latest_release = package_info["info"]["version"]
        latest_version_date = package_info["releases"][latest_release][0]["upload_time"]
    else:
        print(f"Registry '{registry}' not supported")
        return False

    # Parse the date and compare with the current date
    latest_date = datetime.strptime(latest_version_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    days_old = (datetime.now() - latest_date).days

    return days_old > 60


def fetch_group_push_rules(group_id, token):
    """
    Fetch push rules for a GitLab group (which might enforce dependency policies).

    Args:
        group_id (int): The ID of the GitLab group.
        token (str): GitLab personal access token.

    Returns:
        dict: Push rules settings for the group.
    """
    url = f"https://gitlab.com/api/v4/groups/{group_id}/push_rule"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch push rules for group ID {group_id}: {e}")
        return None


def fetch_security_scanning(project_id, token):
    """
    Fetch security scanning configuration for the project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        dict: Security scanning configuration data if available.
    """
    url = (
        f"https://gitlab.com/api/v4/projects/{project_id}/dependency_scanning/settings"
    )
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch security scanning configuration: {e}")
        return None


def fetch_license_scanning(project_id, token):
    """
    Fetch license scanning configuration for the project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        dict: License scanning configuration data if available.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/license_scanning/settings"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch license scanning configuration: {e}")
        return None


def fetch_group_settings(group_id, token):
    """
    Fetch the group settings from GitLab API.

    Args:
        group_id (int): The GitLab group ID.
        token (str): GitLab private token for authentication.

    Returns:
        dict: A dictionary containing group settings, or None if fetch fails.
    """
    url = f"https://gitlab.com/api/v4/groups/{group_id}"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch group settings: {e}")
        return None
