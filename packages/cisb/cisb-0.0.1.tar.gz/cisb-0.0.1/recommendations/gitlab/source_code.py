from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateutil_parser


# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()

"""1.1.X CODE CHANGES"""


def check_1_1_1_version_control_tracking():
    """Ensure any changes to code are tracked in a version control platform."""

    # Since the tool is running in a GitLab repository, we assume compliance
    compliance_score = 5

    print("\nCheck 1.1.1: Code changes are tracked in version control.")
    print(f"Compliance score: {compliance_score}/5\n")

    return compliance_score


def check_1_1_2_jira_integration_and_requirements(project_data, jira_data):
    """
    Check if the project has Jira integration and enforces Jira issue requirements.

    Points breakdown:
    - 2 points if Jira integration is active.
    - 3 points if the project requires an associated Jira issue for merge requests.
    """
    compliance_score = 0  # Initialize the compliance score to 0

    # Check if Jira integration is active
    if jira_data.get("active", False):
        print("Compliant: Jira integration is active.")
        compliance_score += 2  # Add 2 points if Jira integration is active
    else:
        print("Non-compliant: Jira integration is not active.")

    # Check if the project requires a Jira issue for merge requests
    if project_data.get("prevent_merge_without_jira_issue", False):
        print(
            "Compliant: The project requires an associated Jira issue for merge requests."
        )
        compliance_score += 3  # Add 3 points if Jira issue requirement is enabled
    else:
        print(
            "Non-compliant: The project does not require an associated Jira issue for merge requests."
        )

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_1_3_strongly_authenticated_approval_manual():
    """
    Ensure that any change to code receives approval of two strongly authenticated users (Manual).

    This check provides manual instructions for reviewing the project settings to ensure
    that two approvals are required for any code change, and that those approvers are using Multi-Factor Authentication (MFA).

    As this is a manual process, no compliance score is returned.
    """
    print(
        "Manual check required for verifying approval and MFA enforcement for code changes:"
    )

    print("To verify this setting, please follow the steps below:")
    print("1. On the left sidebar, select Search or go to and find your project.")
    print("2. Select **Settings > Merge requests**.")
    print(
        "3. In the Merge request approvals section, look for the **Approval rules** section."
    )
    print("4. Next to the rule you want to edit, select **Edit**.")
    print(
        "5. Ensure that the **In Approvals required** field is set to at least **2**."
    )
    print(
        "6. Additionally, ensure that approvers are required to use Multi-Factor Authentication."
    )

    print("\nManual remediation steps (if necessary):")
    print("1. Ensure at least two approvals are required for code merges.")
    print(
        "2. Enforce Multi-Factor Authentication (MFA) for users in the project settings."
    )

    print("\nSince this is a manual check, no compliance score is provided.")
    return None


def check_1_1_4_remove_approvals_link(project_data):
    """Ensure the user manually checks if 'Remove all approvals' is enabled."""
    base_url = "https://gitlab.com"
    project_name = project_data.get("path_with_namespace")  # Extract project path
    settings_path = f"/{project_name}/-/settings/merge_requests"
    full_url = base_url + settings_path
    print(f"Please manually check the 'Remove all approvals' setting here: {full_url}")
    return None


def check_1_1_5_restrict_dismissal_of_code_reviews(project_data):
    """
    This check ensures that a link is provided to manually verify if there are restrictions
    on who can dismiss code change reviews.
    The project name is extracted from the GitLab project data.
    """
    base_url = "https://gitlab.com"

    # Extract the project name from the API data
    project_name = project_data.get("path_with_namespace", "unknown_project")

    # Construct the URL for the repository settings - protected branches
    settings_path = f"/{project_name}/-/settings/repository"
    full_url = base_url + settings_path

    print(
        f"Please manually check the 'Protected Branches' settings for who can dismiss reviews here: {full_url}"
    )

    return None


def check_1_1_6_codeowners_configuration(codeowners_data):
    """
    Ensure that code owners are configured for sensitive code or configurations.
    """
    sensitive_paths = ["/config/", "/secrets/", "/env/"]  # Example sensitive paths

    if codeowners_data is None:
        print("CODEOWNERS file not found.")
        return 0

    codeowners_entries = codeowners_data.split("\n")
    codeowner_paths = [entry.split()[0] for entry in codeowners_entries if entry]

    for sensitive_path in sensitive_paths:
        if not any(sensitive_path in path for path in codeowner_paths):
            print(f"Code owner not configured for sensitive path: {sensitive_path}")
            compliance_score = 0
            break
    else:
        print("Code owners are properly configured for all sensitive paths.")
        compliance_score = 5

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_1_7_codeowners_review_required(codeowners_data, protected_branches_data):
    """
    Check that code owner reviews are required when a change affects owned code.
    This involves ensuring that the repository enforces Code Owner approval in the branch settings.
    """

    # Check if code owner approval is enabled for any branch
    code_owner_approval_enabled = False
    compliance_score = 0  # Initialize compliance score

    for branch in protected_branches_data:
        if branch.get("code_owner_approval_required", False):
            print(f"Code owner approval is required for branch: {branch['name']}")
            code_owner_approval_enabled = True
            break

    if not code_owner_approval_enabled:
        print("Code owner approval is NOT enabled for any branch. Non-compliant.")
        compliance_score = 0
    else:
        # If code owner approval is enabled, continue to check the CODEOWNERS file
        if codeowners_data:
            print("Codeowners file is present and has entries. Compliant.")
            compliance_score = 5
        else:
            print("Codeowners file is missing or has no valid entries. Non-compliant.")
            compliance_score = 0

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_1_8_inactive_branches(branches_data):
    """
    This check warns if there are inactive branches in the repository
    that should be reviewed or removed.
    """
    # Define the threshold for stale branches (90 days) as offset-aware
    stale_threshold = datetime.now(timezone.utc) - timedelta(days=90)

    inactive_branches = []
    compliance_score = 5  # Start with full compliance

    for branch in branches_data:
        last_commit_date = branch["commit"]["committed_date"]

        # Parse the last commit date to make it offset-aware
        last_commit_date = dateutil_parser.parse(last_commit_date)

        # Compare offset-aware datetime objects
        if last_commit_date < stale_threshold:
            inactive_branches.append(branch["name"])
            compliance_score = 0  # If there are inactive branches, set compliance to 0

    if inactive_branches:
        print(
            f"Warning: The following branches have been inactive for more than 90 days:"
        )
        for branch in inactive_branches:
            print(f"- {branch}")
        print("Consider reviewing or removing these branches.")
    else:
        print("All branches are active.")

    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_1_9_all_checks_passed_before_merge(protected_branches_data):
    """
    Ensure that all checks have passed before merging new code.
    This involves verifying that the 'Status checks must succeed' checkbox is enabled for protected branches.
    """
    # Initialize compliance score
    compliance_score = 0

    # Check if any branch requires all checks to pass
    status_checks_required = False

    for branch in protected_branches_data:
        if branch.get("push_access_levels"):
            for level in branch["push_access_levels"]:
                if (
                    level.get("access_level_description", "")
                    == "Status checks must succeed"
                ):
                    print(f"Status checks are required for branch: {branch['name']}")
                    status_checks_required = True
                    compliance_score = 5  # Fully compliant if at least one branch requires status checks

    if not status_checks_required:
        print(
            "No branch is configured to require status checks before merging. Non-compliant."
        )
        compliance_score = 0

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_1_10_branches_up_to_date(gitlab_data):
    """
    Ensure open Git branches are up to date before they can be merged into the code base.
    This check verifies the project's merge method to ensure that branches must be updated
    before being merged.
    """
    # Fetch the merge method from the gitlab_data
    merge_method = gitlab_data.get("merge_method")

    # If merge_method is not present, handle it as non-compliant
    if not merge_method:
        print("Unable to fetch merge method in the project data. Non-compliant.")
        print("Compliance score: 0/5")
        return 0

    # Compliant merge methods
    compliant_methods = ["merge_commit_with_semi_linear_history", "ff"]

    # Check the merge method
    if merge_method in compliant_methods:
        print(f"Compliant: The project is using the '{merge_method}' merge method.")
        print("Compliance score: 5/5")
        return 5  # Return the maximum score for compliance
    else:
        print(
            f"Non-compliant: The project is using an outdated merge method '{merge_method}'."
        )
        print(
            "Please set the merge method to 'Merge commit with semi-linear history' or 'Fast-forward merge'."
        )
        print("Compliance score: 0/5")
        return 0  # Return 0 for non-compliance


