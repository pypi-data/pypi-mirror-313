from concurrent.futures import ThreadPoolExecutor
from services.gitlab_service import check_package_age


# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()


"""3.1.X THIRD-PARTY PACKAGES"""


def check_3_1_1_third_party_verification(dependency_files):
    """
    Check if third-party artifacts and open-source libraries are verified.

    Args:
        dependency_files (dict): A dictionary containing the content of dependency files.

    Returns:
        tuple: A tuple containing the compliance score (int) and a message (str).
    """
    verification_tools = ["Checksum Verification", "SHA256", "MD5"]
    manual_check_message = (
        "\nManual Check Reminder:\n"
        "1. For each third-party artifact and open-source library, ensure you have verified it using checksum comparisons (e.g., SHA256, MD5).\n"
        "2. Verify against trusted sources to ensure the integrity and authenticity of these components.\n"
        "3. Consider using tools such as 'snyk', 'npm audit', or 'OWASP Dependency-Check' to further validate dependencies.\n"
        "4. Make sure these tools are configured in your CI/CD pipeline to continuously monitor for vulnerabilities."
    )

    if not dependency_files:
        return (
            0,
            f"❌ No dependency files found. Unable to verify third-party artifacts and libraries. {manual_check_message}",
        )

    verification_found = False

    # Check if any dependencies have checksums or verification in place
    for file_name, content in dependency_files.items():
        if "checksum" in content or any(
            tool.lower() in content.lower() for tool in verification_tools
        ):
            verification_found = True
            print(f"✅ Verification details found in {file_name}.")
        else:
            print(f"❌ No verification details found in {file_name}.")

    if verification_found:
        return 5, "✅ Third-party artifacts and libraries are verified."
    else:
        return (
            0,
            f"❌ No verification details found for third-party artifacts and libraries. {manual_check_message}",
        )


def check_3_1_2_third_party_sbom(job_artifacts):
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

    if not job_artifacts:
        return (
            0,
            f"❌ No job artifacts found to verify if SBOMs are provided by third-party suppliers. {manual_check_message}",
        )

    sbom_found = False

    # Check if any artifacts contain SBOM data or files
    for pipeline_id, artifacts in job_artifacts.items():
        if artifacts is None:
            print(f"No artifacts found for pipeline {pipeline_id}")
            continue

        for artifact in artifacts:
            # Check if artifact is a dictionary
            if not isinstance(artifact, dict):
                print(
                    f"Skipping invalid artifact entry in pipeline {pipeline_id}: {artifact}"
                )
                continue

            # Check for common SBOM file names or indicators
            filename = artifact.get("filename", "").lower()
            if (
                filename.endswith((".spdx", ".json", ".xml", ".bom"))
                or "sbom" in filename
            ):
                print(
                    f"✅ SBOM found for pipeline {pipeline_id}: {artifact['filename']}"
                )
                sbom_found = True

    if sbom_found:
        return 5, "✅ SBOMs were found from third-party suppliers for the pipeline."
    else:
        return (
            0,
            f"❌ No SBOM files found in the pipeline job artifacts from third-party suppliers. {manual_check_message}",
        )


