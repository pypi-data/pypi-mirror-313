from concurrent.futures import ThreadPoolExecutor
from services.common_utils import run_checks
from services.gitlab_service import check_package_age
import requests
import json
import re


# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()


"""3.1.X THIRD-PARTY PACKAGES"""


def check_3_1_1_third_party_verification():
    """
    Check if third-party artifacts and open-source libraries are verified.

    Args:
        dependency_files (dict): A dictionary containing the content of dependency files.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. For each third-party artifact and open-source library, ensure you have verified it using checksum comparisons (e.g., SHA256, MD5).\n"
        "2. Verify against trusted sources to ensure the integrity and authenticity of these components.\n"
        "3. Consider using tools such as 'snyk', 'npm audit', or 'OWASP Dependency-Check' to further validate dependencies.\n"
        "4. Make sure these tools are configured in your CI/CD pipeline to continuously monitor for vulnerabilities."
    )

    return (
        None,
        manual_check_message,
    )


def check_3_1_2_third_party_sbom():
    """
    Check if a Software Bill of Materials (SBOM) is required from all third-party suppliers.

    Args:
        job_artifacts (dict): A dictionary containing the artifacts from each pipeline job.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Ensure that every third-party dependency in use has an accompanying SBOM file.\n"
        "2. Verify that your suppliers provide SBOM files with their components, detailing all dependencies used.\n"
        "3. Check the pipeline job artifacts and logs to ensure that an SBOM was included.\n"
        "4. Validate that the SBOM is kept up-to-date for any updates or changes from third-party suppliers."
    )

    return (
        None,
        manual_check_message,
    )


def check_3_1_3_signed_metadata():
    """
    Check if the build process metadata is signed and verified for all artifacts.

    Args:
        job_artifacts (dict): A dictionary containing artifacts for each pipeline job.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. For each artifact used, verify that it was supplied with verified and signed metadata of its build process.\n"
        "2. Ensure that the signature is an organizational signature that is verifiable by common Certificate Authority servers.\n"
        "3. Review the build logs and metadata files to check for any tampering or unsigned metadata."
    )

    return (
        None,
        manual_check_message,
    )


def check_3_1_4_dependency_monitoring(approval_data):
    """
    Check if Dependency Scanning and Container Scanning are enabled in the pipeline.

    Args:
        approval_data (list): List of approval rules fetched from GitLab.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Navigate to the GitLab repository's main page.\n"
        "2. Review the CI pipeline configuration to verify that Dependency Scanning and Container Scanning are enabled.\n"
        "3. If not already configured, enable these scanning tools to monitor vulnerabilities in dependencies and container images."
    )

    if not approval_data:
        return (
            None,
            0,
            f"❌ No approval data found. Unable to verify if dependency and container scanning is enabled. {manual_check_message}",
        )

    dependency_scanning_found = False
    container_scanning_found = False

    # Check the approval data for indicators of dependency scanning or container scanning
    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "dependency_scanning" in scanners:
            dependency_scanning_found = True
            print(
                f"✅ Dependency Scanning is enabled in the approval settings with rule: {rule['name']}"
            )
        if "container_scanning" in scanners:
            container_scanning_found = True
            print(
                f"✅ Container Scanning is enabled in the approval settings with rule: {rule['name']}"
            )

    if dependency_scanning_found and container_scanning_found:
        return (
            5,
            "✅ Both Dependency Scanning and Container Scanning are enabled in the pipeline.",
        )
    else:
        missing_scans = []
        if not dependency_scanning_found:
            missing_scans.append("Dependency Scanning")
        if not container_scanning_found:
            missing_scans.append("Container Scanning")

        missing_scans_str = ", ".join(missing_scans)
        return (
            0,
            f"❌ The following scans are not enabled: {missing_scans_str}. {manual_check_message}",
        )