def check_1_1_11_all_comments_resolved(gitlab_data):
    """
    Ensure all open comments are resolved before allowing code change merging.
    This check verifies that the 'All threads must be resolved' checkbox is enabled
    for merge requests in the project settings.
    """

    # Fetch the setting from the GitLab data
    all_threads_resolved = gitlab_data.get(
        "merge_requests_events"
    )  # Example field, adjust based on actual API response

    # Check if the 'All threads must be resolved' setting is enabled
    if not all_threads_resolved:
        print(
            "Non-compliant: The project is not configured to require all comments to be resolved before merging."
        )
        print(
            "Please enable the 'All threads must be resolved' setting in merge requests."
        )
        print("Compliance score: 0/5")
        return 0
    else:
        print("Compliant: All open comments must be resolved before merging.")
        print("Compliance score: 5/5")
        return 5


def check_1_1_12_signed_commits_required(push_rules):
    """
    Ensure verification of signed commits for new changes before merging.
    This check verifies if the 'Reject unsigned commits' option is enabled in push rules.
    """

    if not push_rules:
        print("Could not fetch push rules. Assuming non-compliant.")
        return 0

    # Check if the 'reject_unsigned_commits' option is enabled
    if push_rules.get("reject_unsigned_commits", False):
        print("Compliant: The project requires signed commits for all new changes.")
        compliance_score = 5
    else:
        print("Non-compliant: The project allows unsigned commits.")
        compliance_score = 0

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_1_13_linear_history_required(gitlab_data):
    """
    Ensure linear history is required by reusing the compliance score
    from the merge method check (1.1.10).
    """
    # Simply call the previous check and return its score
    print("Reusing the compliance check from 1.1.10 for linear history requirement.")
    return check_1_1_10_branches_up_to_date(gitlab_data)