def check_3_1_3_signed_metadata(job_artifacts):
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

    if not job_artifacts:
        return (
            0,
            f"❌ No job artifacts found to verify signed metadata. {manual_check_message}",
        )

    signed_metadata_found = False

    # Iterate through artifacts to check for signature files
    for pipeline_id, artifacts in job_artifacts.items():
        if artifacts is None:
            print(f"No artifacts found for pipeline {pipeline_id}")
            continue

        for artifact in artifacts:
            # Check if artifact is a dictionary
            if not isinstance(artifact, dict):
                print(
                    f"Skipping invalid artifact entry in pipeline {pipeline_id}: {artifact}"
                )
                continue

            # Check if there's a signature file or signed metadata
            filename = artifact.get("filename", "").lower()
            if "signature.asc" in filename or ".sig" in filename:
                print(
                    f"✅ Signed metadata found for pipeline {pipeline_id}: {artifact['filename']}"
                )
                signed_metadata_found = True

    if signed_metadata_found:
        return 5, "✅ Signed metadata was found for the build process."
    else:
        return (
            0,
            f"❌ No signed metadata found for the build process artifacts. {manual_check_message}",
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
            0,
            f"❌ No approval data found. Unable to verify if dependency and container scanning is enabled. {manual_check_message}",
        )

    dependency_scanning_found = False
    container_scanning_found = False

    # Check the approval data for indicators of dependency scanning or container scanning
    for rule in approval_data:
        if isinstance(rule, dict) and "name" in rule:
            rule_name = rule["name"].lower()
            if "dependency scanning" in rule_name:
                dependency_scanning_found = True
                print(
                    f"✅ Dependency Scanning is enabled in the approval settings with rule: {rule['name']}"
                )
            if "container scanning" in rule_name:
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
        int: Compliance score (5 if all package managers/repositories are trusted, 0 otherwise).
    """
    # Define known trusted registries
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
        print(
            f"❌ No package manager configuration files found. {manual_check_message}"
        )
        return 0

    untrusted_found = False

    # Check for each dependency file
    for file_name, content in dependency_files.items():
        print(f"Checking {file_name} for trusted package registries...")

        if any(trusted_registry in content for trusted_registry in trusted_registries):
            print(f"✅ Trusted registries found in {file_name}.")
        else:
            print(
                f"⚠️ No known trusted registries detected in {file_name}. Please verify the registries manually."
            )
            untrusted_found = True

    if untrusted_found:
        print(
            f"❌ Potential untrusted package registries detected. {manual_check_message}"
        )
        return 0  # Non-compliance if any untrusted registries are detected
    else:
        print("✅ All package registries appear to be trusted.")
        return 5  # Full compliance if all registries are trusted


def check_3_1_6_signed_sbom(artifacts):
    """
    Check if the project dependencies have a signed Software Bill of Materials (SBOM).

    Args:
        artifacts (list): List of artifacts containing SBOM information from the pipeline.

    Returns:
        int: Compliance score (5 if signed SBOMs are found for all dependencies, 0 otherwise).
    """
    if not artifacts:
        print("No artifacts found. Unable to verify SBOM signatures.")
        return 0  # Non-compliance if no artifacts are found

    unsigned_sboms = []

    # Check each artifact for SBOM files and their signatures
    for artifact in artifacts:
        sbom_signed = False
        if isinstance(artifact, dict):
            # Assuming each artifact has fields 'file_name' and 'is_signed' to indicate if it's an SBOM and its signature
            if artifact.get("file_name", "").endswith(".sbom.json"):
                if artifact.get("is_signed", False):
                    print(f"✅ Signed SBOM found for: {artifact['file_name']}")
                    sbom_signed = True
                else:
                    print(f"❌ Unsigned SBOM detected for: {artifact['file_name']}")
                    unsigned_sboms.append(artifact["file_name"])

        if not sbom_signed:
            print(
                f"Manual Check Required: Ensure the SBOM for {artifact.get('file_name', 'unknown')} is signed."
            )

    if unsigned_sboms:
        print(f"❌ The following SBOMs are not signed: {unsigned_sboms}")
        return 0  # Non-compliance if any unsigned SBOMs are found
    else:
        print("✅ All SBOMs are verified and signed.")
        return 5  # Full compliance score


def check_3_1_6_signed_sbom(artifacts):
    """
    Check if the project dependencies have a signed Software Bill of Materials (SBOM).

    Args:
        artifacts (list): List of artifacts containing SBOM information from the pipeline.

    Returns:
        int: Compliance score (5 if signed SBOMs are found for all dependencies, 0 otherwise).
    """
    if not artifacts:
        print("No artifacts found. Unable to verify SBOM signatures.")
        return 0  # Non-compliance if no artifacts are found

    unsigned_sboms = []

    # Check each artifact for SBOM files and their signatures
    for artifact in artifacts:
        sbom_signed = False
        if isinstance(artifact, dict):
            # Assuming each artifact has fields 'file_name' and 'is_signed' to indicate if it's an SBOM and its signature
            if artifact.get("file_name", "").endswith(".sbom.json"):
                if artifact.get("is_signed", False):
                    print(f"✅ Signed SBOM found for: {artifact['file_name']}")
                    sbom_signed = True
                else:
                    print(f"❌ Unsigned SBOM detected for: {artifact['file_name']}")
                    unsigned_sboms.append(artifact["file_name"])

        if not sbom_signed:
            print(
                f"Manual Check Required: Ensure the SBOM for {artifact.get('file_name', 'unknown')} is signed."
            )

    if unsigned_sboms:
        print(f"❌ The following SBOMs are not signed: {unsigned_sboms}")
        return 0  # Non-compliance if any unsigned SBOMs are found
    else:
        print("✅ All SBOMs are verified and signed.")
        return 5  # Full compliance score


def check_3_1_7_pinned_dependencies(dependency_files):
    """
    Check if all dependencies are pinned to a specific version and do not use wildcard or "latest" versions.

    Args:
        dependency_files (dict): A dictionary containing the content of dependency files (Gemfile.lock, package-lock.json, yarn.lock, go.sum).

    Returns:
        int: Compliance score (5 if all dependencies are pinned to a specific version, 0 otherwise).
    """
    # Patterns to identify unpinned versions
    problematic_patterns = ["latest", "*", "x", ">=<", "~", "^"]
    unpinned_dependencies = []

    for file_name, content in dependency_files.items():
        lines = content.splitlines()
        for line in lines:
            # Checking for unpinned dependency indicators
            if any(pattern in line for pattern in problematic_patterns):
                unpinned_dependencies.append((file_name, line))

    if unpinned_dependencies:
        print(
            "❌ Some dependencies are not pinned to a specific version. Details below:"
        )
        for file_name, line in unpinned_dependencies:
            print(f"In file {file_name}, unpinned dependency found: {line}")
        return 0  # Non-compliance score
    else:
        print("✅ All dependencies are pinned to specific versions.")
        return 5  # Full compliance score


def check_3_1_8_package_age(dependency_files):
    """
    Check if all packages used are more than 60 days old.

    Args:
        dependency_files (dict): Dictionary containing package files like package.json or requirements.txt.

    Returns:
        int: Compliance score (5 if all packages are more than 60 days old, 0 otherwise).
    """
    non_compliant_packages = []

    # Check package-lock.json (NPM)
    if "package-lock.json" in dependency_files:
        package_lock_data = json.loads(dependency_files["package-lock.json"])
        dependencies = package_lock_data.get("dependencies", {})
        for package_name in dependencies.keys():
            if not check_package_age(package_name, registry="npm"):
                non_compliant_packages.append(package_name)

    # Check requirements.txt (PyPI)
    if "requirements.txt" in dependency_files:
        lines = dependency_files["requirements.txt"].splitlines()
        for line in lines:
            package_name = line.split("==")[0].strip()
            if package_name and not check_package_age(package_name, registry="pypi"):
                non_compliant_packages.append(package_name)

    if non_compliant_packages:
        print("❌ The following packages are less than 60 days old:")
        for pkg in non_compliant_packages:
            print(f"- {pkg}")
        return 0  # Non-compliance score
    else:
        print("✅ All packages used are more than 60 days old.")
        return 5  # Full compliance score


"""3.2.X VALIDATE PACKAGES"""


def check_3_2_1_dependency_usage_policy(group_push_rules):
    """
    Check if there is an organization-wide policy enforcing dependency usage.

    Args:
        project_id (int): The GitLab project ID.
        group_id (int): The GitLab group ID to check for organization-wide rules.
        token (str): GitLab private token.

    Returns:
        int: Compliance score (5 if policies are present, 0 otherwise).
    """
    # Check if the group has any push rules that enforce policies
    if group_push_rules:
        # Look for rules that might enforce dependencies, such as preventing large files or enforcing certain file types
        if group_push_rules.get("deny_delete_tag") or group_push_rules.get(
            "commit_message_regex"
        ):
            print(
                "✅ Organization-wide dependency usage policies are enforced via GitLab push rules."
            )
            return 5  # Full compliance score
        else:
            print(
                "❌ No specific organization-wide dependency usage policies found in GitLab push rules."
            )
    else:
        print("❌ Unable to find organization-wide dependency usage policies.")

    # Additional checks can include:
    # 1. Searching for `dependency` keyword in README files
    # 2. Inspecting `CODEOWNERS` file for policy enforcement sections

    return 0  # Non-compliance


def check_3_2_2_package_scanning(gitlab_ci_content, security_scan_data):
    """
    Check if dependency scanning is enabled for the project.

    Args:
        gitlab_ci_content (str): Content of the .gitlab-ci.yml file.
        security_scan_data (dict): Security scan data fetched via API.

    Returns:
        dict: Result of the check.
    """

    if gitlab_ci_content:
        if "dependency_scanning:" in gitlab_ci_content:
            return {
                "check": "3.2.2",
                "result": "✅ Dependency scanning is enabled in the .gitlab-ci.yml file.",
                "details": (
                    "Dependency scanning is correctly configured within your "
                    ".gitlab-ci.yml file. This ensures that all dependencies "
                    "are automatically scanned for known vulnerabilities with each pipeline run."
                ),
            }
        else:
            return {
                "check": "3.2.2",
                "result": "❌ Dependency scanning is not configured in the .gitlab-ci.yml file.",
                "details": (
                    "The .gitlab-ci.yml file does not contain a dependency scanning configuration. "
                    "To ensure your project is protected against known vulnerabilities, add a "
                    "'dependency_scanning:' job configuration in your .gitlab-ci.yml file. "
                    "Refer to the GitLab documentation to properly configure this: "
                    "https://docs.gitlab.com/ee/user/application_security/dependency_scanning/#enable-the-analyzer"
                ),
            }

    # Fallback to manually checking if dependency scanning is enabled via API
    if security_scan_data and security_scan_data.get("dependency_scanning"):
        return {
            "check": "3.2.2",
            "result": "✅ Dependency scanning is enabled for the project.",
            "details": (
                "Dependency scanning is enabled based on the project's security scan settings. "
                "This indicates that dependencies are being scanned for vulnerabilities."
            ),
        }
    else:
        return {
            "check": "3.2.2",
            "result": "❌ Dependency scanning is not enabled for the project.",
            "details": (
                "Dependency scanning is not enabled for this project. Without it, your project is "
                "at risk of using vulnerable dependencies. Consider enabling Dependency Scanning "
                "in your GitLab CI/CD settings or by configuring it in your .gitlab-ci.yml file. "
                "Refer to the GitLab documentation: "
                "https://docs.gitlab.com/ee/user/application_security/dependency_scanning/#enable-the-analyzer"
            ),
        }


def check_3_2_3_license_scanning(gitlab_ci_content, license_scan_data):
    """
    Check if license scanning is enabled for the project.

    Args:
        gitlab_ci_content (str): Content of the .gitlab-ci.yml file.
        license_scan_data (dict): License scan data fetched via API.

    Returns:
        dict: Result of the check.
    """

    if gitlab_ci_content:
        if (
            "license_management:" in gitlab_ci_content
            or "license_scanning:" in gitlab_ci_content
        ):
            return {
                "check": "3.2.3",
                "result": "✅ License scanning is enabled in the .gitlab-ci.yml file.",
                "details": (
                    "License scanning is correctly configured in the .gitlab-ci.yml file. "
                    "This ensures that all dependencies are scanned for potential license violations, "
                    "helping maintain compliance with your organization's policies."
                ),
            }
        else:
            return {
                "check": "3.2.3",
                "result": "❌ License scanning is not configured in the .gitlab-ci.yml file.",
                "details": (
                    "The .gitlab-ci.yml file does not contain a license scanning configuration. "
                    "To prevent legal and compliance issues, add 'license_management:' or 'license_scanning:' "
                    "to your .gitlab-ci.yml file configuration. Refer to GitLab's documentation for setup: "
                    "https://docs.gitlab.com/ee/user/compliance/license_scanning/"
                ),
            }

    if license_scan_data and license_scan_data.get("enabled"):
        return {
            "check": "3.2.3",
            "result": "✅ License scanning is enabled for the project.",
            "details": (
                "License scanning is enabled based on the project's license scan settings. "
                "This ensures that your project is checked for any potential license violations "
                "on all dependencies."
            ),
        }
    else:
        return {
            "check": "3.2.3",
            "result": "❌ License scanning is not enabled for the project.",
            "details": (
                "License scanning is not enabled for this project. This puts your organization at risk "
                "of using software packages that violate licensing agreements. Enable license scanning "
                "in the project settings or configure it in the .gitlab-ci.yml file. For more information, "
                "refer to the documentation: "
                "https://docs.gitlab.com/ee/user/compliance/license_scanning/"
            ),
        }


"""Runs every check"""


async def run_all_checks(
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
    results = {}  # Dictionary to store check results

    checks = [
        (check_3_1_1_third_party_verification, [dependency_files]),
        (check_3_1_2_third_party_sbom, [job_artifacts]),
        (check_3_1_3_signed_metadata, [job_artifacts]),
        (check_3_1_4_dependency_monitoring, [approval_data]),
        (check_3_1_5_trusted_package_managers, [dependency_files]),
        (check_3_1_6_signed_sbom, [sbom_artifacts]),
        (check_3_1_7_pinned_dependencies, [dependency_files]),
        (check_3_1_8_package_age, [dependency_files]),
        (check_3_2_1_dependency_usage_policy, [group_push_rules]),
        (check_3_2_2_package_scanning, [gitlab_ci_content, security_scan_data]),
        (check_3_2_3_license_scanning, [gitlab_ci_content, license_scan_data]),
    ]

    for check, args in checks:
        print(f"Running {check.__name__}...")
        result = check(*args)  # Call the function with unpacked arguments

        # Handle both integer (compliance score) and string (manual check) results
        if isinstance(result, int):
            total_score += result  # Accumulate the score from each check
            results[check.__name__] = result  # Save the score
        elif isinstance(result, str):
            # Print manual check messages properly and store them in results
            print(result)  # Print the manual check message
            results[check.__name__] = result

        print("\n")  # Add space after each check's output

    # Calculate total possible score based on automated checks (which return integers)
    total_possible_score = (
        len([score for score in results.values() if isinstance(score, int)]) * 5
    )

    print("\n===========================")
    print(f"Total dependency compliance score: {total_score}/{total_possible_score}")
    print("===========================")

    # Return both score and detailed results for manual checks
    return results