def check_3_1_5_trusted_package_managers(dependency_files):
    """
    Check if the package managers and repositories used in the project are from trusted sources.

    Args:
        dependency_files (dict): A dictionary containing the content of package manager configuration files.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    trusted_registries = [
        "https://registry.npmjs.org",  # NPM
        "https://yarnpkg.com",  # Yarn
        "https://pypi.org/simple",  # PyPI
        "https://repo.maven.apache.org/maven2",  # Maven Central
        "https://packagist.org",  # Composer
    ]

    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Review the project's package manager configuration files (e.g., package.json, yarn.lock, Pipfile, pom.xml, composer.json).\n"
        "2. Ensure that any external repositories are trusted and that no unverified or potentially harmful sources are listed.\n"
        "3. If any custom registries are used, verify that they are secure and managed by a trusted entity."
    )

    if not dependency_files:
        return (
            None,
            f"❌ No package manager configuration files found. {manual_check_message}",
        )

    untrusted_found = False
    untrusted_registries = {}

    # Regex pattern to find URLs in the file
    url_pattern = re.compile(r"(https?://[^\s]+)")

    for file_name, content in dependency_files.items():
        file_untrusted = []
        for line in content.splitlines():
            # Skip comment lines, empty lines, and metadata lines
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            # Search for URLs in the line and check if they are trusted
            match = url_pattern.search(line)
            if match:
                url = match.group(0)
                if not any(
                    trusted_registry in url for trusted_registry in trusted_registries
                ):
                    file_untrusted.append(url)

        if file_untrusted:
            untrusted_registries[file_name] = file_untrusted
            untrusted_found = True

    if untrusted_found:
        untrusted_details = "\n".join(
            f"File: {file_name} - Untrusted Registries: {', '.join(file_untrusted)}"
            for file_name, file_untrusted in untrusted_registries.items()
        )
        return (
            0,
            f"❌ Untrusted or unknown registries detected in the following files:\n{untrusted_details}\n{manual_check_message}",
        )
    else:
        return 5, "✅ All package managers and registries are trusted."


def check_3_1_6_signed_sbom():
    """
    Check if the project dependencies have a signed Software Bill of Materials (SBOM).

    Args:
        artifacts (list): List of artifacts containing SBOM information from the pipeline.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Ensure that every third-party dependency in use has an accompanying SBOM file.\n"
        "2. Verify that your suppliers provide SBOM files with their components, detailing all dependencies used.\n"
        "3. Check the pipeline job artifacts and logs to ensure that an SBOM was included.\n"
        "4. Validate that the SBOM is kept up-to-date for any updates or changes from third-party suppliers."
    )

    return (
        None,
        manual_check_message,
    )


def check_3_1_7_pinned_dependencies(dependency_files):
    """
    Check if all dependencies are pinned to a specific version and do not use wildcard or "latest" versions.

    Args:
        dependency_files (dict): A dictionary containing the content of dependency files (Gemfile.lock, package-lock.json, yarn.lock, go.sum).

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    problematic_patterns = ["latest", "*", "x", ">=<", "~", "^"]
    unpinned_dependencies = []

    for file_name, content in dependency_files.items():
        for line in content.splitlines():
            if any(pattern in line for pattern in problematic_patterns):
                unpinned_dependencies.append((file_name, line))

    if unpinned_dependencies:
        details = "\n".join(
            f"In file {file_name}: {line}" for file_name, line in unpinned_dependencies
        )
        return (
            0,
            f"❌ Some dependencies are not pinned to a specific version:\n{details}",
        )
    else:
        return 5, "✅ All dependencies are pinned to specific versions."


def check_3_1_8_package_age(dependency_files):
    """
    Check if all packages used are more than 60 days old.

    Args:
        dependency_files (dict): Dictionary containing package files like package.json or requirements.txt.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    non_compliant_packages = []

    # Example for checking package-lock.json (NPM)
    if "package-lock.json" in dependency_files:
        package_lock_data = json.loads(dependency_files["package-lock.json"])
        dependencies = package_lock_data.get("dependencies", {})
        for package_name in dependencies.keys():
            if not check_package_age(package_name, registry="npm"):
                non_compliant_packages.append(package_name)

    # Example for checking requirements.txt (PyPI)
    if "requirements.txt" in dependency_files:
        for line in dependency_files["requirements.txt"].splitlines():
            package_name = line.split("==")[0].strip()
            if package_name and not check_package_age(package_name, registry="pypi"):
                non_compliant_packages.append(package_name)

    if non_compliant_packages:
        details = "\n".join(non_compliant_packages)
        return 0, f"❌ The following packages are less than 60 days old:\n{details}"
    else:
        return 5, "✅ All packages used are more than 60 days old."