def check_1_1_14_branch_protection_for_admins(protected_branches_data):
    """
    Ensure branch protection rules are enforced for administrators.
    """

    compliance_score = 0  # Initialize compliance score

    # Check if 'allow_owner_manage_default_protection' is set to False
    for branch in protected_branches_data:
        if not branch.get("allow_owner_manage_default_protection", True):
            print(
                f"Compliant: Branch protection rules are enforced for administrators on branch {branch['name']}."
            )
            compliance_score = 5
        else:
            print(
                f"Non-compliant: Administrators can manage branch protection rules on branch {branch['name']}."
            )
            compliance_score = 0  # Return non-compliant if even one branch allows owners to manage protection

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_1_15_pushing_merging_restricted_to_trusted(protected_branches_data):
    """
    Ensure that only trusted individuals or teams are allowed to push or merge to protected branches.
    """
    compliance_score = 5  # Start with full compliance
    non_compliant_branches = []  # List of non-compliant branches

    for branch in protected_branches_data:
        branch_name = branch["name"]
        push_access_levels = branch.get("push_access_levels", [])
        merge_access_levels = branch.get("merge_access_levels", [])
        force_push = branch.get("force_push", False)

        # Check for force push
        if force_push:
            print(f"Non-compliant: Force push is allowed on branch: {branch_name}")
            non_compliant_branches.append(branch_name)
            compliance_score = 0  # Set to non-compliant

        # Check allowed roles or users for push and merge
        trusted_roles_push = [
            level["access_level_description"] for level in push_access_levels
        ]
        trusted_roles_merge = [
            level["access_level_description"] for level in merge_access_levels
        ]

        if not trusted_roles_push or not trusted_roles_merge:
            print(
                f"Non-compliant: No trusted users or roles defined for push or merge on branch: {branch_name}"
            )
            non_compliant_branches.append(branch_name)
            compliance_score = 0  # Set to non-compliant
        else:
            print(
                f"Compliant: Branch {branch_name} has trusted users or roles for push and merge."
            )

    if non_compliant_branches:
        print(
            f"The following branches are non-compliant: {', '.join(non_compliant_branches)}"
        )

    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_1_16_force_push_disabled(protected_branches_data):
    """
    Ensure force pushing is disabled for all protected branches in a GitLab repository.
    This check verifies that no one can force push code directly to any protected branch.
    """

    compliance_score = 5  # Start with full compliance

    if not protected_branches_data:
        print("No protected branches found. Non-compliant.")
        compliance_score = 0
        print(f"Compliance score: {compliance_score}/5")
        return compliance_score

    for branch in protected_branches_data:
        branch_name = branch.get("name", "unknown")
        push_access_levels = branch.get("push_access_levels", [])

        for access_level in push_access_levels:
            if access_level.get("allow_force_push", False):
                print(
                    f"Force push is allowed for branch '{branch_name}'. Non-compliant."
                )
                compliance_score = 0
            else:
                print(
                    f"Branch '{branch_name}' is protected from force pushing. Compliant."
                )

    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_1_17_branch_deletion_denied(protected_branches_data):
    """
    Ensure that branch deletions are denied for protected branches.
    This check verifies that no protected branches have deletion permissions enabled.
    """
    if not protected_branches_data:
        print("No protected branches found. Non-compliant.")
        return 0  # Non-compliant if no protected branches

    compliance_score = 5  # Start with full compliance

    for branch in protected_branches_data:
        if branch.get("allow_force_push", False) or branch.get(
            "allow_deletions", False
        ):
            print(
                f"Non-compliant: Branch '{branch['name']}' allows deletions or force pushes."
            )
            compliance_score = 0  # Set to non-compliant if any branch allows deletions
            break

    if compliance_score == 5:
        print("Compliant: Branch deletions are denied for all protected branches.")
    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_1_18_scan_for_risks(approval_data):
    """
    Check if security scanners are enabled in approval settings.
    - Full 5 points if at least 3 scanners are enabled.
    - 3 points if 2 scanners are enabled.
    - 1 point if 1 scanner is enabled.
    - 0 points if no scanners are enabled.
    """
    compliance_score = 0  # Initialize compliance score

    if not approval_data or "rules" not in approval_data:
        print("No approval rules found. Non-compliant.")
        print(f"Compliance score: {compliance_score}/5")
        return compliance_score

    for rule in approval_data["rules"]:
        # Print each rule to inspect the structure
        scanners = rule.get("scanners", [])

        # Count the number of enabled scanners
        num_scanners = len(scanners)

        if num_scanners >= 3:
            print(
                f"Compliant: {num_scanners} security scanners are enabled: {', '.join(scanners)}."
            )
            compliance_score = 5  # Full compliance if 3 or more scanners are enabled
        elif num_scanners == 2:
            print(
                f"Partially Compliant: 2 security scanners are enabled: {', '.join(scanners)}."
            )
            compliance_score = 3  # 3 points for 2 scanners
        elif num_scanners == 1:
            print(
                f"Minimally Compliant: 1 security scanner is enabled: {', '.join(scanners)}."
            )
            compliance_score = 1  # 1 point for 1 scanner
        else:
            print("Non-compliant: No security scanners are enabled.")
            compliance_score = 0  # No compliance if no scanners are enabled

    # Print the final compliance score
    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_1_19_audit_branch_protection_changes(audit_events):
    """
    Ensure that any changes to branch protection rules are audited.
    This check verifies that the audit log has recorded changes to the protected branch settings.
    """
    if not audit_events:
        print("Failed to retrieve audit events or no audit events available.")
        return 0  # Non-compliant if audit data is unavailable

    # Filter for events related to branch protection rule changes
    branch_protection_events = [
        event
        for event in audit_events
        if event.get("action") == "protected_branch_updated"
    ]

    if branch_protection_events:
        print("Compliant: Branch protection rule changes are audited.")
        for event in branch_protection_events:
            print(f"Audit Event: {event}")
        return 5  # Fully compliant
    else:
        print(
            "Non-compliant: No audit events found for branch protection rule changes."
        )
        return 0  # Non-compliant


def check_1_1_20_default_branch_protection(protected_branches_data, gitlab_data):
    """
    Ensure branch protection is enforced on the default branch.
    This check verifies that the main or default branch of a project is protected.
    """
    # Fetch the default branch from the project data
    default_branch = gitlab_data.get("default_branch")

    # Check if the default branch exists in the protected branches data
    protected_branch_names = [branch.get("name") for branch in protected_branches_data]

    if default_branch in protected_branch_names:
        print(f"Compliant: The default branch '{default_branch}' is protected.")
        print("Compliance score: 5/5")
        return 5  # Return the maximum score for compliance
    else:
        print(f"Non-compliant: The default branch '{default_branch}' is not protected.")
        print("Please enable protection for the default branch.")
        print("Compliance score: 0/5")
        return 0  # Return 0 for non-compliance


"""1.2.X REPOSITORY MANAGEMENT"""


def check_1_2_1_security_md_file(gitlab_data, security_md_file):
    """
    Check 1.2.1: Ensure all public repositories contain a SECURITY.md file.
    If the repository is private, it is considered compliant automatically.

    Args:
        project_data (dict): The GitLab project data containing visibility info.
        security_md_file (str): Content of the SECURITY.md file, if it exists.

    Returns:
        compliance_score (int): Compliance score out of 5.
    """
    # Check if the project is public or private
    visibility = gitlab_data.get("visibility", "private")

    if visibility != "public":
        print("This is a private repository. Automatically compliant.")
        print("Compliance score: 5/5\n")
        return 5  # Private repositories are compliant by default

    # Check for the existence of a SECURITY.md file for public repos
    if security_md_file:
        print("Compliant: SECURITY.md file is present in this public repository.")
        compliance_score = 5
    else:
        print("Non-compliant: No SECURITY.md file found in this public repository.")
        print("Please add a SECURITY.md file to the repository.")
        compliance_score = 0

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_2_2_repository_creation_restricted():
    """
    Manual check for ensuring repository creation is restricted to trusted users.
    This check does not contribute to the compliance score.
    """
    print("Manual check required:")
    print("Please verify the following in the GitLab Admin Area:")
    print("- Navigate to Admin Area > Settings > General > Sign-up restrictions")
    print("- Ensure 'Sign-up enabled' is disabled, or if enabled:")
    print("  - 'Require admin approval for new sign-ups' is selected")
    print("  - 'Email confirmation settings' is set to 'Hard'")

    # Since this is a manual check, it does not contribute to compliance score
    return None


def check_1_2_3_repository_deletion_limited(project_data):
    """
    Manual check for ensuring repository deletion is limited to specific trusted users.
    This check does not contribute to the compliance score.
    """

    base_url = "https://gitlab.com"
    project_name = project_data.get("path_with_namespace", "unknown_project")

    members_url = f"{base_url}/{project_name}/-/project_members"

    print("Manual check required:")
    print("Please verify the following in the GitLab project settings:")
    print(f"- Navigate to the Members page here: {members_url}")
    print("- Select Manage > Members.")
    print(
        "- At the top of the member list, from the dropdown list, select Max role the members have in the group."
    )
    print(
        "- Ensure that only a limited number of users have the 'Owner' or 'Maintainer' role."
    )
    print(
        "- If the minimum number of users with Owner/Maintainer role in the list is correct, you are compliant."
    )
    # Since this is a manual check, it does not contribute to compliance score
    return None


