from concurrent.futures import ThreadPoolExecutor
from services.gitlab_service import fetch_prometheus_metrics

import yaml

# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()

"""2.1.X BUILD ENVIRONMENT"""


def check_2_1_1_pipeline_responsibility(pipeline_jobs):
    """
    Check the latest pipeline jobs to ensure each has a single responsibility.

    Returns:
        None: Prints the results and links to the jobs for manual review.
    """

    if not pipeline_jobs:
        print("No pipeline jobs found or failed to fetch jobs.")
        return

    for job in pipeline_jobs:
        print(f"Job ID: {job['id']}")
        print(f"Stage: {job['stage']}")
        print(f"Status: {job['status']}")
        print(f"URL: https://gitlab.com/{job['web_url']}\n")

    print("Manual Check Required:")
    print("1. Review each pipeline job by clicking the links above.")
    print(
        "2. Ensure each pipeline has a single responsibility (e.g., build, test, or deploy)."
    )
    print(
        "3. If a pipeline is performing multiple tasks, consider splitting it into smaller, distinct pipelines for compliance."
    )


def check_2_1_2_immutable_infrastructure(repo_tree):
    """
    Check if there are any Terraform or Ansible files in the repository tree and assign a compliance score.

    Args:
        repo_tree (list): The repository tree as a list of file objects.

    Returns:
        int: Compliance score (5 if Terraform or Ansible files are found, 0 otherwise).
    """
    found_terraform = False
    found_ansible = False

    for item in repo_tree:
        if item["type"] == "blob":  # 'blob' indicates it's a file
            if item["name"].endswith(".tf"):
                found_terraform = True
            elif item["name"] == "ansible.cfg" or item["name"].endswith(".yml"):
                found_ansible = True

            # If both types are found, we can stop early
            if found_terraform and found_ansible:
                break

    if found_terraform or found_ansible:
        # Found Terraform or Ansible files, return full compliance score
        print("Terraform or Ansible files found in the repository.")
        return 5
    else:
        # No Terraform or Ansible files found, return non-compliance
        print("No Terraform or Ansible files found in the repository.")
        return 0


def check_2_1_3_build_environment_logging(pipeline_jobs, job_logs, project_id, token):
    """
    Check if the build environment logs are available for the pipeline jobs.

    Args:
        pipeline_jobs (list): List of pipeline jobs.
        fetch_job_logs (func): Function to fetch logs for a job.
        project_id (int): The GitLab project ID.
        token (str): GitLab personal access token.

    Returns:
        int: Compliance score (5 if logs are found for all jobs, 0 otherwise).
    """
    all_logs_found = True

    for job in pipeline_jobs:
        job_id = job["id"]

        if job_logs:
            print(f"Logs found for job ID {job_id}")
        else:
            print(f"No logs found for job ID {job_id}")
            all_logs_found = False

    if all_logs_found:
        return 5  # Full compliance score
    else:
        return 0  # Non-compliance


def check_2_1_4_automated_build_environment(environments):
    """
    Check if the creation of the build environment is automated.

    Args:
        environments (list): List of environments in the GitLab project.

    Returns:
        int: Compliance score (5 if automated environments are found, 0 otherwise).
    """
    if environments:
        print(
            f"✅ Automated environments detected. {len(environments)} environments found. The project is compliant."
        )
        return 5  # Full compliance score
    else:
        print("❌ No automated environments found. The project is non-compliant.")
        return 0  # Non-compliance


def check_2_1_5_limited_access_to_build_environments(members):
    """
    Check if access to the build environment is limited to trusted users only.

    Args:
        members (list): List of project members with their roles.

    Returns:
        int: Compliance score (5 if access is limited, 0 otherwise).
    """
    for member in members:
        if member["access_level"] < 30:  # Assuming 30 is Developer access level
            print(f"Member {member['username']} has insufficient access level.")
            return 0  # Non-compliance if any member has insufficient access

    print("All members have appropriate access levels.")
    return 5  # Full compliance if all members have appropriate access


def check_2_1_6_authenticated_build_access(members):
    """
    Check if all users accessing the build environment are authenticated and have appropriate roles.

    Args:
        members (list): List of members with their roles.

    Returns:
        int: Compliance score (5 if all users are authenticated and authorized, 0 otherwise).
    """
    unauthorized_access = False
    required_roles = ["Reporter", "Developer", "Maintainer", "Owner"]

    for member in members:
        if member["access_level"] < 20:  # Reporter level or higher have access
            print(
                f"Unauthorized access: {member['username']} with access level {member['access_level']}"
            )
            unauthorized_access = True
        else:
            print(
                f"Authorized access: {member['username']} with access level {member['access_level']}"
            )

    if unauthorized_access:
        return 0  # Non-compliance
    else:
        return 5  # Full compliance score


