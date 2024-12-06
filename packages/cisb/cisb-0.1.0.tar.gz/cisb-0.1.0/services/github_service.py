import requests


def fetch_github_data(repo_name, token):
    """Fetch repository data from GitHub API without caching."""
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repository data: {e}")
        return None

    return response.json()


def fetch_pull_requests(repo_name, token):
    """Fetch pull requests from GitHub API without caching."""
    url = f"https://api.github.com/repos/{repo_name}/pulls"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch pull requests: {e}")
        return None

    return response.json()


def fetch_pull_request_comments(repo_name, pr_number, token):
    """Fetch comments for a specific pull request from GitHub API without caching."""
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch pull request comments: {e}")
        return None

    return response.json()


def fetch_protected_branches(repo_name, token):
    """Fetch the protected branches from GitHub API without caching."""
    url = f"https://api.github.com/repos/{repo_name}/branches"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch protected branches: {e}")
        return None

    return response.json()


def fetch_branches(repo_name, token):
    """Fetch branches from GitHub API without caching."""
    url = f"https://api.github.com/repos/{repo_name}/branches"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch branches: {e}")
        return None

    return response.json()


def fetch_security_md_file(repo_name, token, branch="main"):
    """Fetch the SECURITY.md file from a GitHub project repository without caching."""
    url = f"https://api.github.com/repos/{repo_name}/contents/SECURITY.md?ref={branch}"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json().get(
                "content"
            )  # Return the raw content of the SECURITY.md file (encoded in base64)
        elif response.status_code == 404:
            return "SECURITY.md file not found."
        else:
            return f"Error: Received unexpected status code {response.status_code}."

    except requests.RequestException as e:
        return f"An error occurred: {e}"
