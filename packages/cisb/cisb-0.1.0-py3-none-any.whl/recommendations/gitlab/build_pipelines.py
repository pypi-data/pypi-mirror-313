from concurrent.futures import ThreadPoolExecutor
from services.gitlab_service import fetch_prometheus_metrics
from services.common_utils import run_checks
import logging
import yaml
from collections import defaultdict


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline_checks.log"),  # Log to a file
        logging.StreamHandler(),  # Print to the console
    ],
)


# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()

"""2.1.X BUILD ENVIRONMENT"""


def check_2_1_1_pipeline_responsibility(pipeline_jobs):
    """
    Check the latest pipeline jobs to ensure each has a single responsibility.

    Returns:
        None, message: Always return None and a message for manual checks.
    """

    if not pipeline_jobs:
        message = "No pipeline jobs found or failed to fetch jobs."
        return None, message

    recent_jobs = pipeline_jobs[-5:]

    job_details = []
    for job in recent_jobs:
        job_info = (
            f"Job ID: {job['id']}\n"
            f"Stage: {job['stage']}\n"
            f"Status: {job['status']}\n"
            f"URL: {job['web_url']}\n"
        )
        job_details.append(job_info)

    message = (
        "Manual Check Required:\n"
        "1. Review each pipeline job by clicking the links above.\n"
        "2. Ensure each pipeline has a single responsibility (e.g., build, test, or deploy).\n"
        "3. If a pipeline is performing multiple tasks, consider splitting it into smaller, distinct pipelines for compliance.\n\n"
        + "\n".join(job_details)
    )

    return None, message


def check_2_1_2_immutable_infrastructure(ci_files):
    """
    Check if there are any CI files in the .gitlab/ci path and list the last 5 CI files.

    Args:
        ci_files (list): The repository tree as a list of file objects.

    Returns:
        None, message: Always return None for the score and a message indicating the findings.
    """

    if ci_files:
        last_5_ci_files = "\n".join(ci_files[-5:])
        message = (
            "To ensure pipeline infrastructure is immutable, it is important that the CI configurations "
            "remain unchanged once the pipeline is running. Below are the last 5 CI configuration files found in "
            "the `.gitlab/ci` directory. Review them for any necessary adjustments to ensure the infrastructure "
            "is immutable during pipeline execution:\n"
            f"{last_5_ci_files}"
        )
    else:
        message = (
            "No CI files found in the `.gitlab/ci` directory. This may indicate that no pipeline configurations "
            "are present, or the files may not be located in the expected path. Ensure that the pipeline "
            "infrastructure is configured properly and stored in the correct directory to maintain immutability."
        )

    return None, message


def check_2_1_3_build_environment_logging():
    """
    Manual check for build environment logging availability.

    Returns:
        tuple: (int, message) indicating that manual verification is needed for log availability.
    """
    message = (
        "⚠️ Manual Check Required: Please ensure that logs are available for all pipeline jobs.\n\n"
        "Steps:\n"
        "1. Verify that logs for each pipeline job are stored in a centralized organizational log store.\n"
        "2. Confirm that logs are accessible and reviewable for future audits.\n"
        "3. Check the logging paths and storage policies to ensure that log data is preserved.\n\n"
        "For further guidance, refer to the GitLab documentation on centralized log storage:\n"
        "https://docs.gitlab.com/ee/administration/job_logs.html"
    )
    return None, message


def check_2_1_4_automated_build_environment(environments):
    """
    Check if the creation of the build environment is automated.

    Args:
        environments (list): List of environments in the GitLab project.

    Returns:
        int, message: Returns a compliance score (5 if environments are present, 0 if not) and a message indicating the findings.
    """
    if environments:
        message = (
            f"✅ Automated build environments detected. {len(environments)} environments found.\n"
            "The project is compliant with the automation of the build environment. Review the environments to ensure "
            "they are configured as expected:\n"
            "- On the left sidebar, select 'Search' or go to 'Environments'.\n"
            "- Select 'Operate > Environments' to view and manage the environments.\n\n"
            "If any additional configuration or improvements are needed, you can adjust them through the GitLab CI/CD pipeline settings."
        )
        return 5, message
    else:
        message = (
            "❌ No automated environments found in the project.\n"
            "This means the project is non-compliant with automated build environment requirements. To ensure compliance:\n"
            "- Create a CI/CD pipeline using the gitlab-ci.yml file to automate the deployment of environments.\n"
            "- Review the GitLab documentation to configure automated environments: https://docs.gitlab.com/ee/ci/environments/"
        )
        return 0, message


def check_2_1_5_limited_access_to_build_environments(members):
    """
    Check if access to the build environment is limited to trusted users only, excluding bot accounts.

    Args:
        members (list): List of project members with their roles.

    Returns:
        int, message: Compliance score (5 if access is limited to trusted users, 0 otherwise) and a message describing the findings.
    """
    # List to capture members with insufficient access levels
    unauthorized_members = []

    # Iterate through the members to check access levels, ignoring bots
    for member in members:
        username = member.get("username", "")
        # Filter out bot accounts and check access level
        if "bot" not in username and member["access_level"] < 30:
            unauthorized_members.append(username)

    # Construct the return message
    if unauthorized_members:
        unauthorized_list = "\n".join(unauthorized_members)
        message = (
            "❌ Non-compliant: Some members (excluding bots) have insufficient access levels for the build environment.\n"
            "The following members need their access restricted or reviewed:\n"
            f"{unauthorized_list}\n\n"
            "Remediation steps:\n"
            "- Ensure that only users with Developer role (access level 30 or higher) or above have access to the build environment.\n"
            "- Review your project's access control settings to limit build environment access to trusted and qualified users only."
        )
        return 0, message  # Non-compliance score

    else:
        message = (
            "✅ Compliant: All members have appropriate access levels to the build environment.\n"
            "The project follows the best practices by limiting access to trusted and qualified users only. "
            "To continue ensuring security:\n"
            "- Regularly review access control settings to avoid unauthorized users gaining access.\n"
            "- Use GitLab’s 'Manage > Members' section to verify that only users with Developer or higher roles have access to critical environments."
        )
        return 5, message  # Full compliance score