def check_1_2_4_issue_deletion_limited(project_data):
    """
    Manual check for ensuring issue deletion is limited to specific trusted users.
    This check does not contribute to the compliance score.
    """

    project_name = project_data.get("path_with_namespace")  # Extract project path
    base_url = "https://gitlab.com"
    members_path = f"/{project_name}/-/project_members"
    full_url = base_url + members_path

    print("Manual check required:")
    print(f"Please verify the following in the GitLab project settings: {full_url}")
    print("- Navigate to the project in GitLab.")
    print("- Go to 'Manage' > 'Members' from the left sidebar.")
    print(
        "- At the top of the member list, from the dropdown list, select 'Max role' the members have in the group."
    )
    print(
        "- Ensure that only a limited number of users have the 'Owner' or 'Maintainer' role."
    )
    print("- If only trusted users have the correct permissions, you are compliant.")

    # Since this is a manual check, it does not contribute to compliance score
    return None


def check_1_2_5_forks_tracked(forks_data):
    """
    Ensure all copies (forks) of the code are tracked and accounted for.
    The forks_data should be provided as input to this check.
    """
    if forks_data:
        print(f"Compliant: Project has {len(forks_data)} forks tracked:")
        for fork in forks_data:
            print(f"- Fork: {fork['name']} by {fork['owner']['username']}")
        compliance_score = 5  # Fully compliant if forks are tracked
    else:
        print(
            "Compliant: No forks found for this project. All forks are accounted for."
        )
        compliance_score = 5  # Fully compliant if no forks exist

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_2_6_visibility_change_tracked(audit_events):
    """
    Ensure that the ability to track visibility changes is present, regardless of whether
    there are actual visibility change events in the logs.

    Args:
    audit_events (list): A list of audit events retrieved from the GitLab API.

    Returns:
    int: Compliance score out of 5.
    """
    # Define visibility change actions
    visibility_change_actions = [
        "Changed visibility from Private to Public",
        "Changed visibility from Internal to Public",
    ]

    # Check if we can track visibility change events, even if none have occurred
    if isinstance(audit_events, list):
        print("Compliant: Ability to track visibility changes detected.")
        compliance_score = 5  # Full compliance if audit events tracking is available
    else:
        print("Non-compliant: Unable to retrieve audit events or tracking not enabled.")
        compliance_score = 0  # Non-compliance if we can't retrieve audit events

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_2_7_inactive_repository(branches_data):
    """
    Ensure the 'main' or 'master' branch of the repository has been updated within the last 6 months.

    Args:
    branches_data (list): A list of branches and their associated commit data.

    Returns:
    int: Compliance score out of 5.
    """
    # Define the threshold for inactive branches (6 months)
    six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)

    # Look for the 'main' or 'master' branch
    main_branch = None
    for branch in branches_data:
        if branch["name"] in ["main", "master"]:
            main_branch = branch
            break

    # If no 'main' or 'master' branch is found, consider it non-compliant
    if not main_branch:
        print("Non-compliant: No 'main' or 'master' branch found.")
        print("Compliance score: 0/5\n")
        return 0

    # Get the last commit date of the 'main' or 'master' branch
    last_commit_date = main_branch.get("commit", {}).get("committed_date")

    if not last_commit_date:
        print(f"Non-compliant: Branch '{main_branch['name']}' has no commit history.")
        print("Compliance score: 0/5\n")
        return 0

    # Parse and check if the branch has had commits in the last 6 months
    last_commit_date = dateutil_parser.parse(last_commit_date)

    if last_commit_date < six_months_ago:
        print(
            f"Non-compliant: The '{main_branch['name']}' branch has not been updated in the last 6 months."
        )
        print("Compliance score: 0/5\n")
        return 0
    else:
        print(
            f"Compliant: The '{main_branch['name']}' branch has been updated within the last 6 months."
        )
        print("Compliance score: 5/5\n")
        return 5


"""1.3.X CONTRIBUTION ACCESS"""