def check_2_1_7_minimal_secrets_scope(gitlab_ci_content):
    """
    Check if build secrets are scoped minimally in the provided .gitlab-ci.yml content.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file.

    Returns:
        int: Compliance score (5 if secrets are scoped minimally, 0 otherwise).
    """
    secrets_found = False
    minimal_scope = True

    # Check each line in the .gitlab-ci.yml content
    for line in gitlab_ci_content.splitlines():
        if "secret" in line or "variable" in line:
            secrets_found = True
            # Assess the scope (you can customize this check based on your needs)
            if "global" in line:
                minimal_scope = False

    if secrets_found:
        if minimal_scope:
            print("Secrets are scoped minimally.")
            return 5  # Full compliance score
        else:
            print("Secrets are not scoped minimally.")
            return 0  # Non-compliance
    else:
        print("No secrets found in the .gitlab-ci.yml file.")
        return 5  # Full compliance if no secrets are found


def check_2_1_8_scan_build_infrastructure():
    """
    Reminder to manually ensure that the build infrastructure is scanned for vulnerabilities.

    Returns:
        int: Always return 0, because this check is manual.
    """
    print(
        "Manual Check: Ensure that the build infrastructure is automatically scanned for vulnerabilities using appropriate tools. This includes configuring your build environment to review dependencies, infrastructure, and scripts for known security issues."
    )
    return 0  # Return 0 because it's a manual check


def check_2_1_9_default_passwords():
    """
    Manual check to ensure that no default passwords are being used in GitLab.

    Returns:
        int: Always return 0, because this check is manual.
    """
    print(
        "Manual Check: Ensure that no default passwords are used in GitLab or any build tools. Review all related services and ensure no default credentials are present."
    )
    return 0


def check_2_1_10_secured_webhooks(webhooks):
    """
    Check if the webhooks in the GitLab project are secured (use HTTPS) and have SSL verification enabled.

    Args:
        webhooks (list): List of webhooks configured for the GitLab project.

    Returns:
        int: Compliance score (5 if all webhooks are secured, 0 otherwise).
    """
    if not webhooks:
        print("No webhooks found.")
        return 0  # Non-compliance if no webhooks are found

    all_webhooks_secured = True

    for webhook in webhooks:
        if webhook["url"].startswith("https://") and webhook["enable_ssl_verification"]:
            print(
                f"Webhook {webhook['id']} is secured with HTTPS and SSL verification is enabled."
            )
        else:
            print(f"Webhook {webhook['id']} is not secured properly.")
            all_webhooks_secured = False

    if all_webhooks_secured:
        return 5  # Full compliance score
    else:
        return 0  # Non-compliance if any webhook is not secured properly


def check_2_1_11_minimum_administrators(members):
    """
    Ensure that the number of administrators (Owners/Maintainers) is kept to a minimum.

    Args:
        members (list): List of project members with their access levels.

    Returns:
        int: Compliance score (5 if the minimum number of admins is set, 0 otherwise).
    """
    admin_roles = ["Owner", "Maintainer"]  # Define admin roles
    admin_count = 0

    for member in members:
        if member["access_level"] >= 40:  # Assuming 40+ is Maintainer and above
            admin_count += 1

    if admin_count > 2:  # You can adjust this number based on your policy
        print(
            f"❌ Too many administrators found: {admin_count}. Please reduce the number of admins."
        )
        return 0  # Non-compliance
    else:
        print(f"✅ Minimum administrators set correctly. Admin count: {admin_count}.")
        return 5  # Full compliance score


"""2.1.X BUILD ENVIRONMENT"""


def check_2_2_1_single_used_build_workers(pipeline_jobs):
    """
    Check if each pipeline job uses a single-use runner (e.g., a new VM/container).

    Args:
        pipeline_jobs (list): List of recent pipeline jobs.

    Returns:
        int: Compliance score (5 if all jobs use different runners, 0 otherwise).
    """
    runner_ids = set()  # To track unique runner IDs for each job
    non_compliant_jobs = []

    for job in pipeline_jobs:
        runner = job.get("runner") or {}
        runner_id = runner.get("id", None)
        if runner_id:
            if runner_id in runner_ids:
                print(
                    f"Non-compliant job found: Job ID {job['id']} reuses runner ID {runner_id}"
                )
                non_compliant_jobs.append(job["id"])
            else:
                runner_ids.add(runner_id)
        else:
            print(f"No runner information found for job ID {job['id']}")
            non_compliant_jobs.append(job["id"])

    # If no non-compliant jobs are found, we return a full compliance score
    if not non_compliant_jobs:
        print("✅ All pipeline jobs are using single-use runners.")
        return 5
    else:
        print(f"❌ Non-compliant jobs found: {non_compliant_jobs}.")
        return 0


