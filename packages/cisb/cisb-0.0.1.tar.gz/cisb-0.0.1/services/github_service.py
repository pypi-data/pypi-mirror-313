import os
import json
import requests

CACHE_DIR = ".github_cache/"
PULL_REQUESTS_CACHE_FILE = os.path.join(CACHE_DIR, "pull_requests.json")
PROTECTED_BRANCHES_CACHE_FILE = os.path.join(CACHE_DIR, "protected_branches.json")
BRANCHES_CACHE_FILE = os.path.join(CACHE_DIR, "branches.json")
SECURITY_MD_CACHE_FILE = os.path.join(CACHE_DIR, "security_md.json")

# Ensure cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def fetch_github_data(repo_name, token):
    """Fetch repository data from GitHub API, with caching."""
    repo_data_cache_file = os.path.join(CACHE_DIR, f"repo_data_{repo_name}.json")

    # Check if cached repo data exists
    if os.path.exists(repo_data_cache_file):
        print(f"Using cached repo data from {repo_data_cache_file}")
        with open(repo_data_cache_file, "r") as f:
            return json.load(f)

    # If not cached, fetch from GitHub API
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repository data: {e}")
        return None

    repo_data = response.json()

    # Cache the repo data
    with open(repo_data_cache_file, "w") as f:
        json.dump(repo_data, f)

    return repo_data


def fetch_pull_requests(repo_name, token):
    """Fetch pull requests from GitHub API, with caching."""
    if os.path.exists(PULL_REQUESTS_CACHE_FILE):
        print(f"Using cached pull requests from {PULL_REQUESTS_CACHE_FILE}")
        with open(PULL_REQUESTS_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://api.github.com/repos/{repo_name}/pulls"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch pull requests: {e}")
        return None

    pull_requests = response.json()

    # Cache the data
    with open(PULL_REQUESTS_CACHE_FILE, "w") as f:
        json.dump(pull_requests, f)

    return pull_requests


def fetch_pull_request_comments(repo_name, pr_number, token):
    """Fetch comments for a specific pull request from GitHub API, with caching."""
    cache_file = os.path.join(CACHE_DIR, f"pr_comments_{pr_number}.json")

    if os.path.exists(cache_file):
        print(
            f"Using cached pull request comments for PR {pr_number} from {cache_file}"
        )
        with open(cache_file, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch pull request comments: {e}")
        return None

    comments = response.json()

    # Cache the data
    with open(cache_file, "w") as f:
        json.dump(comments, f)

    return comments


def fetch_protected_branches(repo_name, token):
    """Fetch the protected branches and check if branch protection rules are applied."""
    if os.path.exists(PROTECTED_BRANCHES_CACHE_FILE):
        print(f"Using cached protected branches from {PROTECTED_BRANCHES_CACHE_FILE}")
        with open(PROTECTED_BRANCHES_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://api.github.com/repos/{repo_name}/branches"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch protected branches: {e}")
        return None

    branches = response.json()

    # Cache the data
    with open(PROTECTED_BRANCHES_CACHE_FILE, "w") as f:
        json.dump(branches, f)

    return branches


def fetch_branches(repo_name, token):
    """Fetch branches from GitHub API, with caching."""
    if os.path.exists(BRANCHES_CACHE_FILE):
        print(f"Using cached branches from {BRANCHES_CACHE_FILE}")
        with open(BRANCHES_CACHE_FILE, "r") as f:
            return json.load(f)

    # If not cached, fetch from API
    url = f"https://api.github.com/repos/{repo_name}/branches"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch branches: {e}")
        return None

    branches_data = response.json()

    # Cache the data
    with open(BRANCHES_CACHE_FILE, "w") as f:
        json.dump(branches_data, f)

    return branches_data


def fetch_security_md_file(repo_name, token, branch="main"):
    """Fetch the SECURITY.md file from a GitHub project repository."""
    cache_file = SECURITY_MD_CACHE_FILE

    if os.path.exists(cache_file):
        print(f"Using cached SECURITY.md data from {cache_file}")
        with open(cache_file, "r") as f:
            return json.load(f)

    # URL to fetch the raw content of the SECURITY.md file
    url = f"https://api.github.com/repos/{repo_name}/contents/SECURITY.md?ref={branch}"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            file_content = response.json().get("content")
            return file_content  # Return the raw content of the SECURITY.md file (encoded in base64)
        elif response.status_code == 404:
            return "SECURITY.md file not found."
        else:
            return f"Error: Received unexpected status code {response.status_code}."

    except requests.RequestException as e:
        return f"An error occurred: {e}"
