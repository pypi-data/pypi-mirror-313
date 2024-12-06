from concurrent.futures import ThreadPoolExecutor
from services.common_utils import run_checks
import yaml

# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()


"""5.1.X DEPLOYMENT CONFIG"""


def check_5_1_1_deployment_config_separation_manual():
    """
    Manual check to ensure deployment configuration files are separated from source code.

    Returns:
        tuple: A tuple containing the compliance score (0 since it's a manual check) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Required:\n"
        "1. Review your GitLab repositories and ensure that deployment configuration files (e.g., docker-compose.yml, kubernetes.yml, deployment.yml) "
        "are stored in a dedicated repository separate from the source code repository.\n"
        "2. Deployment configuration files should be isolated from application source code for better maintainability and security."
    )

    return None, f"⚠️ This check requires manual verification. {manual_check_message}"


def check_5_1_2_deployment_config_audit(deployment_files):
    """
    Check if deployment configuration changes are audited and tracked by verifying the presence of deployment files via GitLab API.

    Args:
        project_id (str): The ID of the GitLab project.
        private_token (str): The GitLab personal access token.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """

    if deployment_files:
        message = (
            f"✅ Deployment configuration files are found and changes can be audited and tracked.\n"
            f"Files found:\n"
            + "\n".join(deployment_files)
            + "\n\nEnsure that all changes to these files are reviewed, documented, and tracked with appropriate commit messages."
        )
        return 5, message  # Full compliance if deployment files are found
    else:
        message = (
            "❌ No deployment configuration files were found. "
            "Manual check required to ensure deployment changes are audited and tracked.\n"
            "Steps:\n"
            "1. Go to the GitLab project and review the commit history for important files such as `.gitlab-ci.yml`, Dockerfiles, Terraform files, etc.\n"
            "2. Ensure that every change is documented, reviewed, and includes appropriate commit messages.\n"
            "3. Consider enabling GitLab's audit logs (if using Premium or self-hosted) to ensure changes are logged properly."
        )
        return 0, message  # Non-compliance if no deployment files are found


def check_5_1_3_sensitive_data_scanner(approval_data):
    """
    Check if scanners (such as Secret Detection) are enabled to prevent sensitive data exposure in deployment configuration files.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        tuple: Compliance score (5 if scanners are enabled, 0 otherwise) and a detailed message.
    """
    sensitive_data_scanners = [
        "secret_detection",
        "sast",
        "dast",
        "container_scanning",
        "dependency_scanning",
        "coverage_fuzzing",
        "api_fuzzing",
    ]

    if not approval_data:
        message = (
            "❌ No approval data found. Unable to verify if sensitive data scanners are in place.\n"
            "Ensure that scanners like GitLab's Secret Detection are enabled to prevent the exposure of sensitive data."
        )
        return 0, message

    scanner_found = False

    # Check if any of the approval rules contain sensitive data scanners
    for rule in approval_data["rules"]:
        if isinstance(rule, dict) and "scanners" in rule:
            # Check if any of the defined scanners are present in the rule's scanners field
            if any(scanner in rule["scanners"] for scanner in sensitive_data_scanners):
                scanner_found = True
                print(f"✅ Scanners found in rule: {rule['name']}")

    if scanner_found:
        message = "✅ Sensitive data scanners are enabled to prevent exposure of sensitive data in deployment configuration files."
        return 5, message  # Full compliance if scanners are found
    else:
        message = (
            "❌ No sensitive data scanners found in the approval rules. "
            "Ensure that tools like GitLab's Secret Detection are enabled to prevent sensitive data exposure."
        )
        return 0, message  # Non-compliance if no scanners are found


def check_5_1_4_limit_access_to_deployment_config_manual():
    """
    Manual check to ensure only trusted and qualified users have access to deployment configurations.

    Returns:
        int: Always return 0 because this check is manual.
    """
    message = (
        "Manual Check: Ensure that only trusted and qualified users (e.g., Maintainers, Owners) "
        "have access to deployment configuration files. Review the access levels in the GitLab "
        "project settings and limit access accordingly."
    )
    return None, f"⚠️ This check requires manual verification. {message}"


def check_5_1_5_scan_iac(approval_data):
    """
    Check if Infrastructure as Code (IaC) scanning tools are enabled for the project.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    # Define common IaC scanning tools
    iac_scanning_tools = ["TFSec", "Checkov", "TerraScan", "Open Policy Agent (OPA)"]

    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Ensure that IaC scanning tools like TFSec, Checkov, or similar tools are integrated "
        "into your GitLab pipeline to scan Terraform and other Infrastructure as Code files.\n"
        "2. Verify that the pipeline's security jobs are configured to scan for misconfigurations in IaC files."
    )

    if not approval_data:
        return (
            None,
            f"❌ No approval data found. Unable to verify if IaC scanning is enabled. {manual_check_message}",
        )

    iac_scanning_found = False

    # Check the approval data for indicators of IaC scanning tools
    for rule in approval_data:
        if isinstance(rule, dict) and "name" in rule:
            rule_name = rule["name"].lower()
            if any(tool.lower() in rule_name for tool in iac_scanning_tools):
                iac_scanning_found = True
                print(
                    f"✅ IaC Scanning tool '{rule['name']}' is enabled in the approval settings."
                )

    if iac_scanning_found:
        return (
            5,
            "✅ Infrastructure as Code (IaC) scanning tools are enabled in the pipeline.",
        )
    else:
        return (
            0,
            f"❌ No IaC scanning tools found in the pipeline job artifacts or approval data. {manual_check_message}",
        )


