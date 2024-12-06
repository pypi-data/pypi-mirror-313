import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging
import datetime
import os


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_gitlab_data(project_id, token):
    """Fetch all project data from GitLab API without caching."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch project data: {e}")
        return None

    return response.json()


def fetch_approval_settings(project_id, token):
    """Fetch approval settings from GitLab API without caching."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/approval_settings"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch approval settings: {e}")
        return None

    return response.json()


def fetch_merge_requests(project_id, token):
    """Fetch merge requests from GitLab API without caching."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch merge requests: {e}")
        return None

    return response.json()


def fetch_merge_request_notes(project_id, mr_iid, token):
    """Fetch notes for a specific merge request from GitLab API without caching."""
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

    return response.json()


# Define the URL to fetch the CODEOWNERS file
def fetch_codeowners_file(project_id, token, branch="main"):
    """Fetch the CODEOWNERS file from GitLab API without caching."""
    possible_paths = ["/CODEOWNERS", "/.gitlab/CODEOWNERS", "/docs/CODEOWNERS"]
    headers = {"PRIVATE-TOKEN": token}

    # Try fetching from 'main' branch first
    for path in possible_paths:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files{path}/raw?ref={branch}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text

    # If CODEOWNERS file is not found on 'main', try fetching from 'master'
    print(f"CODEOWNERS file not found in branch '{branch}'. Trying 'master' branch.")
    for path in possible_paths:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files{path}/raw?ref=master"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text

    print("CODEOWNERS file not found in 'main' or 'master' branches.")
    return None


def fetch_protected_branches(project_id, token):
    """Fetch the protected branches and check if code owner approval is required."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches"
    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def fetch_branches(project_id, token, max_pages=5):
    """Fetch branches from GitLab API with parallel pagination support and retry logic."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/branches"
    headers = {"PRIVATE-TOKEN": token}

    # First request to get the total number of pages
    response = requests.get(url, headers=headers, params={"per_page": 100})
    response.raise_for_status()  # This raises an exception for non-2xx responses
    total_pages = int(response.headers.get("X-Total-Pages", 1))

    # Limit the number of pages
    total_pages = min(total_pages, max_pages)

    branches = []

    def fetch_page(page, retries=3):
        """Fetch a specific page of branches with retry logic."""
        for attempt in range(retries):
            try:
                response = requests.get(
                    url, headers=headers, params={"page": page, "per_page": 100}
                )
                response.raise_for_status()  # Raise an exception for 4xx/5xx errors
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 503 and attempt < retries - 1:
                    print(
                        f"503 Service Unavailable. Retrying page {page}... (Attempt {attempt + 1}/{retries})"
                    )
                    time.sleep(2**attempt)  # Exponential backoff: 1s, 2s, 4s, etc.
                else:
                    print(f"Failed to fetch page {page}: {e}")
                    return []

    # Use ThreadPoolExecutor to fetch pages in parallel
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(fetch_page, page): page
            for page in range(1, total_pages + 1)
        }

        for future in as_completed(futures):
            branches.extend(future.result())

    return branches


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
    """Fetch the push rules for the project from GitLab API."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/push_rule"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch push rules: {e}")
        return None

    return response.json()


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