def check_2_2_2_passed_not_pulled_environment(gitlab_ci_content):
    """
    Check if build worker environments and commands are passed and not pulled.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file.

    Returns:
        int: Compliance score (5 if environments/commands are passed and not pulled, 0 otherwise).
    """
    pulling_commands = False

    # Keywords to flag pulling commands from external sources
    suspicious_keywords = ["curl", "wget", "git clone", "fetch", "scp", "rsync"]

    # Check each line in the .gitlab-ci.yml content
    for line in gitlab_ci_content.splitlines():
        for keyword in suspicious_keywords:
            if keyword in line:
                pulling_commands = True
                print(f"Suspicious command found: {line}")

    if pulling_commands:
        print(
            "Some environment variables or commands are being pulled from external sources."
        )
        return 0  # Non-compliance score
    else:
        print(
            "Environment variables and commands are passed to the build workers, not pulled."
        )
        return 5  # Full compliance score


def check_2_2_3_segregated_duties():
    """
    Manual Check: Ensure the duties of each build worker are segregated.

    Instructions:
        1. Go to your GitLab project or group settings.
        2. Navigate to the CI/CD section.
        3. Expand the 'Runners' section and review the runners.
        4. Check that each runner is tagged with specific duties (e.g., test, compile, push artifacts).
        5. Ensure no runner is responsible for multiple duties.

    Reminder: Each runner should handle only one part of the build workflow, such as testing or compiling,
    to maintain clear separation of responsibilities and reduce security risks.

    Outcome:
        If all runners are handling only one specific duty, the environment is compliant.
        If any runner handles multiple duties, adjustments are required to segregate the tasks.

    Returns:
        str: Instruction message to complete the manual check.
    """
    message = (
        "Manual Check: Ensure that the duties of each build worker are segregated.\n"
        "Steps:\n"
        "1. Go to the project or group settings in GitLab.\n"
        "2. Navigate to 'CI/CD' and expand the 'Runners' section.\n"
        "3. Review the runners and check that each runner has only one specific responsibility (e.g., test, compile, deploy).\n"
        "4. Adjust the runner responsibilities if necessary to ensure that duties are separated across different runners.\n"
    )
    return message


def check_2_2_4_minimal_network_connectivity():
    """
    Manual Check: Ensure build workers have minimal network connectivity.

    This check cannot be automated via the API, so administrators should verify that the build workers are restricted in their network access, as recommended.
    The following actions should be reviewed manually:

    - Review the runner virtual machine network configurations.
    - Ensure runners are configured in their own network segment.
    - Verify that SSH access from the Internet to runner virtual machines is blocked.
    - Check that traffic between runner virtual machines is restricted.
    - Confirm that access to cloud provider metadata endpoints is filtered.

    Remediation steps:
    - If any of the above configurations are not in place, ensure that you implement these network restrictions to minimize connectivity and prevent external access or data leakage.
    """
    message = (
        "2.2.4 Ensure Build Workers Have Minimal Network Connectivity: "
        "Please manually review your build worker and runner configuration to ensure that they have minimal network connectivity. "
        "This includes verifying the segmentation of virtual machines, blocking of SSH access from the Internet, "
        "and restricting traffic between machines. Make sure only the necessary data flows between workers and cloud services."
    )

    return message


def check_2_2_5_runtime_security():
    """
    Manual check to ensure that run-time security is enforced for all build workers.

    This check cannot be automated through the API and requires manual verification.
    The purpose of this check is to confirm that security solutions (such as IDS,
    malware detection, or monitoring tools) are in place and monitoring the build workers
    during runtime.

    Returns:
        str: Message instructing the user to perform a manual check for run-time security.
    """
    message = (
        "2.2.5 Ensure Run-time Security is Enforced for Build Workers: \n"
        "- Please perform a manual review of your build infrastructure to ensure that all build workers "
        "have appropriate run-time security solutions enabled. This can include tools like Falco, AppArmor, "
        "or Seccomp, which monitor the worker's system for suspicious activities. \n"
        "- Verify that real-time security monitoring is configured and that logs are generated and reviewed. \n"
        "- Ensure that your organization has policies in place to require run-time security on build workers."
    )

    return message


def check_2_2_6_automatic_vulnerability_scan_manual():
    """
    Manual check to ensure that a container vulnerability scanning tool is used.

    Returns:
        str: Message prompting the user to manually verify the use of container scanning tools.
    """
    message = (
        "2.2.6 Ensure Build Workers are Automatically Scanned for Vulnerabilities: "
        "Please verify that the project uses a container vulnerability scanning tool. "
        "Ensure that tools like 'trivy', 'clair', 'anchore', 'snyk', or 'grype' are implemented "
        "to automatically scan containers for vulnerabilities. Check the Dockerfile, CI/CD pipeline, or other "
        "build configurations for references to these tools or similar alternatives."
    )
    return message