def check_2_1_6_authenticated_build_access(members):
    """
    Check if all users accessing the build environment are authenticated and have appropriate roles,
    filtering out bot and token accounts.

    Args:
        members (list): List of members with their roles.

    Returns:
        int, message: Compliance score (5 if all users are authenticated and authorized, None otherwise)
        and a detailed message indicating the result.
    """
    unauthorized_access = False
    authorized_users = []
    unauthorized_users = []
    required_roles = ["Reporter", "Developer", "Maintainer", "Owner"]

    # Check each member's access level and filter out bots/tokens
    for member in members:
        access_level = member["access_level"]
        username = member["username"]

        # Filter out bots and token users
        if "bot" in username or "token" in username:
            continue

        if access_level < 20:  # Ensuring at least Reporter level (20)
            unauthorized_users.append(f"{username} (Access Level: {access_level})")
            unauthorized_access = True
        else:
            authorized_users.append(f"{username} (Access Level: {access_level})")

    # Constructing the output message
    if unauthorized_access:
        message = (
            "❌ Non-compliant: Unauthorized access detected to the build environment.\n"
            "The following users have insufficient access levels:\n"
            + "\n".join(unauthorized_users)
            + "\n\nRemediation steps:\n"
            "- Ensure all users with access to the build environment have at least 'Reporter' level access.\n"
            "- Remove or adjust permissions for users with insufficient access levels."
        )
        return 0, message
    else:
        message = (
            "✅ Compliant: All users accessing the build environment are authenticated and authorized.\n"
            "Authorized users with appropriate access levels:\n"
            + "\n".join(authorized_users)
            + "\n\nNo further action required."
        )
        return 5, message


def check_2_1_7_minimal_secrets_scope(ci_variables):
    """
    Check if secrets in the GitLab CI/CD pipeline are scoped minimally.

    Args:
        ci_variables (list): A list of CI/CD variables retrieved from the GitLab project.

    Returns:
        tuple: (None or int, message) describing the compliance and findings.
    """
    secrets_found = False
    minimal_scope = True
    overscoped_secrets = []

    # Loop through the variables to check for secrets
    for variable in ci_variables:
        key = variable.get("key")
        environment_scope = variable.get(
            "environment_scope", "*"
        )  # '*' means global scope

        # Check if the variable is considered a secret
        if "secret" in key.lower() or "token" in key.lower() or "key" in key.lower():
            secrets_found = True
            if environment_scope == "*":  # Global scope is overscoped
                minimal_scope = False
                overscoped_secrets.append(key)

    # Construct the return message based on findings
    if secrets_found:
        if minimal_scope:
            message = (
                "✅ Compliant: Secrets are scoped minimally to specific environments, ensuring better security.\n"
                "All sensitive variables (secrets, tokens, and keys) are correctly limited to appropriate scopes, "
                "minimizing their exposure."
            )
            return 5, message  # Full compliance score
        else:
            message = (
                "❌ Non-compliant: The following secrets are overscoped and available in all environments, which increases the risk of exposure:\n"
                + "\n".join(overscoped_secrets)
                + "\n\nRemediation steps:\n"
                "- Review and restrict the scope of these secrets to only the environments where they are needed (e.g., production, staging).\n"
                "- Modify the environment scope of each secret by editing the variable settings in GitLab: "
                "Go to 'Settings > CI/CD > Variables' and assign appropriate environment scopes.\n"
                "- For more guidance on scoping CI/CD variables, refer to the GitLab documentation: "
                "https://docs.gitlab.com/ee/ci/variables/#variable-scoping"
            )
            return 0, message  # Non-compliance score
    else:
        message = (
            "No secrets found in the CI/CD variables. If your pipeline requires sensitive data (e.g., API tokens, keys), "
            "ensure that these secrets are added with minimal scope to reduce security risks."
        )
        return None, message  # No secrets found


def check_2_1_8_scan_build_infrastructure():
    """
    Reminder to manually ensure that the build infrastructure is scanned for vulnerabilities.

    Returns:
        tuple: (int, message) Always return 0 (manual check) and a message reminding users to scan for vulnerabilities.
    """
    message = (
        "Manual Check Required: Ensure that the build infrastructure is scanned for vulnerabilities using appropriate tools.\n"
        "This should include automated scans for:\n"
        "- Known security vulnerabilities in dependencies (e.g., libraries, modules).\n"
        "- Infrastructure configurations (e.g., Terraform, Ansible).\n"
        "- Scripts and other components that might be part of the build process.\n\n"
        "Consider using tools like SAST, DAST, or dependency scanning to detect these vulnerabilities and ensure they are addressed."
    )

    return None, message


def check_2_1_9_default_passwords():
    """
    Manual check to ensure that no default passwords are being used in GitLab or build tools.

    Returns:
        tuple: (int, message) Always return 0 (manual check) and a message reminding users to avoid default passwords.
    """
    message = (
        "Manual Check Required: Review all services and ensure that no default passwords are used in GitLab or any other related build tools.\n"
        "This includes:\n"
        "- Verifying that no default credentials are set in any systems.\n"
        "- Changing default passwords where applicable to secure and unique credentials.\n\n"
        "Default passwords can be an easy target for attackers. Review your environment and update passwords to maintain security best practices."
    )

    return None, message


def check_2_1_10_secured_webhooks(webhooks):
    """
    Check if the webhooks in the GitLab project are secured (use HTTPS) and have SSL verification enabled.

    Args:
        webhooks (list): List of webhooks configured for the GitLab project.

    Returns:
        tuple: (int, message) Compliance score (5 if all webhooks are secured, 0 otherwise) and a message describing the findings.
    """
    if not webhooks:
        message = (
            "Manual Check Required: "
            "No webhooks found in the GitLab project. This may indicate that no external services are triggered by "
            "the project. If webhooks are used, ensure they are properly configured with HTTPS and SSL verification."
        )
        return None, message

    all_webhooks_secured = True
    unsecured_webhooks = []

    # Iterate over each webhook to check security configuration
    for webhook in webhooks:
        if webhook["url"].startswith("https://") and webhook["enable_ssl_verification"]:
            print(
                f"Webhook {webhook['id']} is secured with HTTPS and SSL verification enabled."
            )
        else:
            unsecured_webhooks.append(webhook["id"])
            all_webhooks_secured = False

    if all_webhooks_secured:
        message = (
            "✅ Compliant: All webhooks are secured using HTTPS with SSL verification enabled.\n"
            "You are following best practices to ensure secure communication for your webhook requests."
        )
        return 5, message  # Full compliance score
    else:
        unsecured_webhook_list = "\n".join([str(id) for id in unsecured_webhooks])
        message = (
            "Manual Check Required: "
            f"❌ Non-compliant: The following webhooks are not secured properly (either missing HTTPS or SSL verification):\n"
            f"{unsecured_webhook_list}\n\n"
            "Remediation steps:\n"
            "- Ensure that all webhook URLs use HTTPS to protect the integrity and confidentiality of data in transit.\n"
            "- Enable SSL verification for each webhook to ensure secure connections.\n"
            "You can review the settings for webhooks under 'Settings > Webhooks' in your GitLab project."
        )
        return 0, message  # Non-compliance score