def fetch_project_events(project_id, token, per_page=100, max_pages=5):
    """
    Fetch the events related to a specific project from GitLab API, with pagination support and limit.

    Args:
    token (str): GitLab API token.
    project_id (int): GitLab Project ID.
    per_page (int): Number of events to fetch per page (GitLab default is 20, max is 100).
    max_pages (int): Maximum number of pages to fetch (default is 5).

    Returns:
    list: A list of all project events.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/events"
    headers = {"PRIVATE-TOKEN": token}
    params = {"per_page": per_page, "page": 1}
    all_events = []

    while params["page"] <= max_pages:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            logging.error(
                f"Error fetching project events on page {params['page']}: {e}"
            )
            break

        events = response.json()
        if not events:
            logging.info(
                f"No more events found on page {params['page']}. Ending pagination."
            )
            break  # No more events, exit the loop

        all_events.extend(events)

        params["page"] += 1  # Move to the next page

    logging.info(f"Completed fetching events. Total events fetched: {len(all_events)}")
    return all_events


def fetch_project_members(project_id, token):
    """
    Fetch all members of a GitLab project with pagination.
    
    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        list: List of all project members.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/members/all"
    headers = {"PRIVATE-TOKEN": token}
    members = []
    page = 1
    per_page = 100

    try:
        while True:
            # Fetch each page of members
            response = requests.get(
                url,
                headers=headers,
                params={"page": page, "per_page": per_page},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            
            # If no more data, break out of the loop
            if not data:
                break

            members.extend(data)  # Add members from the current page
            page += 1  # Move to the next page

        return members  # Complete list of members

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
    Fetch IP restrictions data for a self-managed instance.
    """
    url = f"{gitlab_url}/api/v4/groups/{group_id}/allowed_ip_ranges"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print("Allowed IP ranges endpoint not found. Skipping this check.")
            return None  # Endpoint not applicable for this instance
        response.raise_for_status()
        ip_ranges = response.json()

        return ip_ranges  # Return the IP ranges data

    except requests.RequestException as e:
        print(f"Failed to retrieve IP restriction data: {e}")
        return None  # Handle error appropriately


def fetch_installed_applications(project_id, token):
    """
    Fetch installed applications (project services/integrations) for a given project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        list: Installed applications with their metadata.
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
                installed_apps.append({
                    "name": service.get("title", "Unknown Title"),
                    "active": service.get("active", False)
                })

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
    Fetch the latest SBOM artifact from the most recent Gemnasium dependency scanning job.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.

    Returns:
        dict or None: Information about the SBOM artifact, if found, otherwise None.
    """
    headers = {"PRIVATE-TOKEN": token}
    jobs_url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs"

    logging.info(f"Starting fetch_sbom_artifacts for project ID {project_id}.")

    try:
        # Fetch the list of jobs
        logging.info(f"Fetching jobs from {jobs_url}")
        response = requests.get(jobs_url, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        logging.debug(f"Jobs fetched: {jobs}")

        # Filter for Gemnasium dependency scanning jobs
        gemnasium_jobs = [
            job for job in jobs if job.get("name") == "gemnasium-dependency_scanning"
        ]
        logging.info(f"Found {len(gemnasium_jobs)} Gemnasium dependency scanning jobs.")

        if not gemnasium_jobs:
            logging.warning("No Gemnasium dependency scanning jobs found.")
            return None

        # Get the latest job
        gemnasium_jobs.sort(key=lambda job: job["created_at"], reverse=True)
        latest_job = gemnasium_jobs[0]
        job_id = latest_job["id"]
        logging.info(f"Latest Gemnasium job ID: {job_id}")

        # Fetch artifacts for the latest job
        artifacts_url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/{job_id}/artifacts"
        logging.info(f"Fetching artifacts from {artifacts_url}")
        artifact_response = requests.get(artifacts_url, headers=headers)

        if artifact_response.status_code == 200:
            artifacts = artifact_response.json()
            logging.debug(f"Artifacts fetched: {artifacts}")

            # Search for an SBOM artifact
            for artifact in artifacts:
                if (
                    artifact.get("filename", "").endswith(".sbom.json")
                    or "sbom" in artifact.get("filename", "").lower()
                ):
                    sbom_artifact = {
                        "job_id": job_id,
                        "file_name": artifact["filename"],
                        "size": artifact.get("size"),
                        "created_at": latest_job["created_at"],
                        "web_url": latest_job["web_url"],
                    }
                    logging.info(f"SBOM Artifact found: {sbom_artifact}")
                    return sbom_artifact
            logging.warning("No SBOM artifact found in the latest Gemnasium job.")
        else:
            logging.error(
                f"Could not fetch artifacts for job ID '{job_id}'. Status: {artifact_response.status_code}"
            )
    except requests.RequestException as e:
        logging.error(f"Error fetching SBOM artifacts: {e}")

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


def fetch_approvals(project_id, token):
    """
    Fetch the project-level MR approvals from the GitLab API.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab private token for authentication.

    Returns:
        dict: A dictionary containing the approval settings, or None if the fetch fails.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/approvals"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch project approvals: {e}")
        return None