def check_2_2_7_version_control_for_deployment_configuration():
    """
    Manual Check: Ensure that the deployment configuration of build workers is stored in a version control platform.

    Instructions:
        1. Ensure that all build worker deployment configuration files (e.g., Dockerfiles, Kubernetes manifests,
           Terraform files, Ansible scripts, etc.) are stored in the GitLab repository or another version control system.
        2. Verify that any changes to these configurations are tracked in version control.
        3. Check if there's a process to review and approve changes to these files (e.g., through merge requests).
        4. Review historical commits to ensure that changes are properly documented and that there's a clear history of
           modifications.

    Outcome:
        If all deployment configuration files are stored in version control and changes are reviewed and tracked, the environment is compliant.
        If some deployment configurations are stored outside of version control or changes are not tracked, adjustments are required.

    Returns:
        str: Instruction message to complete the manual check.
    """
    message = (
        "Manual Check: Ensure that build workers' deployment configuration is stored in a version control platform.\n"
        "Steps:\n"
        "1. Ensure that all deployment configuration files (e.g., Dockerfiles, Kubernetes manifests, "
        "   Terraform/Ansible files, etc.) are stored in the GitLab repository or another version control system.\n"
        "2. Verify that changes to these configurations are tracked in version control and that a change history is visible.\n"
        "3. Check if there is a review process for changes to these files, such as merge request approvals.\n"
        "4. Ensure that historical commits show a clear documentation of configuration changes and their rationale."
    )
    return message


def check_2_2_8_resource_consumption_metrics(runners):
    """
    Check if the resource consumption of GitLab runners is being monitored using Prometheus metrics.

    Args:
        runners (list): List of runner dictionaries retrieved from the GitLab API.

    Returns:
        int: Compliance score (5 if metrics are fetched for all online runners, 0 otherwise).
    """
    print("Running check_2_2_8_resource_consumption_metrics...")

    # Fetch Prometheus metrics for the runners
    prometheus_metrics = fetch_prometheus_metrics(runners)

    # Track compliance and non-compliant runners
    compliant_runners = []
    non_compliant_runners = []

    for runner_id, metrics in prometheus_metrics.items():
        if isinstance(metrics, str) and "Error fetching metrics" not in metrics:
            compliant_runners.append(runner_id)
            print(f"✅ Runner {runner_id} is compliant with resource monitoring.")
        else:
            non_compliant_runners.append(runner_id)
            print(f"❌ Runner {runner_id} is non-compliant: {metrics}")

    # Calculate the compliance score
    if non_compliant_runners:
        print(f"❌ Non-compliant runners found: {non_compliant_runners}")
        return 0  # Non-compliance if any runner does not have Prometheus monitoring
    else:
        print("✅ All runners are compliant with resource consumption monitoring.")
        return 5  # Full compliance score if all runners have Prometheus metrics enabled


"""2.3.X PIPELINE INSTRUCTION"""


def check_2_3_1_build_steps_as_code(gitlab_ci_content):
    """
    Check if all build steps are defined as code and stored in a version control system.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file as a string.

    Returns:
        int: Compliance score (5 if .gitlab-ci.yml exists, 0 if not).
    """
    # Check if the .gitlab-ci.yml content exists
    if gitlab_ci_content:
        print("✅ .gitlab-ci.yml file exists. All build steps are defined as code.")
        return 5  # Compliance: .gitlab-ci.yml exists
    else:
        print("❌ .gitlab-ci.yml file is missing. Build steps are not defined as code.")
        return 0  # Non-compliance: .gitlab-ci.yml does not exist


def check_2_3_2_build_stage_io(gitlab_ci_content):
    """
    Check if build stages have clearly defined input and output (e.g., artifacts, dependencies) in the .gitlab-ci.yml file.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file as a string.

    Returns:
        int: Compliance score (5 if inputs/outputs are defined, 0 otherwise).
    """

    try:
        # Parse the YAML content
        gitlab_ci_config = yaml.safe_load(gitlab_ci_content)
    except yaml.YAMLError as e:
        print(f"Error parsing .gitlab-ci.yml content: {e}")
        return 0  # Non-compliance due to YAML parsing error

    io_defined = True
    stages_with_io = []

    # Iterate through the parsed YAML content
    for job_name, job_config in gitlab_ci_config.items():
        if isinstance(job_config, dict):
            # Check for "artifacts" or "dependencies" as part of input/output
            if "artifacts" in job_config or "dependencies" in job_config:
                print(
                    f"✅ {job_name} defines input/output through 'artifacts' or 'dependencies'."
                )
                stages_with_io.append(job_name)
            else:
                print(f"❌ {job_name} does not define explicit input/output.")
                io_defined = False

    if io_defined:
        return 5  # Full compliance
    else:
        print(
            f"❌ Some stages did not have clearly defined input/output: {stages_with_io}"
        )
        return 0  # Non-compliance