def check_2_1_11_minimum_administrators(members):
    """
    Ensure that the number of administrators (Owners/Maintainers) is kept to a minimum, excluding bot accounts.
    This is a manual check that outputs the list of admins for review.

    Args:
        members (list): List of project members with their access levels.

    Returns:
        tuple: (None, message) Compliance score (None for manual checks) and a message describing the findings.
    """
    admin_roles = ["Owner", "Maintainer"]  # Define admin roles
    admin_count = 0
    admin_list = []

    # Iterate through members to count and list administrators, excluding bots
    for member in members:
        if (
            member["access_level"] >= 40 and "bot" not in member["username"].lower()
        ):  # Exclude bots
            admin_count += 1
            admin_list.append(
                f"{member['username']} (Access Level: {member['access_level']})"
            )

    # Construct the return message based on findings
    admin_details = "\n".join(admin_list)
    message = (
        f"Manual Check Required: The project has {admin_count} administrators (excluding bots).\n"
        "The following members have Maintainer or Owner roles:\n"
        f"{admin_details}\n\n"
        "Remediation steps:\n"
        "- Review the members with elevated privileges to ensure only essential personnel have administrative rights.\n"
        "- Reduce the number of users with admin-level access (Maintainer/Owner) if possible."
    )
    
    return None, message  # Manual check score


"""2.1.X BUILD ENVIRONMENT"""


def check_2_2_1_single_used_build_workers(pipeline_jobs):
    """
    Check if each pipeline job uses a single-use runner (e.g., a new VM/container) within the same pipeline.

    Args:
        pipeline_jobs (list): List of recent pipeline jobs.

    Returns:
        tuple: Compliance score (5 if all jobs within a pipeline use different runners, 0 otherwise) and a message indicating the findings.
    """
    pipeline_runners = defaultdict(set)  # To track unique runner IDs by pipeline
    non_compliant_pipelines = []

    # Group jobs by pipeline and check runner uniqueness
    for job in pipeline_jobs:
        if not job:  # Check if job is None or empty
            continue

        # Extract pipeline ID safely
        pipeline = job.get("pipeline") if isinstance(job, dict) else None
        pipeline_id = pipeline.get("id") if isinstance(pipeline, dict) else None

        # Extract runner ID safely
        runner = job.get("runner") if isinstance(job, dict) else None
        runner_id = runner.get("id") if isinstance(runner, dict) else None

        # If there's no runner information, mark the job as non-compliant
        if runner_id is None:
            non_compliant_pipelines.append(
                f"Pipeline ID: {pipeline_id or 'Unknown'} - Job ID: {job.get('id', 'Unknown')} has no runner information."
            )
            continue

        # Check if the runner ID is reused within the same pipeline
        if pipeline_id and runner_id in pipeline_runners[pipeline_id]:
            non_compliant_pipelines.append(
                f"Pipeline ID: {pipeline_id} - Job ID: {job.get('id', 'Unknown')} reuses runner ID: {runner_id}"
            )
        elif pipeline_id:
            pipeline_runners[pipeline_id].add(runner_id)

    # Construct the message based on compliance
    if not non_compliant_pipelines:
        message = (
            "✅ Compliant: All jobs within each pipeline are using unique, single-use runners.\n"
            "This ensures that each job runs on a clean, isolated runner instance, reducing the risk of data "
            "leakage or state retention between jobs."
        )
        return 5, message  # Full compliance score
    else:
        non_compliant_list = "\n".join(non_compliant_pipelines)
        message = (
            "❌ Non-compliant: Some pipelines have jobs that reuse the same runner instance. "
            "This could lead to data retention or state leakage between jobs.\n"
            "Non-compliant pipelines and jobs:\n"
            f"{non_compliant_list}\n\n"
            "Remediation steps:\n"
            "- Configure each pipeline job to use a dedicated, single-use runner to ensure isolation.\n"
            "- Review GitLab Runner configurations to enforce ephemeral runners or use GitLab Runner SaaS if available."
        )
        return 0, message 
    

def check_2_2_2_passed_not_pulled_environment():
    """
    Manual Check: Ensure that build worker environments and commands are passed and not pulled.

    Returns:
        tuple: (int, message) Always return 0 and a detailed manual check message.
    """
    message = (
        "Manual Check Required:\n\n"
        "This check ensures that build worker environments and commands are passed directly to the runner (e.g., using predefined variables and configurations) "
        "and not dynamically pulled from external sources during the job execution. Below are the steps to verify this in your GitLab CI configuration:\n\n"
        "1. **Review `.gitlab-ci.yml` file:**\n"
        "- Open your project's `.gitlab-ci.yml` file and examine the stages, scripts, and jobs defined within.\n"
        "- Ensure that all environment variables, commands, and configurations needed by the build workers are defined directly in the `.gitlab-ci.yml` file, "
        "rather than being pulled from external resources.\n"
        "- Look for commands like `curl`, `wget`, `git clone`, `fetch`, `scp`, and `rsync`, which may indicate that configurations or dependencies are being "
        "fetched from external sources during runtime. These should be replaced with secure, pre-configured settings within the project or repository.\n\n"
        "2. **Examine Runner Configuration:**\n"
        "- Go to your GitLab Runner setup (Settings > CI/CD > Runners) and verify that the runner is using predefined images, environment variables, and configurations.\n"
        "- Check that these configurations are controlled within the project or via secure, versioned base images. Ensure no dynamic fetching of configurations "
        "occurs during the build.\n\n"
        "3. **Check for External Dependencies:**\n"
        "- Review third-party dependencies, libraries, or tools referenced in your `.gitlab-ci.yml` or runner configurations.\n"
        "- These should be explicitly defined and version-controlled in the project repository or fetched through trusted sources (e.g., secure container registries). "
        "Avoid pulling dependencies from remote, unsecured locations during the pipeline run, as this can expose the build process to attacks like man-in-the-middle attacks.\n\n"
        "By ensuring that environment variables and configurations are passed securely to build workers, you minimize security risks and maintain compliance "
        "with best practices for secure, automated pipelines."
    )

    return None, message  # Manual check, no compliance score assigned


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
    return None, message


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

    return None, message