def check_5_1_6_deployment_manifest_verification():
    """
    Manual check for deployment configuration manifests verification.

    Returns:
        tuple: A tuple containing a reminder to manually verify deployment manifests.
    """
    message = (
        "Manual Check: Verify that the deployment configuration manifests in use have been verified.\n"
        "1. For each manifest file in the project, calculate its checksum (e.g., SHA256) and compare it with a trusted source.\n"
        "2. If the checksum differs, investigate for potential tampering.\n"
        "3. Make sure this verification is documented and performed before deploying to production."
    )
    return None, message


"""5.2.X DEPLOYMENT ENVIRONMENT"""


def check_5_2_1_automated_deployments(gitlab_ci_content):
    """
    Check if the deployment process is automated by inspecting the .gitlab-ci.yml file.

    Args:
        gitlab_ci_content (str): Content of the .gitlab-ci.yml file.

    Returns:
        tuple: Compliance score (int) and a message (str).
    """
    if not gitlab_ci_content:
        return (
            None,
            "❌ No .gitlab-ci.yml file found. Unable to verify if deployments are automated.",
        )

    try:
        # Load the GitLab CI configuration
        gitlab_ci_config = yaml.safe_load(gitlab_ci_content)
    except yaml.YAMLError as e:
        return 0, f"❌ Error parsing .gitlab-ci.yml file: {e}"

    deployment_jobs_found = False
    deployment_keywords = ["deploy", "production", "environment", "release"]

    # Iterate through the jobs defined in the CI configuration
    for job_name, job_config in gitlab_ci_config.items():
        if isinstance(job_config, dict):
            # Check if the job name or stage includes deployment-related keywords
            if any(
                keyword in job_name.lower() for keyword in deployment_keywords
            ) or any(
                keyword in job_config.get("stage", "").lower()
                for keyword in deployment_keywords
            ):
                deployment_jobs_found = True
                print(f"✅ Automated deployment job found: {job_name}")

    if deployment_jobs_found:
        return 5, "✅ Deployment process is automated as per the CI/CD pipeline."
    else:
        return (
            0,
            "❌ No automated deployment jobs found in the CI/CD pipeline. Please ensure the deployment process is automated.",
        )


def check_5_2_2_reproducible_deployment():
    """
    Manual check for ensuring the deployment environment is reproducible.

    Returns:
        tuple: Compliance score (int) and a reminder message (str).
    """
    message = (
        "Manual Check: Ensure the deployment environment is reproducible.\n"
        "1. Verify that the deployment process generates the same artifacts and environment consistently.\n"
        "2. Ensure that the configuration and input to the deployment process remain unchanged between deployments.\n"
        "3. Review the CI/CD pipeline for any changes in the environment or deployment scripts."
    )
    return None, message


def check_5_2_3_production_environment_access():
    """
    Manual check to ensure that access to the production environment is limited to trusted and qualified users.

    Returns:
        tuple: Compliance score (int) and a reminder message (str).
    """
    message = (
        "Manual Check Reminder: Verify that access to the production environment is limited to trusted and qualified users.\n"
        "Steps:\n"
        "1. Review the list of users who have access to the production environment.\n"
        "2. Ensure that only users with appropriate roles (e.g., Maintainers, Owners) have access.\n"
        "3. Remove or limit access for any users who should not have access to production environments."
    )
    return None, message


"""Runs every check"""


async def run_deployment_checks(
    approval_data,
    gitlab_ci_content,
    deployment_files,
):
    """Run all the checks defined in this file."""

    # Define your checks (manual and automated) here
    checks = [
        (check_5_1_1_deployment_config_separation_manual, [], True),  # Manual check
        (check_5_1_2_deployment_config_audit, [deployment_files], False),
        (check_5_1_3_sensitive_data_scanner, [approval_data], False),
        (check_5_1_4_limit_access_to_deployment_config_manual, [], True),
        (check_5_1_5_scan_iac, [approval_data], False),
        (check_5_1_6_deployment_manifest_verification, [], True),
        (check_5_2_1_automated_deployments, [gitlab_ci_content], False),
        (check_5_2_2_reproducible_deployment, [], True),
        (check_5_2_3_production_environment_access, [], True),
    ]

    # Use the reusable function to run the checks
    results = run_checks(checks, context_name="deployments")

    # Return the results, you no longer need to expect total_score and total_possible_score
    return results