def check_2_3_3_separate_storage_for_artifacts(gitlab_ci_content):
    """
    Manual Check: Ensure pipeline output artifacts are written to a separate, secured storage repository.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file as a string.

    Returns:
        int: Compliance score (0 for non-compliance, 5 for compliance).
    """
    try:
        # Parse the YAML content
        gitlab_ci_config = yaml.safe_load(gitlab_ci_content)
    except yaml.YAMLError as e:
        print(f"Error parsing .gitlab-ci.yml content: {e}")
        return 0  # Non-compliance due to YAML parsing error

    artifacts_defined = False

    # Check if 'artifacts' keyword is defined
    for job_name, job_config in gitlab_ci_config.items():
        if isinstance(job_config, dict) and "artifacts" in job_config:
            artifacts_defined = True
            print(f"✅ Artifacts are defined in the job: {job_name}")

            # Further check if there's a configuration for external storage (this might be specific to your setup)
            if "paths" in job_config["artifacts"]:
                print(
                    f"Paths for artifacts are specified for job '{job_name}': {job_config['artifacts']['paths']}"
                )

    if artifacts_defined:
        print(
            "Please manually verify that these artifacts are being stored in a secured, separate storage repository."
        )
        return (
            5  # Assuming compliance based on definition, but needs manual verification
        )
    else:
        print(
            "❌ No artifacts are defined in the pipeline jobs, or they are not configured for external storage."
        )
        return 0  # Non-compliance if no artifacts are defined


def check_2_3_4_pipeline_files_tracked_and_reviewed(commit_history):
    """
    Check if changes to the pipeline files (.gitlab-ci.yml) are tracked in version control.

    Args:
        project_id (int): The ID of the GitLab project.
        private_token (str): Your GitLab personal access token.

    Returns:
        int: Compliance score (5 if changes are tracked, 0 if not).
    """
    file_path = ".gitlab-ci.yml"

    if commit_history:
        print(f"✅ The file '{file_path}' has a tracked history of changes:")
        for commit in commit_history:
            print(
                f"- Commit ID: {commit['id']}, Author: {commit['author_name']}, Date: {commit['created_at']}, Message: {commit['message']}"
            )
        return 5  # Full compliance if the file has a tracked history
    else:
        print(
            f"❌ No commit history found for '{file_path}'. This file may not be tracked or doesn't exist."
        )
        return 0  # Non-compliance if no history is found


def check_2_3_5_minimize_trigger_access(members):
    """
    Check if access to triggering the build process is minimized.

    Args:
        members (list): List of project members with their access levels.

    Returns:
        int: Compliance score (5 if access is minimized, 0 otherwise).
    """
    # Define roles that should have access to triggering pipelines (Owner = 50, Maintainer = 40)
    allowed_roles = [40, 50]

    unauthorized_members = []

    for member in members:
        if member["access_level"] not in allowed_roles:
            unauthorized_members.append(member["username"])
            print(
                f"❌ Unauthorized member found: {member['username']} with access level {member['access_level']}"
            )

    if not unauthorized_members:
        print(
            "✅ Access to triggering the build process is minimized to authorized members only."
        )
        return 5  # Full compliance
    else:
        print(f"❌ There are unauthorized members with access: {unauthorized_members}")
        return 0  # Non-compliance


def check_2_3_6_pipeline_scanning(approval_data):
    """
    Check if pipelines are automatically scanned for misconfigurations.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        int: Compliance score (5 if scanning tools are enabled, 0 otherwise).
    """
    # Define common scanning tools or jobs
    scanning_tools = [
        "SAST",
        "DAST",
        "Dependency Scanning",
        "Container Scanning",
        "License Compliance",
        "Secret Detection",
    ]

    if not approval_data:
        print(
            "No approval data found. Unable to verify if pipelines are being scanned for misconfigurations."
        )
        return 0

    scanning_found = False

    # Check if any of the approval rules indicate scanning tools
    for rule in approval_data:
        if isinstance(rule, dict):
            if any(tool in rule.get("name", "") for tool in scanning_tools):
                print(
                    f"✅ Scanning tool '{rule.get('name')}' is enabled in the approval settings."
                )
                scanning_found = True
        else:
            print(f"⚠️ Unexpected data format in approval_data: {rule}")

    if scanning_found:
        return 5  # Full compliance
    else:
        print(
            "❌ No scanning tools found in the approval rules. Pipelines are not being automatically scanned for misconfigurations."
        )
        return 0  # Non-compliance