def fetch_group_members(group_id, token, per_page=100):
    """
    Fetch all members of a group from GitLab API, handling pagination.
    """
    url = f"https://gitlab.com/api/v4/groups/{group_id}/members/all"
    headers = {"PRIVATE-TOKEN": token}
    members = []
    page = 1

    try:
        while True:
            params = {"per_page": per_page, "page": page}
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            page_members = response.json()

            if not page_members:  # No more members to fetch
                break

            members.extend(page_members)
            page += 1  # Move to the next page

        return members  # Return the list of all members

    except requests.exceptions.RequestException as e:
        print(f"Error fetching group members: {e}")
        return None


def fetch_ci_files(project_id, token, ref="master"):
    """
    Fetch CI files from the .gitlab/ci directory in the repository.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.
        ref (str): The branch or tag to fetch the repository tree for.

    Returns:
        list: A list of CI file paths found under .gitlab/ci.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/tree"
    headers = {"PRIVATE-TOKEN": token}
    params = {
        "ref": ref,
        "recursive": "true",
        "per_page": 100,
        "path": ".gitlab/ci",  # Restrict search to .gitlab/ci directory
    }

    all_ci_files = []
    page = 1

    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        items = response.json()
        if not items:
            break
        all_ci_files.extend(items)

        next_page = response.headers.get("X-Next-Page")
        if next_page:
            page = int(next_page)
        else:
            break

    # Filter to include only file paths in the CI directory
    ci_files = [item["path"] for item in all_ci_files if item["type"] == "blob"]

    return ci_files


def fetch_gitlab_ci_variables(project_id, token):
    """
    Fetch the CI/CD variables (including secrets) from the GitLab project.

    Args:
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        list: A list of variables (potential secrets) in the project.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/variables"
    headers = {"PRIVATE-TOKEN": token}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()  # Return the variables as a list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching variables: {e}")
        return []


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


def fetch_deployment_files_from_gitlab(project_id, private_token):
    """
    Fetch specific deployment configuration files from a GitLab repository using the GitLab API.

    Args:
        project_id (str): The ID of the GitLab project.
        private_token (str): The GitLab personal access token.

    Returns:
        list: A list of deployment configuration files found in the repository.
    """
    api_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files"
    headers = {"PRIVATE-TOKEN": private_token}

    # List of common deployment files to search for
    deployment_files = [
        "docker-compose.yml",
        "kubernetes.yml",
        "deployment.yml",
        ".gitlab-ci.yml",
        "helm",
        "terraform",
    ]

    found_files = []

    # Iterate through each file and check if it exists in the repository
    for deployment_file in deployment_files:
        encoded_file_path = requests.utils.quote(deployment_file, safe="")
        check_file_url = f"{api_url}/{encoded_file_path}/raw?ref=master"  # Checking in the master branch by default
        try:
            response = requests.head(check_file_url, headers=headers)
            if response.status_code == 200:
                found_files.append(deployment_file)
            elif response.status_code == 404:
                print(f"{deployment_file} not found in the repository.")
            else:
                print(f"Error fetching {deployment_file}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Exception occurred while fetching {deployment_file}: {e}")

    return found_files


def fetch_branch_by_name(project_id, token, branch_name="main"):
    """Fetch a specific branch by name from the GitLab API."""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/branches/{branch_name}"
    headers = {"PRIVATE-TOKEN": token}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for 4xx or 5xx responses
        return response.json()  # Return the branch details as JSON
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Branch '{branch_name}' not found in project {project_id}.")
        else:
            print(f"Error fetching branch '{branch_name}': {err}")
        return None
    