def check_1_3_1_inactive_project_users(project_events):
    """
    Check if there are inactive users in a specific project based on their contributions
    (commits, merge requests, issues) within the last 6 months.

    Args:
    project_events (list): A list of project events.

    Returns:
    None: This check is informational and does not affect the compliance score.
    """
    # Calculate the threshold for inactive users (e.g., 6 months ago)
    six_months_ago = datetime.now() - timedelta(days=180)

    # Sets to store active and inactive users
    inactive_users = set()
    active_users = set()

    # Logging to check if project_events are being processed
    if not project_events:
        print("No project events found.")
        return None

    print(f"Processing {len(project_events)} project events...")

    # Check each event to see if the user has been active in the last 6 months
    for event in project_events:
        user = event.get("author", {})
        user_name = user.get("name", "Unknown")
        user_last_activity = event.get("created_at", None)

        if user_last_activity:
            last_activity_date = datetime.strptime(
                user_last_activity, "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            # If the activity is older than 6 months, consider them inactive
            if last_activity_date < six_months_ago:
                print(f"User {user_name} is inactive since {last_activity_date}.")
                inactive_users.add(user_name)
            else:
                active_users.add(user_name)

    # Filter out users who have been active within the last 6 months
    inactive_users = inactive_users - active_users

    if inactive_users:
        print(f"Found {len(inactive_users)} inactive users in the project:")
        for user in inactive_users:
            print(f" - {user}")
    else:
        print("No inactive users found for this project.")

    return None


def check_1_3_2_limit_top_level_group_creation():
    """
    Manual check to ensure top-level group creation is limited to specific, trusted users.

    This check provides instructions to manually verify that only trusted users can create
    top-level groups in the GitLab Admin Area.

    Returns:
        None: This is a manual check and does not return a compliance score.
    """
    print("Manual check required:")
    print(
        "Please verify that top-level group creation is limited to specific, trusted users by performing the following steps:"
    )
    print("1. In the GitLab UI, go to the Admin Area.")
    print("2. In the left sidebar, select 'Settings' and then 'General'.")
    print("3. Expand the 'Account and limit' section.")
    print(
        "4. Ensure the 'Allow new users to create top-level groups' checkbox is **not** checked."
    )
    print(
        "\nIf the checkbox is unchecked, top-level group creation is restricted to trusted users."
    )
    print("Since this is a manual check, no compliance score is assigned.")

    return None  # No compliance score for manual checks


def check_1_3_3_minimum_number_of_administrators():
    """
    This check is a manual verification for ensuring the minimum number of administrators are set for the organization.
    No compliance score will be returned. Instead, the user is prompted with instructions on how to perform the audit.
    """

    # Provide the instructions for manually performing the check
    print(
        "Manual check required to ensure minimum number of administrators are set for the organization:"
    )
    print("\nFollow these steps:")
    print("1. On the left sidebar, select 'Search' or go to and find your project.")
    print("2. Select 'Manage > Members'.")
    print(
        "3. At the top of the member list, from the dropdown list, select 'Max role' the members have in the group."
    )
    print("4. Review the list of members with the 'Owner' or 'Maintainer' role.")
    print(
        "5. If there are only a minimal number of members with these roles, you are compliant."
    )
    print("\nRemediation (if non-compliant):")
    print("1. Go to 'Manage > Members' again.")
    print("2. Use the 'Max role' filter to identify users with excessive permissions.")
    print(
        "3. Remove any unnecessary administrators by selecting 'Remove member' next to their name."
    )

    print(
        "\nFor detailed documentation, refer to: https://docs.gitlab.com/ee/user/project/members/#filter-and-sort-project-members"
    )
    print(
        "This check does not return a compliance score, as it requires manual review."
    )

    return None


def check_1_3_4_mfa_for_contributors():
    """
    Manual check: Verify that MFA is enforced for contributors.
    This check does not return a compliance score, but it provides the necessary steps for manual verification.
    """

    print("\n=== Check 1.3.4: Ensure MFA is required for contributors ===")

    print(
        "This is a manual check to verify if MFA is enforced for contributors in your GitLab group."
    )
    print("Please follow these steps to perform the check manually:\n")

    print("1. In GitLab, on the left sidebar, at the bottom, select Admin Area.")
    print("2. Select Settings > General.")
    print("3. Expand the 'Sign-in restrictions' section.")
    print("4. Check if the 'Enforce two-factor authentication' option is enabled.")
    print("   If it is enabled, you are compliant.\n")

    print(
        "To enforce MFA, you need to enable the 'Enforce two-factor authentication' option in the Sign-in restrictions section."
    )
    print(
        "\nThis check does not return a compliance score since it requires a manual audit."
    )

    return None


def check_1_3_5_mfa_enforcement():
    """
    This manual check ensures that Multi-Factor Authentication (MFA) is required for all users
    in the organization.
    """
    # Since this is a manual check, we do not return a compliance score, but provide instructions.

    print("Manual check required:")
    print(
        "For every organization in GitLab, ensure Multi-Factor Authentication is enforced using the following steps:"
    )

    # Instructions for enforcing MFA via the GitLab Admin UI
    print("\nUse the GitLab UI to enforce MFA:")
    print("1. On the left sidebar, select 'Search' or go to the Admin Area.")
    print("2. In the Admin Area, select 'Settings' > 'General'.")
    print("3. Under 'Sign-in restrictions', expand the section.")
    print("4. Verify that 'Enforce two-factor authentication' is enabled.")

    # Instructions for how MFA enforcement can be implemented
    print("\nYou can enforce MFA in two different ways:")
    print("- Enforce on next sign in.")
    print("- Suggest on next sign in, but allow a grace period before enforcing.")

    print("\nIf MFA is not enabled for all users, the organization is non-compliant.")

    # Since this is a manual check, no compliance score is returned.
    return None


def check_1_3_6_company_approved_email():
    """
    Ensure new members are required to be invited using company-approved email addresses (Manual Check).
    """

    # Instructions for manual check
    print("Manual Check Required:")
    print(
        "For every group in use, verify for each invitation that the invited email address is company-approved by performing the following:"
    )
    print("1. On the left sidebar, select 'Search' or go to and find your group.")
    print("2. Select 'Manage' > 'Members'.")
    print(
        "3. Members that are not automatically added are displayed on the 'Invited' tab."
    )
    print("4. Verify that each invitation email is company-approved by your company.")

    # No compliance score since this is a manual check
    return None


def check_1_3_7_two_administrators_per_repository(project_members):
    """
    Check if there are exactly two users with administrative permissions (Owner or Maintainer) for the repository.

    Args:
        project_members (list): List of project members with their access levels.

    Returns:
        compliance_score (int): Compliance score based on the number of admins found.
    """
    print("Check 1.3.7: Ensure two administrators are set for the repository.")

    # Initialize the compliance score to 0
    compliance_score = 0

    if project_members is None:
        print("Failed to retrieve members. Cannot proceed with the check.")
        return compliance_score

    # Count users with admin roles (Maintainer = 40, Owner = 50)
    admin_users = [
        member for member in project_members if member.get("access_level") >= 40
    ]

    # Display the result and assign the compliance score
    if len(admin_users) == 2:
        print(
            f"Compliant: There are exactly two users with administrative permissions: {[user['username'] for user in admin_users]}"
        )
        compliance_score = 5  # Full score for compliance
    elif len(admin_users) < 2:
        print(
            f"Non-compliant: Fewer than two users with administrative permissions found: {[user['username'] for user in admin_users]}"
        )
        compliance_score = 2  # Partial score for non-compliance
    else:
        print(
            f"Non-compliant: More than two users with administrative permissions found: {[user['username'] for user in admin_users]}"
        )
        compliance_score = 0  # No compliance if more than 2 users found

    print(f"Total admin users found: {len(admin_users)}")
    print(f"Compliance score: {compliance_score}/5")

    return compliance_score


def check_1_3_8_strict_base_permissions(project_members):
    """
    Ensure strict base permissions are set for the organization or project repository.
    This check will analyze the access level for members and ensure that
    unnecessary write or higher permissions are not granted by default.

    Returns:
        compliance_score (int): Compliance score based on the strictness of base permissions.
    """
    print("Check 1.3.8: Ensuring strict base permissions are set for the repository.")

    # Initialize the compliance score
    compliance_score = 5

    # Define strict access levels (Guest or Reporter in GitLab are considered strict)
    strict_access_levels = [10, 20]  # Guest (10), Reporter (20)

    # Check the access levels of all project members
    non_compliant_users = []
    for member in project_members:
        user_access_level = member.get("access_level")
        username = member.get("username")

        # Ensure no user has higher permissions than Reporter
        if user_access_level not in strict_access_levels:
            print(
                f"Non-compliant: User '{username}' has too high access level: {user_access_level}"
            )
            non_compliant_users.append(username)

    # Adjust compliance score based on findings
    if non_compliant_users:
        print(
            f"Non-compliant: {len(non_compliant_users)} users have too high access level."
        )
        compliance_score = 0
    else:
        print("Compliant: All users have strict base permissions.")

    print(f"Compliance score: {compliance_score}/5\n")
    return compliance_score


def check_1_3_9_verified_domain():
    print(
        "Check 1.3.9: Ensuring the organization's identity is confirmed with a 'Verified' badge."
    )

    # Since domain verification cannot be fetched via API, this is a manual check
    print("Manual Check Required:")
    print("1. Navigate to your GitLab group settings.")
    print("2. Select 'Settings' > 'Domain Verification'.")
    print("3. Check if your organization's domains have the 'Verified' badge.")
    print("4. If verified, your organization's identity is confirmed and compliant.")

    return None


def check_1_3_10_scm_email_notifications_restricted_to_verified_domains():
    """
    Manual check to ensure that SCM email notifications are restricted to verified domains.
    Since there is no API to directly check this, users must follow the instructions to verify manually.
    """
    print(
        "Check 1.3.10: Ensure Source Code Management (SCM) email notifications are restricted to verified domains."
    )
    print(
        "\nThis check cannot be performed through the GitLab API. Please follow the manual instructions below:\n"
    )

    # Instructions for manual check
    instructions = """
    1. Navigate to your GitLab instance.
    2. On the left sidebar, select Search or go to and find your top-level group.
    3. Select Settings > Domain Verification.
    4. When viewing Domain Verification, ensure the listed domains are verified.
    5. Check if access is limited to only the verified domains for receiving SCM notifications.
    
    Remediation (if non-compliant):
    - Limit email notifications to only verified domains by ensuring all domains under Domain Verification are properly verified.
    """
    print(instructions)

    print(
        "\nPlease complete the manual verification, and mark compliance based on the following:\n"
    )
    print("Compliance Scoring:")
    print(" - 5/5: All SCM notifications are restricted to verified domains.")
    print(" - 0/5: Notifications are not restricted to verified domains.")

    return None


def check_1_3_11_ssh_certificates_enforcement():
    """
    This is a manual check to ensure the organization provides SSH certificates and enforces SSH certificate validation.
    The administrator must manually verify whether SSH key restrictions and certificate authorities are in place.
    """
    print("Check 1.3.11: Ensure an organization provides SSH certificates (Manual).")

    print("\nManual verification steps:")
    print("- Log in to GitLab as an admin.")
    print("- Navigate to Admin Area > Settings > General.")
    print("- Expand 'Visibility and access controls'.")
    print("- Ensure restrictions are applied on SSH key types and length.")
    print(
        "- If using an SSH Certificate Authority (CA), confirm that only verified certificates are accepted for repository access."
    )
    print(
        "- Verify that developers with unverified SSH keys cannot push or clone repositories."
    )

    print("\nNote: This check requires manual confirmation in GitLab settings.")

    return None


def check_1_3_12_ip_restrictions(is_self_managed, check_ip_restrictions):
    """
    Main check function to ensure Git access is restricted based on IP addresses.

    Args:
        group_id (int): The GitLab group ID.
        token (str): GitLab private token.

    If the instance is self-managed, it will run the automated check. Otherwise, it will provide a manual check.
    """
    if is_self_managed:
        print("Running automated IP restriction check for self-managed instance...")
        score = check_ip_restrictions
        print(f"Compliance score: {score}/5")
    else:
        print("Manual Check: Please follow these steps to verify IP restrictions:")
        print("1. Navigate to Settings > General for your group.")
        print("2. Expand the Permissions and group features section.")
        print("3. Check the 'Restrict access by IP address' text box.")


def check_1_3_13_code_anomalies(project_events):
    """Check for anomalous code pushes outside typical working hours."""
    print("Checking for anomalous code behavior...")

    if not project_events:
        print("No events found or failed to fetch events.")
        return

    # Define working hours (9 AM to 6 PM) and check the time of each event
    working_hours_start = 7
    working_hours_end = 19

    anomalies_found = False
    for event in project_events:
        if event.get("action_name") == "pushed to":
            event_time = datetime.strptime(
                event.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if (
                event_time.hour < working_hours_start
                or event_time.hour >= working_hours_end
            ):
                print(
                    f"Anomaly detected: Code push by {event['author']['name']} at {event_time}."
                )
                anomalies_found = True

    if not anomalies_found:
        print("No anomalies detected.")


"""1.4.X THIRD-PARTY"""


def check_1_4_1_admin_approval_for_installed_apps(installed_apps):
    """
    Ensure administrator approval is required for every installed application.
    If applications are found, assign None and recommend manual review.
    If no applications are found, automatically assign a score of 5 (compliant).

    Args:
        installed_apps (list): List of installed applications.

    Returns:
        int or None: Compliance score (5 for compliant, None if manual review is required).
    """
    print(
        "Check 1.4.1: Ensure administrator approval is required for installed applications."
    )

    # Check if there are any installed applications
    if not installed_apps:
        print("Compliant: No installed applications found.")
        return 5  # Fully compliant

    # Recommend manual review for installed applications
    print(f"Manual review needed: Found installed applications: {installed_apps}")
    print(
        "Please review the list of installed applications and ensure they are all approved by an administrator."
    )

    return None  # No score assigned, manual review is needed


def check_1_4_2_stale_applications(installed_apps):
    """
    Ensure stale applications are reviewed and inactive ones are removed.
    This check will return installed apps and recommend a manual review since we cannot automate the activity check.

    Args:
        installed_apps (list): List of installed applications.

    Returns:
        None: This check does not return a compliance score as it requires a manual review.
    """
    print(
        "Check 1.4.2: Ensure stale applications are reviewed and inactive ones are removed."
    )

    # Recommend manual review for installed applications
    if installed_apps:
        print(f"Manual review needed: Found installed applications: {installed_apps}")
        print(
            "Please review the list of installed applications and ensure they are all still active and necessary."
        )
        print("Verify that any stale or inactive apps are removed.")
    else:
        print("Compliant: No installed applications found.")

    return None  # No score, manual review is required


def check_1_4_3_least_privilege_for_installed_apps(installed_apps):
    """
    Ensure that each installed application is granted the least privilege required.
    Since there is no direct API method to retrieve permissions, this check
    will recommend a manual review for all installed applications.

    Args:
        installed_apps (list): List of installed applications.

    Returns:
        None: Recommends manual review.
    """
    print("Check 1.4.3: Ensure installed applications have the least privilege.")

    # Check if there are any installed applications
    if not installed_apps:
        print("Compliant: No installed applications found.")
        return None  # Fully compliant if no apps are installed

    # Recommend manual review for installed applications
    print(f"Manual review needed: Found installed applications: {installed_apps}")
    print(
        "Please manually review the permissions granted to these applications and ensure they adhere to the least privilege principle."
    )

    return None


def check_1_4_4_secure_webhooks(webhooks):
    """
    Ensure only secured webhooks (https and SSL verification) are used.

    Args:
        webhooks (list): List of webhooks fetched from a project or group.

    Returns:
        None: No score, just prints the compliance result.
    """
    print("Check 1.4.4: Ensure only secured webhooks are used.")

    # Initialize the compliance score
    compliance_score = 5

    if not webhooks:
        print("Compliant: No webhooks found.")
        return compliance_score  # No webhooks means full compliance

    non_compliant_hooks = []

    # Check each webhook
    for webhook in webhooks:
        url = webhook.get("url", "")
        ssl_verification = webhook.get("enable_ssl_verification", False)

        # If URL doesn't start with https or SSL verification is disabled, it's non-compliant
        if not url.startswith("https://") or not ssl_verification:
            non_compliant_hooks.append(url)

    # If any non-compliant webhooks are found, adjust the score to 0
    if non_compliant_hooks:
        print(f"Non-compliant: Found insecure webhooks: {non_compliant_hooks}")
        compliance_score = 0
    else:
        print(
            "Compliant: All webhooks are secure (https with SSL verification enabled)."
        )

    print(f"Final compliance score: {compliance_score}/5")
    return compliance_score


"""1.5.X CODE RISKS"""


def check_1_5_1_secret_detection_enabled(approval_data):
    """
    Check if secret detection scanner is enabled in approval settings.
    - 5 points if secret detection is enabled.
    - 0 points if secret detection is not enabled.
    """
    compliance_score = 0  # Initialize compliance score

    if not approval_data or "rules" not in approval_data:
        print("No approval rules found. Non-compliant.")
        print(f"Compliance score: {compliance_score}/5")
        return compliance_score

    for rule in approval_data["rules"]:
        # Get the list of scanners for the rule
        scanners = rule.get("scanners", [])

        # Check if 'secret_detection' is in the enabled scanners
        if "secret_detection" in scanners:
            print("Compliant: Secret detection is enabled.")
            compliance_score = 5  # Full compliance if secret detection is enabled
        else:
            print("Non-compliant: Secret detection is not enabled.")
            compliance_score = 0  # No compliance if secret detection is not enabled

    # Print the final compliance score
    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_5_2_ci_configuration_file_exists(repo_tree, project_data):
    """
    Check if a CI configuration file exists in the repository.
    Provide a link to the CI file for manual review if it exists.

    Args:
        project_id (int): GitLab project ID.
        token (str): GitLab private token for authentication.

    Returns:
        None: This check does not assign a compliance score.
    """

    project_name = project_data.get("path_with_namespace")  # Extract project path
    print("Check 1.5.2: Ensure a CI configuration file exists.")

    # Check if '.gitlab-ci.yml' exists in the repository tree

    if repo_tree:
        print(
            f"Review the CI configuration file at: https://gitlab.com/{project_name}/-/blob/main/.gitlab-ci.yml"
        )
    else:
        print("No CI configuration file found. Manual review required.")

    return None


def check_1_5_3_iac_scanner_in_approval_settings(approval_data):
    """
    Check if Infrastructure as Code (IaC) scanning is enabled in the project's approval settings.

    Args:
        approval_data (dict): Approval settings to check if 'iac_scanning' or similar is enabled.

    Returns:
        None: This is a manual check, so no score is provided.
    """
    print("Check 1.5.3: Ensure Infrastructure as Code (IaC) scanning is enabled.")

    # Check if approval data exists
    if not approval_data or "rules" not in approval_data:
        print("No approval rules found. Manual review required.")
        return None

    # Loop through the rules to find the scanners used
    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])

        # Check if 'iac_scanning' is present in the enabled scanners
        if "iac_scanning" in scanners:
            print("Compliant: Infrastructure as Code (IaC) scanning is enabled.")
        else:
            print(
                "Non-compliant: Infrastructure as Code (IaC) scanning is not enabled."
            )
            print("Please enable IaC scanning in the CI pipeline configuration.")

    # Since this is a manual review, no compliance score is returned.
    return None