def check_2_2_5_runtime_security():
    """
    Manual check to ensure that run-time security is enforced for all build workers.

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

    return None, message


def check_2_2_6_automatic_vulnerability_scan_manual(approval_data):
    """
    Manual check to ensure that a container vulnerability scanning tool is used, based on approval data.

    Args:
        approval_data (dict): Data that includes information about approved or in-use vulnerability scanning tools.

    Returns:
        str: Message prompting the user to manually verify the use of container scanning tools,
             including those found in the approval_data.
    """
    # Extract vulnerability scanners from the approval_data
    scanners_in_use = approval_data.get("vulnerability_scanners", [])

    # Format the scanners into a readable string
    scanners_str = (
        ", ".join(scanners_in_use)
        if scanners_in_use
        else "No scanners found in approval data."
    )

    message = (
        "2.2.6 Ensure Build Workers are Automatically Scanned for Vulnerabilities: "
        "Please verify that the project uses a container vulnerability scanning tool. "
        "The following tools were found in the approval data: {scanners}. "
        "Ensure that these or similar tools like 'trivy', 'clair', 'anchore', 'snyk', or 'grype' "
        "are implemented to automatically scan containers for vulnerabilities. Check the Dockerfile, CI/CD pipeline, or other "
        "build configurations for references to these tools or similar alternatives."
    ).format(scanners=scanners_str)

    return None, message


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
    return None, message


def check_2_2_8_resource_consumption_metrics(runners):
    """
    Manual check to ensure that GitLab runners are monitored for resource consumption using Prometheus metrics.

    Args:
        runners (list): List of runner dictionaries retrieved from the GitLab API.

    Returns:
        str: A message prompting the user to verify Prometheus monitoring and listing the runners by name.
    """
    # List of runner names
    runner_names = [runner.get("description", "Unknown") for runner in runners]

    # Message explaining the manual steps for compliance
    message = (
        "2.2.8 Ensure GitLab Runners' Resource Consumption is Monitored:\n"
        "This check is manual, and you need to verify that Prometheus or a similar tool is being used "
        "to monitor the resource consumption of your GitLab runners. Monitoring resource consumption helps ensure "
        "efficient use of resources and provides insight into potential performance bottlenecks. Here's how to ensure compliance:\n\n"
        "Steps to be compliant:\n"
        "1. **Check Runner Configuration**: Ensure that each GitLab runner is configured to expose Prometheus metrics. "
        "This can typically be done by enabling a metrics endpoint on port 9252 in the runner's configuration file (`config.toml`). "
        "For example, you can check `/etc/gitlab-runner/config.toml` to verify if Prometheus metrics are enabled.\n"
        "2. **Prometheus Scrape Config**: If Prometheus is already set up in your environment, make sure it is configured to scrape the metrics from your runners. "
        "Verify the `prometheus.yml` configuration file to ensure that the runners are listed as scrape targets. Look for a section similar to the following:\n"
        "   ```yaml\n"
        "   scrape_configs:\n"
        "     - job_name: 'gitlab-runners'\n"
        "       static_configs:\n"
        "         - targets: ['runner1.example.com:9252', 'runner2.example.com:9252']\n"
        "   ```\n"
        "3. **Verify Metrics Availability**: Use `curl` to check if Prometheus metrics are accessible on the runner by executing the following command on each runner:\n"
        "   ```bash\n"
        "   curl http://<runner_hostname>:9252/metrics\n"
        "   ```\n"
        "   Replace `<runner_hostname>` with the actual hostname of the runner. If this command returns a list of metrics, then Prometheus is successfully collecting data.\n"
        "4. **Enable Prometheus in GitLab Runner**: If Prometheus is not yet enabled on the runner, modify the GitLab Runner configuration to enable Prometheus metrics. You can add the following section to your `config.toml` file:\n"
        "   ```toml\n"
        "   [metrics]\n"
        '   address = ":9252"\n'
        "   ```\n"
        "   After modifying the configuration, restart the GitLab runner for the changes to take effect.\n"
        "5. **Confirm Compliance**: Periodically review the Prometheus metrics and logs to ensure the metrics are being collected and no errors are occurring.\n\n"
        "List of Runners (by name):\n"
    )

    # Append runner names to the message
    message += "\n".join(f"- {name}" for name in runner_names)

    return None, message


"""2.3.X PIPELINE INSTRUCTION"""


def check_2_3_1_build_steps_as_code(gitlab_ci_content):
    """
    Check if all build steps are defined as code and stored in a version control system.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file as a string.

    Returns:
        tuple: A tuple containing:
            - int: Compliance score (5 if .gitlab-ci.yml exists, 0 if not).
            - str: A message describing the result and steps for remediation if needed.
    """
    # Check if the .gitlab-ci.yml content exists
    if gitlab_ci_content:
        message = (
            "✅ Compliance: .gitlab-ci.yml file exists. All build steps are defined as code "
            "and stored in version control, which helps automate and secure your build pipeline. "
            "No further action is needed."
        )
        return 5, message  # Compliance: .gitlab-ci.yml exists
    else:
        message = (
            "❌ Non-compliance: .gitlab-ci.yml file is missing. Build steps are not currently defined as code, "
            "which increases the risk of human error and makes it difficult to audit and secure your build process.\n\n"
            "To become compliant, follow these steps:\n"
            "1. Navigate to the repository where the build steps should be defined.\n"
            "2. Create a `.gitlab-ci.yml` file at the root of the repository.\n"
            "3. Define the necessary pipeline instructions (jobs, stages, scripts) inside the file.\n"
            "4. Commit the `.gitlab-ci.yml` file to the version control system.\n\n"
            "Once the file is created, your project will be compliant, and the pipeline steps will be automated and versioned."
        )
        return 0, message  # Non-compliance: .gitlab-ci.yml does not exist


def check_2_3_2_build_stage_io():
    """
    Provide guidance for manually checking if build stages have clearly defined input and output 
    (e.g., artifacts, dependencies) in the .gitlab-ci.yml file.

    Args:
        gitlab_ci_content (str): The content of the .gitlab-ci.yml file as a string (not used for parsing).

    Returns:
        tuple: (int, message) - Compliance score (None for manual check) and a message with guidance.
    """

    message = (
        "🔍 Manual Check Required: Review the `.gitlab-ci.yml` file to ensure each build stage "
        "has clearly defined input and output using 'artifacts' or 'dependencies'.\n\n"
        "Guidance:\n"
        "1. Open the `.gitlab-ci.yml` file.\n"
        "2. For each job in the file, check if 'artifacts' or 'dependencies' are specified.\n"
        "   - 'artifacts' define outputs that can be shared with subsequent stages or jobs.\n"
        "   - 'dependencies' specify inputs from previous stages or jobs.\n"
        "3. Ensure that each build stage has the necessary configuration to explicitly define inputs and outputs.\n\n"
        "Remediation steps:\n"
        "- If any stage lacks defined input/output, consider adding 'artifacts' or 'dependencies' to improve clarity and reproducibility.\n"
        "- Refer to the GitLab documentation for further guidance: https://docs.gitlab.com/ee/ci/pipelines/"
    )

    return None, message


def check_2_3_3_separate_storage_for_artifacts():
    """
    Manual Check: Ensure pipeline output artifacts are written to a separate, secured storage repository.

    Returns:
        tuple: (None, message) describing the manual check instructions.
    """
    message = (
        "Manual Check Required:\n\n"
        "- Review the `.gitlab-ci.yml` file to ensure pipeline jobs define output artifacts.\n"
        "- Verify that artifacts are stored in a separate, secured storage repository (e.g., a dedicated object storage bucket).\n"
        "- Ensure storage configurations follow security best practices, including access control, encryption, and isolation from the pipeline execution environment.\n"
        "- Document the findings of this manual review for compliance purposes."
    )
    return None, message


def check_2_3_4_pipeline_files_tracked_and_reviewed(commit_history):
    """
    Check if changes to the pipeline files (.gitlab-ci.yml) are tracked in version control.

    Args:
        commit_history (list): List of commit history for the .gitlab-ci.yml file.

    Returns:
        tuple: (Compliance score, Message)
    """
    file_path = ".gitlab-ci.yml"

    if commit_history:
        message = f"✅ The file '{file_path}' has a tracked history of changes. Below are the recent commits:\n"
        for commit in commit_history[
            :5
        ]:  # Display up to the last 5 commits for clarity
            message += (
                f"- Commit ID: {commit['id']}\n"
                f"  Author: {commit['author_name']}\n"
                f"  Date: {commit['created_at']}\n"
                f"  Message: {commit['message']}\n\n"
            )
        message += (
            "The pipeline file is being properly tracked in version control, and you can review changes by "
            "selecting **Code > Repository** in the GitLab sidebar. Use the 'History' option to track and review changes."
        )
        return 5, message  # Full compliance
    else:
        # No commit history found
        message = (
            f"❌ No commit history found for '{file_path}'. This could indicate that the file is not being tracked "
            "in version control, or it may not exist in the repository.\n\n"
            "To ensure compliance:\n"
            "- Ensure the `.gitlab-ci.yml` file exists in the root of your repository.\n"
            "- Track changes to it by committing and pushing updates regularly.\n"
            "- Use GitLab's **History** feature to monitor changes to pipeline files and ensure proper review."
        )
        return 0, message


def check_2_3_5_minimize_trigger_access(protected_environments):
    """
    Check if access to triggering the build process is minimized in protected environments.

    Args:
        protected_environments (list): List of protected environments with their deploy access details.

    Returns:
        tuple: (int, message) Compliance score (5 if access is minimized, 0 otherwise) and a message describing the findings.
    """
    if not protected_environments:
        # No protected environments, recommend a manual check
        message = (
            "⚠️ No protected environments configured in this project. "
            "Please perform a manual review to ensure that only authorized members have access to trigger pipeline deployments.\n"
            "You can set up protected environments in GitLab under Settings > CI/CD > Protected Environments."
        )
        return None, message

    non_compliant_environments = []
    for env in protected_environments:
        environment_name = env["name"]
        allowed_access = env.get("deploy_access_levels", [])

        unauthorized_access = [
            access for access in allowed_access
            if access.get("access_level_description") not in ["Maintainers", "Developers"]
        ]

        if unauthorized_access:
            non_compliant_details = [
                f"User ID: {access.get('user_id') or 'N/A'}, Group ID: {access.get('group_id') or 'N/A'}, Access Level: {access.get('access_level_description')}"
                for access in unauthorized_access
            ]
            non_compliant_environments.append(
                f"Environment: {environment_name}\n- " + "\n- ".join(non_compliant_details)
            )

    # Construct compliance message based on findings
    if not non_compliant_environments:
        message = (
            "✅ Compliant: Access to triggering the build process is minimized in all protected environments.\n"
            "Only authorized roles (Maintainers, Developers) have deploy permissions."
        )
        return 5, message
    else:
        non_compliant_list = "\n\n".join(non_compliant_environments)
        message = (
            "❌ Non-compliant: Some protected environments have unauthorized access configured for triggering deployments.\n"
            f"{non_compliant_list}\n\n"
            "Remediation steps:\n"
            "- Limit deploy access to authorized roles (e.g., Maintainers and Developers only).\n"
            "- Review the members with access to each protected environment and adjust their roles as necessary to comply with the least privilege principle.\n"
            "You can manage protected environments in GitLab under Settings > CI/CD > Protected Environments."
        )
        return 0, message


def check_2_3_6_pipeline_scanning(approval_data):
    """
    Check if pipelines are automatically scanned for misconfigurations by examining the approval settings for enabled scanning tools.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        tuple: Compliance score (5 if scanning tools are enabled, 0 otherwise) and a message describing the findings.
    """
    # Define the scanning tools we expect to see
    scanning_tools = [
        "sast",
        "secret_detection",
        "dependency_scanning",
        "container_scanning",
        "dast",
        "coverage_fuzzing"
    ]

    if not approval_data:
        message = (
            "❌ No approval data found. Unable to verify if pipelines are being scanned for misconfigurations.\n"
            "Please ensure the approval rules include scanning tools such as SAST, DAST, Dependency Scanning, "
            "or Secret Detection. Without these tools enabled, misconfigurations may go undetected."
        )
        return None, message

    scanning_found = False
    enabled_scanning_tools = set()

    # Check if any of the approval rules have scanning tools enabled
    for rule in approval_data.get("rules", []):
        scanners = rule.get("scanners", [])
        
        # Check if any defined scanning tools are in this rule's scanners
        for tool in scanning_tools:
            if tool in scanners:
                enabled_scanning_tools.add(tool)
                scanning_found = True

    # Construct the return message based on findings
    if scanning_found:
        enabled_tools_list = ", ".join(enabled_scanning_tools)
        message = (
            "✅ Compliant: The following scanning tools are enabled in the approval settings:\n"
            f"{enabled_tools_list}\n"
            "These tools help ensure that your pipelines are automatically scanned for misconfigurations."
        )
        return 5, message
    else:
        message = (
            "❌ Non-compliant: No scanning tools found in the approval rules. Pipelines are not being "
            "automatically scanned for misconfigurations.\n"
            "To ensure compliance, enable tools such as SAST, DAST, Dependency Scanning, and Secret Detection "
            "in your pipeline settings."
        )
        return 0, message

def check_2_3_7_vulnerability_scanning(approval_data):
    """
    Check if pipelines are automatically scanned for vulnerabilities.

    Args:
        approval_data (dict): Approval data fetched from GitLab.

    Returns:
        tuple: (int, message) Compliance score (5 if vulnerability scanning tools are enabled, 0 otherwise) and message detailing findings.
    """
    # Define common vulnerability scanning tools
    vulnerability_scanning_tools = [
        "sast",
        "secret_detection",
        "dependency_scanning",
        "container_scanning",
        "dast",
        "coverage_fuzzing"
    ]

    if not approval_data:
        message = (
            "❌ No approval data found. Unable to verify if pipelines are being scanned for vulnerabilities.\n"
            "Ensure that pipelines include vulnerability scanning stages in their CI configuration."
        )
        return None, message

    enabled_scanners = set()

    # Check each rule's `scanners` field for vulnerability scanning tools
    for rule in approval_data.get("rules", []):
        scanners = rule.get("scanners", [])
        for tool in vulnerability_scanning_tools:
            if tool in scanners:
                enabled_scanners.add(tool)

    # Construct the message based on findings
    if enabled_scanners:
        tools_list = ", ".join(enabled_scanners)
        message = (
            "✅ Compliant: Vulnerability scanning is enabled for the following tools:\n"
            f"- {tools_list}\n\n"
            "Pipelines are compliant with automatic vulnerability scanning best practices."
        )
        return 5, message
    else:
        message = (
            "❌ No vulnerability scanning tools found in the approval rules.\n"
            "Pipelines are not being automatically scanned for vulnerabilities.\n"
            "Remediation:\n"
            "- Add stages to the pipeline configuration that include SAST, DAST, Dependency Scanning, and other vulnerability detection tools."
        )
        return 0, message


def check_2_3_8_secret_scanner(approval_data):
    """
    Check if pipelines have scanners in place to identify and prevent sensitive data.

    Args:
        approval_data (dict): Approval data fetched from GitLab.

    Returns:
        tuple: (int, message) Compliance score (5 if secret scanners are enabled, 0 otherwise), and a message with findings.
    """
    # Define the name for the secret detection scanner
    secret_scanner_name = "secret_detection"

    if not approval_data:
        message = (
            "❌ No approval data found. Unable to verify if the secret scanner is enabled.\n"
            "Manual remediation required: Ensure that secret detection is configured in your pipelines. "
            "Refer to GitLab's documentation for setting up Secret Detection: https://docs.gitlab.com/ee/user/application_security/secret_detection/"
        )
        return None, message

    secret_scanner_found = False

    # Check each rule's `scanners` field for the secret scanner
    for rule in approval_data.get("rules", []):
        if secret_scanner_name in rule.get("scanners", []):
            secret_scanner_found = True
            break  # Stop once we find the scanner enabled

    # Construct the message based on findings
    if secret_scanner_found:
        message = (
            "✅ Compliant: Secret scanner is enabled in the approval settings.\n"
            "Pipelines are being scanned for sensitive data like credentials and API keys.\n"
            "No further action required, but continue reviewing regularly to ensure security."
        )
        return 5, message
    else:
        message = (
            "❌ Non-compliant: No secret scanner found in the approval rules.\n"
            "Pipelines are not being scanned for sensitive data.\n\n"
            "Remediation steps:\n"
            "- Add 'Secret Detection' to your pipeline settings by including the following lines in your `.gitlab-ci.yml` file:\n"
            "```yaml\n"
            "include:\n"
            "  - template: Jobs/Secret-Detection.gitlab-ci.yml\n"
            "```\n"
            "- Validate your pipeline settings in GitLab.\n"
            "For more details, see: https://docs.gitlab.com/ee/user/application_security/secret_detection/"
        )
        return 0, message


"""2.4.X PIPELINE INTEGRITY"""


def check_2_4_1_artifacts_signed(artifacts):
    """
    Check if all artifacts in the project releases are signed.

    Args:
        artifacts (list): List of artifacts from the project releases.

    Returns:
        int, message: Compliance score (5 if all artifacts are signed, 0 otherwise), and a message describing the findings.
    """
    if not artifacts:
        message = "❌ No artifacts found for the releases. Please ensure artifacts are being created and signed for every release."
        return None, message

    unsigned_artifacts = []

    # Iterate through the artifacts and check if they are signed
    for artifact in artifacts:
        if artifact.get("signed"):
            print(f"✅ Artifact for release '{artifact['tag_name']}' is signed.")
        else:
            unsigned_artifacts.append(artifact["tag_name"])

    if unsigned_artifacts:
        unsigned_list = "\n".join(unsigned_artifacts)
        message = (
            f"Partially compliant: The following releases have unsigned artifacts:\n"
            f"{unsigned_list}\n\n"
            "Remediation steps:\n"
            "- Ensure that all release artifacts are signed using user or organization keys.\n"
            "- Follow GitLab's documentation on signing release artifacts: https://docs.gitlab.com/ee/user/project/releases/"
        )
        return 3, message
    else:
        message = (
            "✅ All artifacts in all releases are properly signed.\n"
            "The project is compliant with artifact signing requirements, ensuring artifact integrity and security."
        )
        return 5, message


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
        print("Some external dependencies are not locked.")
        return 3  # Non-compliance


def check_2_4_2_locked_dependencies(dependency_files):
    """
    Check if all external dependencies used in the build process are locked.

    Args:
        dependency_files (dict): A dictionary of file names and their content representing dependency files.

    Returns:
        int, message: Compliance score (5 if all dependencies are locked, otherwise a lower score) and a message describing the findings.
    """

    if not dependency_files:
        message = (
            "❌ No dependency files found. Unable to verify if external dependencies are locked.\n"
            "Ensure that the project contains dependency lock files such as 'Gemfile.lock', 'package-lock.json', 'yarn.lock', or 'go.sum'."
        )
        return 0, message

    all_dependencies_locked = True
    non_compliant_files = []

    # Check if the dependency files have versions specified
    for file_name, content in dependency_files.items():
        if file_name == "Gemfile.lock":
            if "GEM" in content:
                print(f"✅ Dependencies are locked in {file_name}")
            else:
                print(f"❌ Dependencies in {file_name} do not appear to be locked.")
                all_dependencies_locked = False
                non_compliant_files.append(file_name)

        elif file_name in ["package-lock.json", "yarn.lock"]:
            if '"version":' in content:
                print(f"✅ Dependencies are locked in {file_name}")
            else:
                print(f"❌ Dependencies in {file_name} do not appear to be locked.")
                all_dependencies_locked = False
                non_compliant_files.append(file_name)

        elif file_name == "go.sum":
            if any(line.strip() for line in content.splitlines()):
                print(f"✅ Dependencies are locked in {file_name}")
            else:
                print(f"❌ Dependencies in {file_name} do not appear to be locked.")
                all_dependencies_locked = False
                non_compliant_files.append(file_name)

    # Construct the message based on the findings
    if all_dependencies_locked:
        message = (
            "✅ All external dependencies used in the build process are locked.\n"
            "The project complies with the requirement to lock all dependencies, ensuring the build is reproducible and secure."
        )
        return 5, message
    else:
        non_compliant_list = "\n".join(non_compliant_files)
        message = (
            f"❌ Some external dependencies are not locked in the following files:\n{non_compliant_list}\n\n"
            "Remediation steps:\n"
            "- Ensure that all dependency files (Gemfile.lock, package-lock.json, yarn.lock, go.sum, etc.) are updated and contain locked versions of dependencies.\n"
            "- Review your package manager documentation to lock dependencies correctly and ensure a consistent build environment."
        )
        return 3, message


def check_2_4_3_dependency_validation(approval_data):
    """
    Check if pipelines are using dependency scanning by inspecting approval data.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        tuple: (Compliance score (int), message (str))
               Score will be 5 if dependency scanning tools are enabled, 0 otherwise.
               Message will describe the compliance status and relevant findings.
    """
    # Define the name of the dependency scanning tool
    dependency_scanning_tool = "dependency_scanning"

    if not approval_data:
        message = (
            "❌ No approval data found. Unable to verify if dependency scanning is in place."
            "\nPlease ensure that dependency scanning is configured to catch potential vulnerabilities in your dependencies."
        )
        return None, message

    dependency_scanning_found = False

    # Check if any of the approval rules include dependency scanning in the 'scanners' field
    for rule in approval_data.get("rules", []):
        scanners = rule.get("scanners", [])
        if dependency_scanning_tool in scanners:
            dependency_scanning_found = True

    if dependency_scanning_found:
        message = (
            "✅ Compliant: Dependency scanning is enabled in the approval settings."
            "\nThis ensures that your dependencies are automatically checked for known vulnerabilities."
        )
        return 5, message  # Full compliance
    else:
        message = (
            "❌ Non-compliant: No dependency scanning tools found in the approval rules."
            "\nTo achieve compliance, enable dependency scanning in your pipeline approval settings."
        )
        return 0, message  # Non-compliance


def check_2_4_4_reproducible_artifacts(pipeline_ids, job_artifacts):
    """
    Check if build pipelines create reproducible artifacts.

    Args:
        pipeline_ids (list): List of pipeline IDs to compare artifacts.
        job_artifacts (dict): Dictionary containing artifacts for each pipeline job.

    Returns:
        tuple: (int, message) Compliance score and a message describing the findings.
    """
    if not pipeline_ids or not job_artifacts:
        return 0, "❌ Missing pipeline IDs or job artifacts. Unable to verify reproducibility."

    artifact_data = {}
    message_lines = []

    # Fetch artifact details for each pipeline
    for pipeline_id in pipeline_ids:
        artifacts = job_artifacts.get(pipeline_id, [])
        if artifacts:
            artifact_data[pipeline_id] = artifacts
            message_lines.append(f"✅ Artifacts found for pipeline {pipeline_id}.")
        else:
            message_lines.append(f"❌ No artifacts found for pipeline {pipeline_id}.")
            continue  # Skip pipelines without artifacts

    if not artifact_data:
        return None, "❌ No artifacts found for any pipelines. Reproducibility cannot be verified."

    # Compare artifacts from different pipeline runs
    first_pipeline_id = pipeline_ids[0]
    first_pipeline_artifacts = artifact_data.get(first_pipeline_id, [])

    for pipeline_id, artifacts in artifact_data.items():
        if pipeline_id == first_pipeline_id:
            continue  # Skip comparison for the first pipeline (it's our baseline)

        # Use a more robust comparison (e.g., hash comparison)
        if set(map(str, first_pipeline_artifacts)) != set(map(str, artifacts)):
            message_lines.append(
                f"❌ Artifacts are not reproducible between pipelines {first_pipeline_id} and {pipeline_id}."
            )
            return 2, "\n".join(message_lines)  # Non-compliance if artifacts differ

    # If all pipelines have matching artifacts
    message_lines.append("✅ All pipelines produce the same reproducible artifacts.")
    return 5, "\n".join(message_lines)  # Full compliance if all artifacts are reproducible


def check_2_4_5_sbom_generation(sbom_data):
    """
    Check if the pipeline generates an SBOM (Software Bill of Materials) during its run.

    Args:
        sbom_data (list): List of boolean values indicating if an SBOM was generated in each job.

    Returns:
        tuple: (int, message) Compliance score (5 if SBOM generation is detected, 0 otherwise) and a detailed message.
    """
    if any(sbom_data):
        message = "✅ SBOM generation detected in the pipeline for one or more jobs."
        return 5, message  # Full compliance
    else:
        message = (
            "❌ No SBOM generation detected in any job of the pipeline.\n"
            "Remediation steps:\n"
            "- Ensure that the pipeline is configured to generate an SBOM (Software Bill of Materials) during the build process.\n"
            "- Review the CI/CD configuration to enable SBOM generation using available tools."
        )
        return 0, message


def check_2_4_6_sbom_signature(sbom_data):
    """
    Manual check if the pipeline-generated SBOMs are signed.

    Args:
        sbom_data (list): List of boolean values indicating if an SBOM was generated in each job.

    Returns:
        tuple: (int, message) Compliance score (None as it’s a manual check, with a message for manual inspection).
    """
    manual_check_message = (
        "\nManual Check Required:\n"
        "1. Verify that each generated SBOM in the pipeline has a corresponding signature file.\n"
        "2. Confirm that each SBOM signature originates from a trusted and verified source.\n"
        "3. If signatures are missing, update the pipeline to sign the SBOM upon generation."
    )

    if any(sbom_data):
        message = (
            "🔍 SBOM generation detected. Please proceed with the manual check to verify signatures.\n"
            f"{manual_check_message}"
        )
        return None, message  # Manual check required
    else:
        message = (
            "❌ No SBOM generation detected in the pipeline. Unable to verify signatures."
            f"{manual_check_message}"
        )
        return 0, message 


"""Runs every check"""


async def run_build_pipeline_checks(
    pipeline_jobs,
    job_logs,
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
    ci_files,
    ci_variables,
    protected_environments,
    approvals,
):
    """
    Runs all the build pipeline-related compliance checks.

    Args:
        pipeline_jobs (list): List of pipeline jobs.
        job_logs (list): List of job logs.
        project_id (int): GitLab project ID.
        token (str): GitLab access token.
        environments (list): List of project environments.
        members (list): List of project members.
        gitlab_config (str): GitLab CI config content.
        webhooks (list): List of project webhooks.
        runners (list): List of GitLab runners.
        commit_history (list): Commit history for the project.
        approval_data (list): Approval rules data for the project.
        artifacts (list): List of pipeline artifacts.
        dependency_files (list): List of dependency files.
        job_artifacts (list): List of job artifacts.
        pipeline_ids (list): List of pipeline IDs.

    Returns:
        dict: A dictionary of check results.
    """

    ### False = Automated, True = Manual, and Manual sometimes

    checks = [
        (check_2_1_1_pipeline_responsibility, [pipeline_jobs], True),  # Manual
        (check_2_1_2_immutable_infrastructure, [ci_files], True),
        (
            check_2_1_3_build_environment_logging,
            [],
            True,
        ),
        (check_2_1_4_automated_build_environment, [environments], False),  # Automated
        (
            check_2_1_5_limited_access_to_build_environments,
            [members],
            False,
        ),  # Automated
        (check_2_1_6_authenticated_build_access, [members], False),  # Automated
        (check_2_1_7_minimal_secrets_scope, [ci_variables], False),  # Automated
        (check_2_1_8_scan_build_infrastructure, [], True),  # Manual
        (check_2_1_9_default_passwords, [], True),  # Manual
        (check_2_1_10_secured_webhooks, [webhooks], False),  # Automated
        (check_2_1_11_minimum_administrators, [members], True),  # Automated
        (check_2_2_1_single_used_build_workers, [pipeline_jobs], False),  
        (
            check_2_2_2_passed_not_pulled_environment,
            [],
            True,
        ),
        (check_2_2_3_segregated_duties, [], True),  # Manual
        (check_2_2_4_minimal_network_connectivity, [], True),  # Manual
        (check_2_2_5_runtime_security, [], True),  # Manual
        (
            check_2_2_6_automatic_vulnerability_scan_manual,
            [approval_data],
            True,
        ),  # Manual
        (check_2_2_7_version_control_for_deployment_configuration, [], True),  # Manual
        (check_2_2_8_resource_consumption_metrics, [runners], True),
        (check_2_3_1_build_steps_as_code, [gitlab_config], False),  
        (check_2_3_2_build_stage_io, [], False),  
        (check_2_3_3_separate_storage_for_artifacts, [], True),
        (
            check_2_3_4_pipeline_files_tracked_and_reviewed,
            [commit_history],
            False,
        ),  # Automated
        (check_2_3_5_minimize_trigger_access, [protected_environments], True),  # Automated
        (check_2_3_6_pipeline_scanning, [approval_data], True),  # Automated
        (check_2_3_7_vulnerability_scanning, [approval_data], True),  # Automated
        (check_2_3_8_secret_scanner, [approval_data], False),  # Automated
        (check_2_4_1_artifacts_signed, [artifacts], False),  # Automated
        (check_2_4_2_locked_dependencies, [dependency_files], False),  # Automated
        (check_2_4_3_dependency_validation, [approval_data], False),  # Automated
        (
            check_2_4_4_reproducible_artifacts,
            [pipeline_ids, job_artifacts],
            False,
        ),  # Automated
        (check_2_4_5_sbom_generation, [job_logs], False),  # Automated
        (check_2_4_6_sbom_signature, [job_logs], True),  
    ]
    return run_checks(checks, context_name="Build Pipeline Compliance")