def fetch_job_logs_dict(pipeline_jobs, project_id, token):
    """
    Fetch logs for each job in the pipeline_jobs list and store them in a dictionary.

    Args:
        pipeline_jobs (list): List of pipeline job dictionaries.
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        dict: Dictionary where keys are job IDs and values are job log content (or None if not available).
    """
    job_logs = {}
    for job in pipeline_jobs:
        job_id = job.get("id")
        if job_id:
            job_logs[job_id] = fetch_job_logs(project_id, token, job_id)
    return job_logs


def fetch_protected_environments(project_id, private_token):
    """
    Fetch the list of protected environments for a specific GitLab project.

    Args:
        project_id (int): The ID of the GitLab project.
        private_token (str): The GitLab personal access token.

    Returns:
        list: A list of protected environments, each containing allowed deploy access information.
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_environments"
    headers = {
        "PRIVATE-TOKEN": private_token
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # List of protected environments
    else:
        print(f"Error fetching protected environments: {response.status_code} - {response.text}")
        return None
    

def fetch_sbom_artifacts_from_jobs(project_id, token):
    """
    Fetch the latest SBOM artifact from the most recent Gemnasium dependency scanning job,
    following the steps used in curl commands.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.

    Returns:
        dict or None: Information about the SBOM artifact, if found, otherwise None.
    """
    headers = {"PRIVATE-TOKEN": token}
    jobs_url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs"

    logging.info(f"Starting fetch_sbom_artifacts_from_curl_steps for project ID {project_id}.")

    try:
        # Step 1: Get all jobs for the project
        logging.info(f"Fetching jobs from {jobs_url}")
        response = requests.get(jobs_url, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        logging.debug(f"Jobs fetched: {jobs}")

        # Step 2: Filter for "gemnasium-dependency_scanning" jobs
        gemnasium_jobs = [
            job for job in jobs if job.get("name") == "gemnasium-dependency_scanning"
        ]
        logging.info(f"Found {len(gemnasium_jobs)} Gemnasium dependency scanning jobs.")

        if not gemnasium_jobs:
            logging.warning("No Gemnasium dependency scanning jobs found.")
            return None

        # Step 3: Sort jobs to get the latest one
        gemnasium_jobs.sort(key=lambda job: job["created_at"], reverse=True)
        latest_job = gemnasium_jobs[0]
        job_id = latest_job["id"]
        logging.info(f"Latest Gemnasium job ID: {job_id}")

        # Step 4: Check the existence of artifacts for the latest job
        artifacts_url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/{job_id}/artifacts"
        logging.info(f"Checking artifacts for job ID {job_id} at {artifacts_url}")
        artifact_response = requests.head(artifacts_url, headers=headers)

        if artifact_response.status_code == 200:
            logging.info(f"Artifacts exist for job ID {job_id}. Checking for SBOM file.")

            # Step 5: Fetch and analyze specific SBOM file
            sbom_file_url = f"{artifacts_url}/gl-sbom.cdx.json.gz"
            sbom_check_response = requests.head(sbom_file_url, headers=headers)

            if sbom_check_response.status_code == 200:
                logging.info(f"SBOM artifact found: gl-sbom.cdx.json.gz for job ID {job_id}")
                return {
                    "job_id": job_id,
                    "file_name": "gl-sbom.cdx.json.gz",
                    "created_at": latest_job["created_at"],
                    "web_url": latest_job["web_url"],
                }
            else:
                logging.warning(f"SBOM artifact gl-sbom.cdx.json.gz not found for job ID {job_id}.")
        else:
            logging.warning(f"No artifacts found for job ID {job_id}. Status: {artifact_response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error fetching SBOM artifacts: {e}")

    return None