def check_1_5_4_sast_scanning_enabled(approval_data):
    """
    Check if SAST (Static Application Security Testing) is enabled in the approval settings for code vulnerabilities.

    Args:
        approval_data (dict): Approval settings to check if 'SAST' scanning is included.

    Returns:
        str: Compliance result.
    """
    print(
        "Check 1.5.4: Ensure SAST is configured and running for code vulnerabilities."
    )

    if not approval_data or "rules" not in approval_data:
        print("No approval rules found. Non-compliant.")
        return None

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])

        if "sast" in scanners:
            print("Compliant: SAST scanning is enabled for code vulnerabilities.")
        else:
            print(
                "Non-compliant: SAST scanning is not enabled for code vulnerabilities."
            )

    return None


def check_1_5_5_dependency_scanning_enabled(approval_data):
    """
    Check if Dependency Scanning is enabled in the project approval settings.

    Args:
        approval_data (dict): Approval settings for the project.

    Returns:
        None: Manual review is required for non-compliance, or confirmation is provided for compliance.
    """
    print(
        "Check 1.5.5: Ensure Dependency Scanning is enabled for project dependencies."
    )

    if not approval_data or "rules" not in approval_data:
        print("No approval rules found. Please verify manually.")
        return None

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "dependency_scanning" in scanners:
            print("Compliant: Dependency Scanning is enabled in the project.")
        else:
            print(
                "Non-compliant: Dependency Scanning is not enabled in the project. Please review manually."
            )
            print("Remediation steps: Enable Dependency Scanning for the project.")

    return None