def check_2_3_7_vulnerability_scanning(approval_data):
    """
    Check if pipelines are automatically scanned for vulnerabilities.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        int: Compliance score (5 if vulnerability scanning tools are enabled, 0 otherwise).
    """
    # Define common vulnerability scanning tools
    vulnerability_scanning_tools = [
        "SAST",
        "DAST",
        "Dependency Scanning",
        "Container Scanning",
        "License Compliance",
        "Secret Detection",
    ]

    if not approval_data:
        print(
            "No approval data found. Unable to verify if pipelines are being scanned for vulnerabilities."
        )
        return 0

    vulnerability_scanning_found = False

    # Check if any of the approval rules indicate vulnerability scanning tools
    for rule in approval_data:
        if isinstance(rule, dict):
            if any(
                tool in rule.get("name", "") for tool in vulnerability_scanning_tools
            ):
                print(
                    f"✅ Vulnerability scanning tool '{rule.get('name')}' is enabled in the approval settings."
                )
                vulnerability_scanning_found = True
        else:
            print(f"⚠️ Unexpected data format in approval_data: {rule}")

    if vulnerability_scanning_found:
        return 5  # Full compliance
    else:
        print(
            "❌ No vulnerability scanning tools found in the approval rules. Pipelines are not being automatically scanned for vulnerabilities."
        )
        return 0  # Non-compliance


def check_2_3_8_secret_scanner(approval_data):
    """
    Check if pipelines have scanners in place to identify and prevent sensitive data.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        int: Compliance score (5 if secret scanners are enabled, 0 otherwise).
    """
    # Define the name for the secret detection scanner
    secret_scanner_name = "Secret Detection"

    if not approval_data:
        print(
            "No approval data found. Unable to verify if the secret scanner is enabled."
        )
        return 0

    secret_scanner_found = False

    # Check if any of the approval rules indicate the presence of the secret scanner
    for rule in approval_data:
        if isinstance(rule, dict) and secret_scanner_name in rule.get("name", ""):
            print(
                f"✅ Secret scanner '{rule.get('name')}' is enabled in the approval settings."
            )
            secret_scanner_found = True

    if secret_scanner_found:
        return 5  # Full compliance
    else:
        print(
            "❌ No secret scanner found in the approval rules. Pipelines are not being scanned for sensitive data."
        )
        return 0  # Non-compliance


"""2.4.X PIPELINE INTEGRITY"""


def check_2_4_1_artifacts_signed(artifacts):
    """
    Check if all artifacts on all releases are signed.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.

    Returns:
        int: Compliance score (5 if all artifacts are signed, 0 otherwise).
    """

    if not artifacts:
        print("No artifacts found for the releases.")
        return 0

    unsigned_artifacts = []

    for artifact in artifacts:
        if artifact.get("signed"):
            print(f"✅ Artifact for release '{artifact['tag_name']}' is signed.")
        else:
            print(f"❌ Artifact for release '{artifact['tag_name']}' is not signed.")
            unsigned_artifacts.append(artifact["tag_name"])

    if unsigned_artifacts:
        print(
            f"❌ The following releases have unsigned artifacts: {unsigned_artifacts}"
        )
        return 0  # Non-compliance
    else:
        print("✅ All artifacts on all releases are signed.")
        return 5  # Full compliance


def check_2_4_2_locked_dependencies(dependency_files):
    """
    Check if all external dependencies used in the build process are locked.

    Args:
        project_id (int): The ID of the GitLab project.
        token (str): GitLab personal access token.
        branch (str): Branch of the project to check.

    Returns:
        int: Compliance score (5 if all dependencies are locked, 0 otherwise).
    """

    if not dependency_files:
        print(
            "❌ No dependency files found. Unable to verify if external dependencies are locked."
        )
        return 0

    all_dependencies_locked = True

    # Check if the dependency files have versions specified
    for file_name, content in dependency_files.items():
        if file_name == "Gemfile.lock":
            if "GEM" in content:
                print(f"✅ Dependencies are locked in {file_name}")
            else:
                print(f"❌ Dependencies in {file_name} do not appear to be locked.")
                all_dependencies_locked = False

        elif file_name in ["package-lock.json", "yarn.lock"]:
            if '"version":' in content:
                print(f"✅ Dependencies are locked in {file_name}")
            else:
                print(f"❌ Dependencies in {file_name} do not appear to be locked.")
                all_dependencies_locked = False

        elif file_name == "go.sum":
            if any(line.strip() for line in content.splitlines()):
                print(f"✅ Dependencies are locked in {file_name}")
            else:
                print(f"❌ Dependencies in {file_name} do not appear to be locked.")
                all_dependencies_locked = False

    if all_dependencies_locked:
        print("✅ All external dependencies used in the build process are locked.")
        return 5  # Full compliance
    else:
        print("❌ Some external dependencies are not locked.")
        return 0  # Non-compliance