"""3.2.X VALIDATE PACKAGES"""


def check_3_2_1_dependency_usage_policy(group_push_rules):
    """
    Check if there is an organization-wide policy enforcing dependency usage.

    Args:
        group_push_rules (dict): Group push rules to check for organization-wide enforcement.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. Verify that GitLab push rules include policies such as dependency enforcement.\n"
        "2. Check if rules prevent actions like deleting tags or enforce commit messages."
    )

    if group_push_rules:
        if group_push_rules.get("deny_delete_tag") or group_push_rules.get(
            "commit_message_regex"
        ):
            return (
                5,
                "✅ Organization-wide dependency usage policies are enforced via GitLab push rules.",
            )
        else:
            return (
                None,
                f"❌ No specific organization-wide dependency usage policies found in GitLab push rules. {manual_check_message}",
            )
    else:
        return (
            0,
            f"❌ Unable to find organization-wide dependency usage policies. {manual_check_message}",
        )


def check_3_2_2_package_scanning(approval_data):
    """
    Check if Dependency Scanning is enabled based on approval rules.

    Args:
        approval_data (dict): Dictionary containing approval rules fetched from GitLab.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """

    if not approval_data or "rules" not in approval_data:
        return (
            None,
            "❌ Non-compliant: No approval rules found. Unable to verify if Dependency Scanning is enabled.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        num_scanners = len(scanners)

        if "dependency_scanning" in scanners:
            return (
                5,
                "✅ Compliant: Dependency Scanning is enabled in the approval settings.",
            )

    return (
        0,
        "❌ Non-compliant: Dependency Scanning is not enabled in the approval settings.",
    )


def check_3_2_3_license_scanning(sbom_data):
    """
    Check if License Scanning is enabled by verifying the presence of SBOM data.

    Args:
        sbom_data (list): List indicating if SBOM was generated in each job.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """

    if any(sbom_data):
        message = "✅ Compliant: License Scanning is enabled, as SBOM generation is present in the pipeline."
        return 5, message  # Full compliance
    else:
        message = (
            "❌ Non-compliant: No SBOM generation detected, which is required for License Scanning.\n"
            "Remediation steps:\n"
            "- Configure the pipeline to generate an SBOM (Software Bill of Materials) to enable License Scanning.\n"
            "- Ensure the `.gitlab-ci.yml` includes SBOM generation, as License Scanning relies on it."
        )
        return 0, message  # Non-compliance


"""Runs every check"""


async def run_dependency_checks(
    dependency_files,
    job_artifacts,
    approval_data,
    sbom_artifacts,
    group_push_rules,
    gitlab_ci_content,
    security_scan_data,
    license_scan_data,
):
    """Run all the checks defined in this file."""
    total_score = 0
    results = {}

    ### False = Automated, True = Manual, and Manual sometimes

    checks = [
        (check_3_1_1_third_party_verification, [], True),  # Manual
        (check_3_1_2_third_party_sbom, [], True),  # Manual
        (check_3_1_3_signed_metadata, [], True),  # Manual
        (check_3_1_4_dependency_monitoring, [approval_data], False),  # Automated
        (check_3_1_5_trusted_package_managers, [dependency_files], False),  # Automated
        (check_3_1_6_signed_sbom, [], True),  # Automated
        (check_3_1_7_pinned_dependencies, [dependency_files], False),  # Automated
        (check_3_1_8_package_age, [dependency_files], False),  # Automated
        (check_3_2_1_dependency_usage_policy, [group_push_rules], True),  # Manual
        (
            check_3_2_2_package_scanning,
            [approval_data],
            True,
        ),  # Automated
        (
            check_3_2_3_license_scanning,
            [approval_data],
            True,
        ),  # Automated
    ]

    return run_checks(checks, context_name="Dependency Compliance")