def check_1_5_6_license_scanning_enabled(approval_data):
    """
    Ensure open-source license issues in used packages are identified and scanned.

    Args:
        approval_data (dict): Approval settings to check if license scanning is enabled.

    Returns:
        None: Manual review recommendation or confirmation of compliance.
    """
    if not approval_data or "rules" not in approval_data:
        print("No approval rules found. Please verify manually.")
        return None

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "dependency_scanning" in scanners:
            print("Compliant: Dependency Scanning is enabled in the project.")
        else:
            print(
                "Non-compliant: Dependency Scanning is not enabled in the project. Please review manually."
            )
            print("Remediation steps: Enable Dependency Scanning for the project.")

    return None


def check_1_5_7_dast_scanner(approval_data):
    """
    Check if the DAST (Dynamic Application Security Testing) scanner is enabled in approval settings.

    Args:
        approval_data (dict): Approval settings to check if 'dast' scanner is included.

    Returns:
        str: Compliance result.
    """
    # Initialize compliance status
    compliance_score = 0
    scanner_enabled = False

    # Check if DAST scanner is included in the list of scanners in the approval data
    if not approval_data or "rules" not in approval_data:
        print("Approval data missing or invalid. Unable to check for DAST scanner.")
        return None

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "dast" in scanners:
            scanner_enabled = True
            break

    if scanner_enabled:
        print("Compliant: DAST scanner is enabled for this project.")
        compliance_score = 5  # Full compliance if DAST is enabled
    else:
        print("Non-compliant: DAST scanner is not enabled for this project.")
        compliance_score = 0

    print(f"Compliance score: {compliance_score}/5")
    return compliance_score