def check_2_4_3_dependency_validation(approval_data):
    """
    Check if pipelines are using dependency scanning by inspecting approval data.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        int: Compliance score (5 if dependency scanning tools are enabled, 0 otherwise).
    """
    # Define common dependency scanning tools
    dependency_scanning_tools = ["Dependency Scanning"]

    if not approval_data:
        print(
            "No approval data found. Unable to verify if dependency scanning is in place."
        )
        return 0

    dependency_scanning_found = False

    # Check if any of the approval rules indicate the use of dependency scanning
    for rule in approval_data:
        if isinstance(rule, dict) and "name" in rule:
            if any(tool in rule["name"] for tool in dependency_scanning_tools):
                print(
                    f"✅ Dependency scanning tool '{rule['name']}' is enabled in the approval settings."
                )
                dependency_scanning_found = True

    if dependency_scanning_found:
        return 5  # Full compliance
    else:
        print("❌ No dependency scanning tools found in the approval rules.")
        return 0  # Non-compliance


def check_2_4_4_reproducible_artifacts(pipeline_ids, job_artifacts):
    """
    Check if build pipelines create reproducible artifacts.

    Args:
        pipeline_ids (list): List of pipeline IDs to compare artifacts.
        job_artifacts (dict): Dictionary containing artifacts for each pipeline job.

    Returns:
        int: Compliance score (5 if artifacts are reproducible, 0 otherwise).
    """
    artifact_data = {}

    # Fetch artifact details for each pipeline
    for pipeline_id in pipeline_ids:
        artifacts = job_artifacts.get(pipeline_id, [])

        if artifacts:
            artifact_data[pipeline_id] = artifacts
            print(f"Artifacts for pipeline {pipeline_id}: {artifacts}")
        else:
            print(f"No artifacts found for pipeline {pipeline_id}")
            return 0  # Non-compliance if no artifacts are found

    # Now compare artifacts from different pipeline runs
    first_pipeline_artifacts = artifact_data.get(pipeline_ids[0], [])
    for pipeline_id, artifacts in artifact_data.items():
        if pipeline_id == pipeline_ids[0]:
            continue  # Skip the first pipeline (it's our baseline)

        # Check if the artifacts from this pipeline match those from the first pipeline
        if first_pipeline_artifacts != artifacts:
            print(
                f"❌ Artifacts are not reproducible between pipelines {pipeline_ids[0]} and {pipeline_id}."
            )
            return 0  # Non-compliance if artifacts differ

    print("✅ All pipelines produce the same reproducible artifacts.")
    return 5  # Full compliance if all artifacts are reproducible


def check_2_4_5_sbom_generation(sbom_data):
    """
    Check if the pipeline generates an SBOM (Software Bill of Materials) during its run.

    Args:
        sbom_data (list): List of boolean values indicating if an SBOM was generated in each job.

    Returns:
        int: Compliance score (5 if SBOM generation is detected, 0 otherwise).
    """
    if any(sbom_data):
        print("✅ SBOM generation detected in the pipeline.")
        return 5  # Full compliance
    else:
        print("❌ No SBOM generation detected in the pipeline.")
        return 0  # Non-compliance