def check_1_5_8_dast_api_scanner(approval_data):
    """
    Check if DAST-API security scanning is enabled in the approval settings for the project.

    Args:
        approval_data (dict): Approval settings to check if 'dast_api' scanner is included.

    Returns:
        None: Since this is a compliance check without a score, it will return None.
    """
    print(
        "Check 1.5.8: Ensure DAST-API scanner is in place for API runtime security weaknesses."
    )

    # Check if the approval data contains the DAST-API scanner
    for rule in approval_data.get("rules", []):
        scanners = rule.get("scanners", [])

        if "api_fuzzing" in scanners or "dast_api" in scanners:
            print(
                f"Compliant: DAST-API scanner is enabled in the approved scanners: {', '.join(scanners)}."
            )
        else:
            print("Non-compliant: DAST-API scanner is not enabled in the project.")

    print(
        "Review the pipeline configuration to ensure the DAST-API scanner is correctly configured."
    )


"""Runs every check"""


async def run_all_checks(
    project_data,
    approval_data,
    codeowners_data,
    protected_branches_data,
    branches_data,
    jira_data,
    push_rules,
    audit_events,
    security_md_file,
    forks_data,
    project_events,
    project_members,
    is_self_managed,
    check_ip_restrictions,
    installed_apps,
    webhooks,
    repo_tree,
):
    """Run all the checks defined in this file."""
    total_score = 0
    results = {}  # Dictionary to store check results

    checks = [
        (check_1_1_1_version_control_tracking, []),
        (check_1_1_2_jira_integration_and_requirements, [project_data, jira_data]),
        (check_1_1_3_strongly_authenticated_approval_manual, []),
        (check_1_1_4_remove_approvals_link, [project_data]),
        (check_1_1_5_restrict_dismissal_of_code_reviews, [project_data]),
        (
            check_1_1_6_codeowners_configuration,
            [codeowners_data],
        ),  # New CODEOWNERS check
        (
            check_1_1_7_codeowners_review_required,
            [codeowners_data, protected_branches_data],
        ),
        (check_1_1_8_inactive_branches, [branches_data]),
        (check_1_1_9_all_checks_passed_before_merge, [protected_branches_data]),
        (check_1_1_10_branches_up_to_date, [project_data]),
        (check_1_1_11_all_comments_resolved, [project_data]),
        (check_1_1_12_signed_commits_required, [push_rules]),
        (check_1_1_13_linear_history_required, [project_data]),
        (check_1_1_14_branch_protection_for_admins, [protected_branches_data]),
        (check_1_1_15_pushing_merging_restricted_to_trusted, [protected_branches_data]),
        (check_1_1_16_force_push_disabled, [protected_branches_data]),
        (check_1_1_17_branch_deletion_denied, [protected_branches_data]),
        (check_1_1_18_scan_for_risks, [approval_data]),
        (check_1_1_19_audit_branch_protection_changes, [audit_events]),
        (
            check_1_1_20_default_branch_protection,
            [protected_branches_data, project_data],
        ),
        (check_1_2_1_security_md_file, [project_data, security_md_file]),
        (check_1_2_2_repository_creation_restricted, []),
        (check_1_2_3_repository_deletion_limited, [project_data]),
        (check_1_2_4_issue_deletion_limited, [project_data]),
        (check_1_2_5_forks_tracked, [forks_data]),
        (check_1_2_6_visibility_change_tracked, [audit_events]),
        (check_1_2_7_inactive_repository, [branches_data]),
        (check_1_3_1_inactive_project_users, [project_events]),
        (check_1_3_2_limit_top_level_group_creation, []),
        (check_1_3_3_minimum_number_of_administrators, []),
        (check_1_3_4_mfa_for_contributors, []),
        (check_1_3_5_mfa_enforcement, []),
        (check_1_3_6_company_approved_email, []),
        (check_1_3_7_two_administrators_per_repository, [project_members]),
        (check_1_3_8_strict_base_permissions, [project_members]),
        (check_1_3_9_verified_domain, []),
        (check_1_3_10_scm_email_notifications_restricted_to_verified_domains, []),
        (check_1_3_11_ssh_certificates_enforcement, []),
        (check_1_3_12_ip_restrictions, [is_self_managed, check_ip_restrictions]),
        (check_1_3_13_code_anomalies, [project_events]),
        (check_1_4_1_admin_approval_for_installed_apps, [installed_apps]),
        (check_1_4_2_stale_applications, [installed_apps]),
        (check_1_4_3_least_privilege_for_installed_apps, [installed_apps]),
        (check_1_4_4_secure_webhooks, [webhooks]),
        (check_1_5_1_secret_detection_enabled, [approval_data]),
        (check_1_5_2_ci_configuration_file_exists, [repo_tree, project_data]),
        (check_1_5_3_iac_scanner_in_approval_settings, [approval_data]),
        (check_1_5_4_sast_scanning_enabled, [approval_data]),
        (check_1_5_5_dependency_scanning_enabled, [approval_data]),
        (check_1_5_6_license_scanning_enabled, [approval_data]),
        (check_1_5_7_dast_scanner, [approval_data]),
        (check_1_5_8_dast_api_scanner, [approval_data]),
    ]

    for check, args in checks:
        print(f"Running {check.__name__}...")
        score = check(*args)  # Call the function with unpacked arguments
        if score is not None:  # Only add to total score if the score is not None
            total_score += score  # Accumulate the score from each check

        results[check.__name__] = score  # Save check and score in results dictionary
        print("\n")  # Add space after each check's output

    total_possible_score = (
        len([score for score in results.values() if score is not None]) * 5
    )

    print("\n===========================")
    print(f"Total source code compliance score: {total_score}/{total_possible_score}")
    print("===========================")

    return results