def check_2_4_6_sbom_signature(job_artifacts):
    """
    Check if the pipeline-generated SBOMs are signed.

    Args:
        job_artifacts (dict): Dictionary containing artifacts for each pipeline job.

    Returns:
        int: Compliance score (5 if all SBOMs are signed, 0 otherwise).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Ensure that every generated SBOM in the pipeline is signed.\n"
        "2. Validate the SBOM signatures to confirm they are generated by a trusted entity.\n"
        "3. If signatures are missing, configure the pipeline to sign the SBOM upon generation."
    )

    if not job_artifacts or not isinstance(job_artifacts, dict):
        print(f"❌ Invalid or missing job artifacts data. {manual_check_message}")
        return 0

    sbom_files_found = False
    signed_sbom_found = False

    for pipeline_id, artifacts in job_artifacts.items():
        # Ensure artifacts is iterable
        if not isinstance(artifacts, list):
            print(
                f"⚠️ Unexpected data type for artifacts in pipeline {pipeline_id}. Expected list but got {type(artifacts).__name__}."
            )
            continue

        for artifact in artifacts:
            # Check if the artifact is a string and ends with ".sbom.json"
            if isinstance(artifact, str) and artifact.endswith(".sbom.json"):
                sbom_files_found = True
                print(f"Found SBOM file: {artifact} in pipeline {pipeline_id}")

                # Check for a corresponding signature file (example: .sbom.json.sig)
                signature_file = f"{artifact}.sig"
                if signature_file in artifacts:
                    signed_sbom_found = True
                    print(f"✅ SBOM signature found: {signature_file}")
                else:
                    print(f"❌ Missing SBOM signature for: {artifact}")

    if sbom_files_found and signed_sbom_found:
        return 5  # Full compliance if all SBOMs are signed
    elif sbom_files_found and not signed_sbom_found:
        print(f"❌ SBOM files found but not signed. {manual_check_message}")
        return 0  # Non-compliance if SBOMs are not signed
    else:
        print(f"❌ No SBOM files were found in the artifacts. {manual_check_message}")
        return 0  # Non-compliance if no SBOM files were found


"""Runs every check"""


async def run_all_checks(
    pipeline_jobs,
    # repo_tree,
    job_logs,
    project_id,
    token,
    environments,
    members,
    gitlab_config,
    webhooks,
    runners,
    commit_history,
    approval_data,
    artifacts,
    dependency_files,
    job_artifacts,
    pipeline_ids,
):
    """Run all the checks defined in this file."""
    total_score = 0
    results = {}  # Dictionary to store check results

    checks = [
        (check_2_1_1_pipeline_responsibility, [pipeline_jobs]),
        # (check_2_1_2_immutable_infrastructure, [repo_tree]),
        (
            check_2_1_3_build_environment_logging,
            [pipeline_jobs, job_logs, project_id, token],
        ),
        (check_2_1_4_automated_build_environment, [environments]),
        (check_2_1_5_limited_access_to_build_environments, [members]),
        (check_2_1_6_authenticated_build_access, [members]),
        (check_2_1_7_minimal_secrets_scope, [gitlab_config]),
        (check_2_1_8_scan_build_infrastructure, []),  # Manual check
        (check_2_1_9_default_passwords, []),  # Manual check
        (check_2_1_10_secured_webhooks, [webhooks]),
        (check_2_1_11_minimum_administrators, [members]),
        (check_2_2_1_single_used_build_workers, [pipeline_jobs]),
        (check_2_2_2_passed_not_pulled_environment, [gitlab_config]),
        # (check_2_2_3_segregated_duties, [repo_tree]),
        (check_2_2_4_minimal_network_connectivity, []),  # Manual check
        (check_2_2_5_runtime_security, []),  # Manual check
        (check_2_2_6_automatic_vulnerability_scan_manual, []),  # Manual check
        (check_2_2_7_version_control_for_deployment_configuration, []),
        (check_2_2_8_resource_consumption_metrics, [runners]),
        (check_2_3_1_build_steps_as_code, [gitlab_config]),
        (check_2_3_2_build_stage_io, [gitlab_config]),
        (check_2_3_3_separate_storage_for_artifacts, [gitlab_config]),
        (check_2_3_4_pipeline_files_tracked_and_reviewed, [commit_history]),
        (check_2_3_5_minimize_trigger_access, [members]),
        (check_2_3_6_pipeline_scanning, [approval_data]),
        (check_2_3_7_vulnerability_scanning, [approval_data]),
        (check_2_3_8_secret_scanner, [approval_data]),
        (check_2_4_1_artifacts_signed, [artifacts]),
        (check_2_4_2_locked_dependencies, [dependency_files]),
        (check_2_4_3_dependency_validation, [approval_data]),
        (check_2_4_4_reproducible_artifacts, [pipeline_ids, job_artifacts]),
        (check_2_4_5_sbom_generation, [job_logs]),
        (check_2_4_6_sbom_signature, [job_artifacts]),
    ]

    for check, args in checks:
        print(f"Running {check.__name__}...")
        result = check(*args)  # Call the function with unpacked arguments

        # Handle both tuple (compliance score and message) results
        if isinstance(result, tuple):
            score, message = result
            total_score += score  # Accumulate the score from each check
            results[check.__name__] = message  # Save the message
            print(message)  # Print the message to the console
        elif isinstance(result, int):
            total_score += result  # Accumulate the score
            results[check.__name__] = result  # Save the score

        print("\n")  # Add space after each check's output

    # Calculate total possible score based on automated checks (which return integers)
    total_possible_score = (
        len([score for score in results.values() if isinstance(score, int)]) * 5
    )

    print("\n===========================")
    print(
        f"Total build pipelines compliance score: {total_score}/{total_possible_score}"
    )
    print("===========================")

    # Return both score and detailed results for manual checks
    return results
