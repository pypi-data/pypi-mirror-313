from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateutil_parser
from services.common_utils import run_checks
import logging

# Define a ThreadPoolExecutor for running I/O bound tasks
executor = ThreadPoolExecutor()


"""1.1.X CODE CHANGES"""


def check_1_1_1_version_control_tracking():
    """Ensure any changes to code are tracked in a version control platform."""
    compliance_score = 5
    message = "Compliant: Code changes are tracked in version control."
    return compliance_score, message


def check_1_1_2_jira_integration_and_requirements(project_data, jira_data):
    """Check if the project has Jira integration and enforces Jira issue requirements."""
    compliance_score = 0
    message = []

    # Check if Jira integration is active
    if jira_data.get("active", False):
        compliance_score += 2
        message.append("✅ Jira integration is active.")
    else:
        message.append("❌ Jira integration is not active.")

    # Check if project enforces Jira issue requirements for merging
    if project_data.get("prevent_merge_without_jira_issue", False):
        compliance_score += 3
        message.append("✅ Jira issue requirement is enforced for merge requests.")
    else:
        message.append("❌ Jira issue requirement is not enforced for merge requests.")

    # If compliance_score is 5, provide a more positive message
    if compliance_score == 5:
        message.append(
            "Project is fully compliant with Jira integration and issue requirements."
        )

    # Join the messages and return
    return compliance_score, " ".join(message)


def check_1_1_3_strongly_authenticated_approval(approval_rules):
    """
    Ensure approval of two strongly authenticated users for code changes.
    Returns a compliance score based on approval settings and provides a message to ensure approvals are properly configured.

    Args:
        approval_rules (list): The list of approval rules retrieved from the GitLab API.

    Returns:
        tuple: compliance_score (int), message (str)
    """
    # Default score and message
    compliance_score = None
    message = (
        "Manual check required to ensure at least two strongly authenticated approvers are required for code changes. "
        "Verify that the code change approval process is secure by following these steps:\n"
        "1. Navigate to **Settings > Merge Requests** in your GitLab project.\n"
        "2. Check the approval rules to ensure that at least two approvals are required before any code is merged into protected branches.\n"
        "3. Make sure that the approvers are trusted individuals who are strongly authenticated (using methods such as Multi-Factor Authentication or other identity verification mechanisms).\n"
        "4. Confirm that changes to the approval rules cannot be bypassed or overridden by users without the proper permissions.\n"
        "5. If no approval rules are set, you must configure them to require at least two approvers and ensure they follow security best practices."
    )

    # Ensure approval_rules is not None or empty
    if approval_rules and isinstance(approval_rules, dict):
        # Check for general approval settings
        if "approvals_before_merge" in approval_rules:
            approvals_required = approval_rules.get("approvals_before_merge", 0)
            
            # Set the compliance score based on approvals required
            if approvals_required == 1:
                compliance_score = 2
                message = (
                    "Compliant: 1 approval is required for code changes. "
                    "However, it's recommended to require at least two approvers for increased security.\n"
                    "Ensure the approvers are strongly authenticated (e.g., using Multi-Factor Authentication).\n"
                    "Steps:\n"
                    "1. Go to **Settings > Merge Requests** and review the approval rules.\n"
                    "2. Consider increasing the number of required approvers to two for stronger protection."
                )
            elif approvals_required >= 2:
                compliance_score = 5
                message = (
                    "Compliant: 2 or more approvals are required for code changes. "
                    "Ensure that the approvers are strongly authenticated (e.g., using Multi-Factor Authentication).\n"
                    "Steps:\n"
                    "1. Verify that the approval rules enforce two or more approvers for each merge.\n"
                    "2. Make sure that all approvers are trusted individuals and use strong authentication mechanisms."
                )
        else:
            # Check if specific rules exist under "rules" (from `/approval_settings`)
            rules = approval_rules.get("rules", [])
            for rule in rules:
                if rule.get("rule_type") == "any_approver":
                    approvals_required = rule.get("approvals_required", 0)

                    # Set the compliance score based on approvals required
                    if approvals_required == 1:
                        compliance_score = 2
                        message = (
                            "Compliant: 1 approval is required for code changes. "
                            "However, it's recommended to require at least two approvers for increased security.\n"
                            "Ensure the approvers are strongly authenticated (e.g., using Multi-Factor Authentication).\n"
                            "Steps:\n"
                            "1. Go to **Settings > Merge Requests** and review the approval rules.\n"
                            "2. Consider increasing the number of required approvers to two for stronger protection."
                        )
                    elif approvals_required >= 2:
                        compliance_score = 5
                        message = (
                            "Compliant: 2 or more approvals are required for code changes. "
                            "Ensure that the approvers are strongly authenticated (e.g., using Multi-Factor Authentication).\n"
                            "Steps:\n"
                            "1. Verify that the approval rules enforce two or more approvers for each merge.\n"
                            "2. Make sure that all approvers are trusted individuals and use strong authentication mechanisms."
                        )
                    break
    else:
        # If no approval rules found, set the message to request enabling approval
        message = (
            "Non-compliant: No approval rules set. Ensure that at least two approvals are required for code changes.\n"
            "Steps:\n"
            "1. Navigate to **Settings > Merge Requests** in your GitLab project.\n"
            "2. Set the approval rules to require at least two approvers for each code change.\n"
            "3. Ensure that these approvers are strongly authenticated and follow security best practices."
        )

    return compliance_score, message


def check_1_1_4_remove_approvals_link(approvals):
    """
    Ensure previous approvals are dismissed when updates are introduced to a code change proposal.

    Args:
        project_id (int): The GitLab project ID.
        token (str): The GitLab private token for authentication.

    Returns:
        tuple: (compliance score, message). Compliance score is 5 if setting is enabled, 0 otherwise.
    """

    if not approvals:
        # If we couldn't retrieve the approval settings, return a manual check message
        return None, "Manual check required: Could not fetch approval settings."

    # Check if "reset_approvals_on_push" is set to true
    if approvals.get("reset_approvals_on_push") is True:
        return 5, "Compliant: Approvals are dismissed when new changes are introduced."
    else:
        # Provide remediation steps if the setting is not enabled
        message = (
            "Non-compliant: Approvals are not dismissed when new changes are introduced. "
            "To remediate:\n"
            "1. Navigate to Settings > Merge Requests in your GitLab project.\n"
            "2. Ensure the 'Remove all approvals when a commit is added' option is selected."
        )
        return 0, message


def check_1_1_5_restrict_dismissal_of_code_reviews(protected_branches):
    """
    Ensure restrictions are in place for who can dismiss code change reviews.
    This function checks the protected branches to see if appropriate dismissal restrictions exist.
    """
    # Define the trusted access levels: 40 (Maintainers) and 60 (Owners)
    trusted_access_levels = [40, 60]

    for branch in protected_branches:
        # Extract the push and merge access levels
        push_access_levels = branch.get("push_access_levels", [])
        merge_access_levels = branch.get("merge_access_levels", [])

        # Check if maintainers or owners are the only ones allowed to dismiss reviews
        for access_level in push_access_levels + merge_access_levels:
            if access_level.get("access_level") not in trusted_access_levels:
                # If any other role has dismissal rights, consider it non-compliant
                message = (
                    f"Non-compliant: Dismissal restrictions are not properly enforced for branch '{branch['name']}'. "
                    "Ensure only Maintainers (40) or Owners (60) can dismiss code change reviews."
                )
                return 0, message

    # If everything looks good, return compliant message
    message = "Compliant: Only trusted users (Maintainers or Owners) can dismiss code change reviews."
    return 5, message


def check_1_1_6_codeowners_configuration(codeowners_data):
    """Ensure that a CODEOWNERS file exists."""
    if not codeowners_data:
        return 0, "Non-compliant: CODEOWNERS file not found."

    return 5, "Compliant: CODEOWNERS file exists."


def check_1_1_7_codeowners_review_required(codeowners_data, protected_branches_data):
    """Ensure code owner reviews are required when changing owned code."""
    code_owner_approval_enabled = False

    for branch in protected_branches_data:
        if branch.get("code_owner_approval_required", False):
            code_owner_approval_enabled = True
            break

    if not code_owner_approval_enabled:
        return 0, "Non-compliant: Code owner approval is not enabled for any branch."

    if codeowners_data:
        return (
            5,
            "Compliant: Code owner approval is enabled, and CODEOWNERS file is present.",
        )
    else:
        return 0, "Non-compliant: Codeowners file is missing."


def check_1_1_8_inactive_branches(branches_data):
    """Ensure there are no inactive branches in the repository."""
    stale_threshold = datetime.now(timezone.utc) - timedelta(days=90)
    inactive_branches = []

    for branch in branches_data:
        last_commit_date = dateutil_parser.parse(branch["commit"]["committed_date"])
        if last_commit_date < stale_threshold:
            inactive_branches.append(branch["name"])

    if inactive_branches:
        message = (
            "Non-compliant: The following branches have been inactive for more than 90 days: "
            + ", ".join(inactive_branches)
        )
        return 0, message
    else:
        return 5, "Compliant: All branches are active."


def check_1_1_9_all_checks_passed_before_merge(protected_branches_data):
    """Ensure all checks have passed before merging new code."""
    status_checks_required = False

    for branch in protected_branches_data:
        if branch.get("push_access_levels"):
            for level in branch["push_access_levels"]:
                if (
                    level.get("access_level_description", "")
                    == "Status checks must succeed"
                ):
                    status_checks_required = True
                    break

    if status_checks_required:
        return 5, "Compliant: Status checks are required before merging."
    else:
        return (
            0,
            "Non-compliant: Status checks are not enforced before merging. To fix this, go to Settings > Merge Requests, and ensure the 'Status checks must succeed' option is enabled for all protected branches.",
        )


def check_1_1_10_branches_up_to_date(project_data):
    """Ensure open Git branches are up to date before they can be merged."""
    merge_method = project_data.get("merge_method")

    if not merge_method:
        return (
            0,
            "Non-compliant: Unable to determine the merge method from the project data. Check the project's merge settings.",
        )

    compliant_methods = ["merge_commit_with_semi_linear_history", "ff"]
    if merge_method in compliant_methods:
        return (
            5,
            f"Compliant: The project uses the '{merge_method}' merge method, which helps ensure branches are up-to-date before merging.",
        )
    else:
        return (
            0,
            f"Non-compliant: The project uses the '{merge_method}' merge method, which could result in outdated branches being merged. Consider switching to 'Fast-forward merge' or 'Merge commit with semi-linear history' for better branch management.",
        )


def check_1_1_11_all_comments_resolved(project_data):
    """Ensure all open comments are resolved before allowing code change merging."""
    all_threads_resolved = project_data.get("merge_requests_events", False)

    if not all_threads_resolved:
        return (
            0,
            "Non-compliant: The project does not require all threads to be resolved before merging. "
            "This may allow unresolved feedback, potential bugs, or security concerns to be overlooked. "
            "It is recommended to enable 'All threads must be resolved' in the merge request settings "
            "to ensure thorough review and avoid merging incomplete or problematic code.",
        )
    else:
        return (
            5,
            "Compliant: The project requires all threads to be resolved before merging, ensuring all concerns are addressed before integration.",
        )


def check_1_1_12_signed_commits_required(push_rules):
    """Ensure verification of signed commits for new changes before merging."""
    if push_rules.get("reject_unsigned_commits", False):
        return 5, (
            "Compliant: Signed commits are required for this project. "
            "This ensures that all commits are verified, adding an extra layer of security "
            "to prevent unverified or unauthorized changes from being merged."
        )
    else:
        return 0, (
            "Non-compliant: Unsigned commits are currently allowed, which poses a risk. "
            "Consider enabling the 'Reject unsigned commits' option in the repository settings "
            "to ensure that all commits are signed and verified before merging."
        )


def check_1_1_13_linear_history_required(project_data):
    """Ensure linear history is required by reusing the compliance score from the merge method check (1.1.10)."""
    return check_1_1_10_branches_up_to_date(project_data)


def check_1_1_14_branch_protection_for_admins(protected_branches_data):
    """Ensure branch protection rules are enforced for administrators."""
    compliance_score = 0

    # Check if branch protection is properly enforced for administrators
    for branch in protected_branches_data:
        if not branch.get("allow_owner_manage_default_protection", True):
            compliance_score = 5
            return (
                compliance_score,
                "Compliant: Branch protection rules are enforced for administrators. This ensures that even privileged users cannot bypass important protections, keeping codebase integrity intact.",
            )

    return (
        0,
        "Non-compliant: Administrators can manage branch protection rules. This is risky because it allows highly privileged users to potentially disable protections, increasing the chances of unauthorized or malicious code being merged."
        " Consider disabling this option by unchecking 'Allow owners to manage default branch protection' to enforce stricter control over the protected branches.",
    )


def check_1_1_15_pushing_merging_restricted_to_trusted(protected_branches_data):
    """Ensure that only trusted individuals or teams are allowed to push or merge to protected branches."""
    compliance_score = 5
    non_compliant_branches = []

    for branch in protected_branches_data:
        push_access_levels = branch.get("push_access_levels", [])
        merge_access_levels = branch.get("merge_access_levels", [])
        force_push = branch.get("force_push", False)

        if force_push or not push_access_levels or not merge_access_levels:
            non_compliant_branches.append(branch["name"])
            compliance_score = 0

    if non_compliant_branches:
        message = f"Non-compliant: Force push is allowed or trusted users are not properly defined for branches: {', '.join(non_compliant_branches)}"
        return compliance_score, message
    else:
        return (
            5,
            "Compliant: Only trusted users can push and merge to protected branches.",
        )


def check_1_1_16_force_push_disabled(protected_branches_data):
    """Ensure force pushing is disabled for all protected branches in a GitLab repository."""

    if not protected_branches_data:
        return (
            0,
            "Non-compliant: No protected branches found. Please configure branch protections in the repository.",
        )

    for branch in protected_branches_data:
        if branch.get("allow_force_push", True):
            return (
                0,
                f"Non-compliant: Force push is allowed on branch '{branch['name']}'. Force pushing should be disabled to maintain code integrity.",
            )

    return 5, "Compliant: Force pushing is disabled for all protected branches."


def check_1_1_17_branch_deletion_denied(protected_branches_data):
    """Ensure that branch deletions are denied for protected branches."""
    if not protected_branches_data:
        return (
            0,
            "Non-compliant: No protected branches found. Ensure that protected branches have deletion protections enabled.",
        )

    for branch in protected_branches_data:
        if branch.get("allow_deletions", True):
            return (
                0,
                f"Non-compliant: Branch deletion is allowed for branch '{branch['name']}'. To maintain branch integrity, deletions should be denied for protected branches.",
            )

    return 5, "Compliant: Branch deletions are denied for all protected branches."


def check_1_1_18_scan_for_risks(approval_data):
    """Ensure that security scanners are enabled in approval settings."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Ensure that security scanning is enabled in the project's approval settings.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        num_scanners = len(scanners)

        if num_scanners >= 3:
            return (
                5,
                f"Compliant: {num_scanners} security scanners are enabled. The project is fully compliant.",
            )
        elif num_scanners == 2:
            return (
                3,
                f"Partially compliant: 2 security scanners are enabled. Consider adding additional scanners for enhanced security.",
            )
        elif num_scanners == 1:
            return (
                1,
                f"Minimally compliant: 1 security scanner is enabled. It is recommended to enable more scanners to improve security.",
            )

    return (
        0,
        "Non-compliant: No security scanners are enabled. Please enable security scanning in the project.",
    )


def check_1_1_19_audit_branch_protection_changes(audit_events):
    """
    Ensure that any changes to branch protection rules are audited.

    This check looks for relevant audit events to verify that branch protection changes
    are being tracked and logged for accountability. Branch protection rules help maintain
    the integrity of a repository, and logging changes ensures that unauthorized or unintended
    modifications are detected.
    """
    if not audit_events:
        return (
            0,
            "Non-compliant: No audit events found. Branch protection changes must be logged "
            "to ensure accountability. Please ensure that audit logging is enabled and capturing "
            "all important events, including branch protection updates.",
        )

    # change protected_branch_updated to look within the security API
    branch_protection_events = [
        event
        for event in audit_events
        if event.get("event_name") == "protected_branch_updated"
    ]

    if branch_protection_events:
        return (
            5,
            "Compliant: Changes to branch protection rules are properly audited. This ensures "
            "that any modifications to branch protection are logged and can be reviewed for security and compliance.",
        )

    return (
        0,
        "Non-compliant: No audit events found for branch protection rule changes. Please verify that changes "
        "to branch protection rules are being captured in the audit logs to ensure proper tracking and accountability.",
    )


def check_1_1_20_default_branch_protection(protected_branches_data, project_data):
    """Ensure branch protection is enforced on the default branch."""
    default_branch = project_data.get("default_branch")
    protected_branch_names = [branch.get("name") for branch in protected_branches_data]

    if default_branch in protected_branch_names:
        return (
            5,
            f"Compliant: The default branch '{default_branch}' is protected, ensuring that this critical branch is safeguarded from unauthorized or accidental changes.",
        )

    return (
        0,
        f"Non-compliant: The default branch '{default_branch}' is not protected. "
        "This means the primary branch could be vulnerable to unapproved changes. "
        "To remediate, ensure that the default branch is listed under the protected branches in the project settings, "
        "by navigating to 'Settings > Repository > Protected Branches' and adding the default branch.",
    )


"""1.2.X REPOSITORY MANAGEMENT"""


def check_1_2_1_security_md_file(gitlab_data, security_md_file):
    """Ensure all public repositories contain a SECURITY.md file."""
    visibility = gitlab_data.get("visibility", "private")

    if visibility != "public":
        return (
            5,
            "Compliant: This is a private repository, so a SECURITY.md file is not required.",
        )

    if security_md_file:
        return (
            5,
            "Compliant: SECURITY.md file is present in this public repository. This ensures that security vulnerabilities are properly reported and addressed.",
        )

    return (
        0,
        "Non-compliant: No SECURITY.md file found in this public repository. Please add a SECURITY.md file to the repository to provide guidance on how to report security issues.",
    )


def check_1_2_2_repository_creation_restricted(group_data):
    """
    Ensure repository creation is restricted to trusted users.
    This function checks the 'project_creation_level' from the group data to verify
    if only trusted users (e.g., Maintainers or Owners) can create repositories.
    """

    # Extract the project creation level
    project_creation_level = group_data.get("project_creation_level", None)

    # Define trusted roles that are allowed to create projects
    trusted_roles = ["maintainer", "owner"]

    if project_creation_level in trusted_roles:
        message = f"Compliant: Repository creation is restricted to trusted users ({project_creation_level})."
        return 5, message
    else:
        message = (
            f"Non-compliant: Repository creation is allowed for '{project_creation_level}', "
            "which is not a trusted role. Please restrict it to 'Maintainers' or 'Owners'."
        )
        return 0, message


def check_1_2_3_repository_deletion_limited(project_members):
    """
    Automatically fetch project members and their access levels, and list them for manual verification
    to ensure repository deletion is restricted to trusted users (Owners and Maintainers), excluding bots.
    """
    member_list = []

    for member in project_members:
        username = member.get("username")
        access_level = member.get("access_level")
        user_id = member.get("id")

        # Skip bot users based on username pattern
        if "bot" in username.lower():
            continue

        access_level_description = (
            "Owner"
            if access_level == 50
            else "Maintainer" if access_level == 40 else "Other"
        )
        member_list.append(
            {
                "username": username,
                "user_id": user_id,
                "access_level": access_level_description,
            }
        )

    # Provide the list of users and their access levels for manual review
    if member_list:
        message = "Review the following project members and their access levels to ensure that only trusted users can delete repositories:\n\n"
        for member in member_list:
            message += f"Username: {member['username']}, ID: {member['user_id']}, Access Level: {member['access_level']}\n"
    else:
        message = "No non-bot users found with high-level access."

    message += "\nManual verification required to determine if the number of powerful users is appropriate."

    return None, message


def check_1_2_4_issue_deletion_limited(project_members):
    """
    Automated check for listing project members along with their access levels to ensure that only Owners
    are allowed to delete issues. This function retrieves the members and their roles for manual verification.
    """
    if not project_members:
        return (
            None,
            "No members found. Please ensure that appropriate members are assigned for this project.",
        )

    message = "Please manually verify that only Owners are allowed to delete issues.\n"
    message += "Below is a list of current project members and their roles:\n"

    non_owner_members = []

    for member in project_members:
        access_level = member.get("access_level")
        member_info = f"- Name: {member.get('name', 'Unknown')}, ID: {member.get('id')}, Access Level: {access_level}\n"
        message += member_info
        
        # Collect members who are not Owners for review
        if access_level < 50:  # Access level 50 corresponds to "Owner"
            non_owner_members.append(member_info)

    if non_owner_members:
        message += "\n⚠️ The following members are not Owners but have access. Ensure they cannot delete issues:\n"
        message += "".join(non_owner_members)
    else:
        message += "\n✅ All members with access are Owners, which aligns with the requirement."

    message += (
        "\nManual check required: Ensure that only users with the 'Owner' role are allowed to delete issues.\n"
        "- Verify that no users with lower roles (e.g., Maintainers) have issue deletion permissions."
    )

    return None, message


def check_1_2_5_forks_tracked(forks_data):
    """List all forks of the repository for manual tracking and verification."""
    if forks_data:
        fork_list = "\n".join(
            [f"- {fork['name']} by {fork['owner']['username']}" for fork in forks_data]
        )
        message = (
            f"The following {len(forks_data)} forks are tracked:\n{fork_list}\n"
            "Please ensure that all forks are authorized and accounted for."
        )
        return None, message

    return (
        None,
        "No forks found for this project. All copies of the code are accounted for.",
    )


def check_1_2_6_visibility_change_tracked(audit_events):
    """Ensure visibility changes are tracked in audit events."""
    if isinstance(audit_events, list):
        return (
            5,
            "Compliant: Ability to track visibility changes detected. This ensures that any changes to repository visibility are recorded and monitored.",
        )

    return (
        0,
        "Non-compliant: Unable to retrieve audit events or tracking is not enabled. Please ensure that visibility changes are logged to track who modifies the repository's visibility.",
    )


def check_1_2_7_inactive_repository(branches_data):
    """Ensure the 'main' or 'master' branch has been updated within the last 6 months."""
    six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)


    main_branch = branches_data if branches_data["name"] in ["main", "master"] else None


    if not main_branch:
        return (
            0,
            "Non-compliant: No 'main' or 'master' branch found. Ensure the repository has a 'main' or 'master' branch.",
        )

    # Handle cases where commit data might be missing
    commit_data = main_branch.get("commit")
    if not commit_data or "committed_date" not in commit_data:
        return (
            0,
            f"Non-compliant: No commit information found for the '{main_branch['name']}' branch. Ensure the branch is properly maintained.",
        )

    # Parse the last commit date
    last_commit_date = dateutil_parser.parse(commit_data["committed_date"])

    # Check if the commit date is set in the future
    if last_commit_date > datetime.now(timezone.utc):
        return (
            0,
            f"Non-compliant: The '{main_branch['name']}' branch has a commit set in the future ('{last_commit_date}'). Please correct the commit date.",
        )

    # Check if the branch was updated within the last 6 months
    if last_commit_date < six_months_ago:
        return (
            0,
            f"Non-compliant: The '{main_branch['name']}' branch has not been updated in the last 6 months. Last commit was on {last_commit_date}.",
        )

    return (
        5,
        f"Compliant: The '{main_branch['name']}' branch has been updated within the last 6 months (Last commit on {last_commit_date}). This ensures the branch is actively maintained.",
    )


"""1.3.X CONTRIBUTION ACCESS"""


def check_1_3_1_inactive_project_users(project_events):
    """Check if there are inactive users in a project based on their contributions in the last 6 months."""
    six_months_ago = datetime.now() - timedelta(days=180)
    inactive_users = set()
    active_users = set()

    if not project_events:
        return None, "No project events found. Unable to determine user activity."

    for event in project_events:
        user = event.get("author", {})
        user_name = user.get("name", "Unknown")
        user_last_activity = event.get("created_at", None)

        if user_last_activity:
            last_activity_date = datetime.strptime(
                user_last_activity, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if last_activity_date < six_months_ago:
                inactive_users.add(user_name)
            else:
                active_users.add(user_name)

    inactive_users = inactive_users - active_users
    if inactive_users:
        user_list = ", ".join(inactive_users)
        return (
            0,
            f"Found inactive users: {user_list}. Consider removing or reviewing these users.",
        )

    return (
        5,
        "No inactive users found. All users have been active in the last 6 months.",
    )


def check_1_3_2_limit_top_level_group_creation(group_data):
    """Check and list the project and subgroup creation levels in a group."""
    project_creation_level = group_data.get("project_creation_level", "Unknown")
    subgroup_creation_level = group_data.get("subgroup_creation_level", "Unknown")

    message = (
        f"Project Creation Level: {project_creation_level}\n"
        f"Subgroup Creation Level: {subgroup_creation_level}\n\n"
        "Manual verification required: Ensure that project and subgroup creation is limited to specific, trusted users."
    )

    return None, message


def check_1_3_3_minimum_number_of_administrators(group_members):
    """Check to ensure the minimum number of administrators is set for the organization."""

    admins = [member for member in group_members if member["access_level"] in [40, 50]]

    # Create a list of admin names and their access levels
    admin_list = "\n".join(
        [
            f"{admin['username']} (Access Level: {admin['access_level']})"
            for admin in admins
        ]
    )

    message = (
        f"Administrators found in the group:\n\n{admin_list}\n\n"
        "Ensure that only the minimum number of administrators is set for the organization."
        "- Navigate to 'Manage > Members' in the project settings.\n"
        "- Review the list of members with the 'Owner' or 'Maintainer' role and remove unnecessary administrators."
    )

    return None, message


def check_1_3_4_mfa_for_contributors(group_settings):
    """Check whether MFA is enforced for contributors using the GitLab API."""
    # Check if 'require_two_factor_authentication' is enabled
    mfa_enabled = group_settings.get("require_two_factor_authentication", False)

    if mfa_enabled:
        score = 5
        message = "Compliant: MFA is enforced for contributors."
    else:
        score = 0
        message = (
            "Non-compliant: MFA is not enforced for contributors.\n"
            "- Navigate to Admin Area > Settings > General.\n"
            "- Check if the 'Enforce two-factor authentication' option is enabled."
        )

    return score, message


def check_1_3_5_mfa_enforcement(group_settings):
    """Check whether MFA is enforced for the Organization"""
    # Check if 'require_two_factor_authentication' is enabled
    mfa_enabled = group_settings.get("require_two_factor_authentication", False)

    if mfa_enabled:
        score = 5
        message = "Compliant: MFA is enforced for contributors."
    else:
        score = 0
        message = (
            "Non-compliant: MFA is not enforced for contributors.\n"
            "- Navigate to Admin Area > Settings > General.\n"
            "- Check if the 'Enforce two-factor authentication' option is enabled."
        )

    return score, message


def check_1_3_6_company_approved_email(group_data):
    """Check if company-approved email domains are enforced for the group."""

    # Extract the allowed email domains list
    allowed_email_domains = group_data.get("allowed_email_domains_list", None)

    if allowed_email_domains:
        # If there are allowed domains, list them and mark as compliant
        domains = ", ".join(allowed_email_domains)
        message = (
            f"Compliant: Company-approved email domains are enforced. "
            f"The following domains are allowed: {domains}."
        )
        return 5, message  # Compliant with a score of 5
    else:
        # If no allowed domains are set, mark as not compliant
        message = (
            "Not compliant: No company-approved email domains are enforced. "
            "Please set the allowed domains under group settings."
        )
        return 0, message  # Not compliant with a score of 0


def check_1_3_7_two_administrators_per_repository(project_members):
    """Check if there are exactly two users with administrative permissions for the repository."""
    admin_users = [
        member for member in project_members if member.get("access_level") >= 40
    ]

    if len(admin_users) == 2:
        return (
            5,
            f"Compliant: There are exactly two users with administrative permissions: {', '.join([user['username'] for user in admin_users])}.",
        )
    elif len(admin_users) < 2:
        return (
            2,
            f"Non-compliant: Fewer than two users with administrative permissions found: {', '.join([user['username'] for user in admin_users])}.",
        )
    else:
        return (
            0,
            f"Non-compliant: More than two users with administrative permissions found: {', '.join([user['username'] for user in admin_users])}.",
        )


def check_1_3_8_strict_base_permissions(project_members):
    """Ensure strict base permissions are set for the organization or project repository."""
    strict_access_levels = [10, 20]  # Guest (10), Reporter (20)
    non_compliant_users = []

    for member in project_members:
        if member.get("access_level") not in strict_access_levels:
            non_compliant_users.append(member["username"])

    if non_compliant_users:
        return (
            0,
            f"Non-compliant: Users with higher than 'Reporter' permissions: {', '.join(non_compliant_users)}. Ensure strict base permissions are enforced.",
        )

    return 5, "Compliant: All users have strict base permissions."


def check_1_3_9_verified_domain():
    """Manual check to ensure the organization's identity is confirmed with a 'Verified' badge."""
    message = (
        "Manual check required: Ensure the organization's identity is confirmed with a 'Verified' badge.\n"
        "- Navigate to the group settings under 'Settings > Domain Verification'.\n"
        "- Check if the organization's domains have the 'Verified' badge."
    )
    return None, message


def check_1_3_10_scm_email_notifications_restricted_to_verified_domains():
    """Manual check to ensure SCM email notifications are restricted to verified domains."""
    message = (
        "Manual check required: Ensure Source Code Management (SCM) email notifications are restricted to verified domains.\n"
        "- Navigate to 'Settings > Domain Verification' in the Admin Area.\n"
        "- Ensure that email notifications are only sent to verified domains."
    )
    return None, message


def check_1_3_11_ssh_certificates_enforcement():
    """Manual check to ensure SSH certificates and SSH key restrictions are enforced."""
    message = (
        "Manual check required: Ensure SSH certificates are enforced and SSH key restrictions are in place.\n"
        "- Navigate to Admin Area > Settings > General.\n"
        "- Ensure restrictions on SSH key types and lengths are enforced."
    )
    return None, message


def check_1_3_12_ip_restrictions(is_self_managed, ip_restrictions):
    """
    Check to ensure Git access is restricted based on IP addresses.
    """
    if is_self_managed:
        # Automated check with scoring
        if ip_restrictions:
            return (
                5,
                f"Compliant: IP access is restricted to the following IP ranges: {ip_restrictions}.",
            )
        else:
            return 0, "Non-compliant: No IP restrictions found."

    # Manual check if not self-managed
    message = (
        "Manual check required: Ensure IP restrictions are enforced.\n"
        "- Navigate to 'Settings > General' for the group.\n"
        "- Check the 'Restrict access by IP address' field."
    )
    return None, message


def check_1_3_13_code_anomalies(project_events):
    """Check for anomalous code pushes outside typical working hours."""
    working_hours_start = 5
    working_hours_end = 20
    anomalies_found = False

    if not project_events:
        return (
            None,
            "No events found or failed to fetch events. Unable to detect code anomalies.",
        )

    for event in project_events:
        if event.get("action_name") == "pushed to":
            event_time = datetime.strptime(
                event.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if (
                event_time.hour < working_hours_start
                or event_time.hour >= working_hours_end
            ):
                anomalies_found = True
                break

    if anomalies_found:
        return (
            None,
            "Anomaly detected: Code push occurred outside of working hours. Investigate the event to ensure compliance.",
        )

    return (
        None,
        "Compliant: No anomalies detected. All code pushes occurred within typical working hours.",
    )


"""1.4.X THIRD-PARTY"""


def check_1_4_1_admin_approval_for_installed_apps(installed_apps):
    """Ensure administrator approval is required for installed applications."""
    if not installed_apps:
        return (
            5,
            "Compliant: No installed applications found. This ensures that no third-party applications have access without administrator approval.",
        )

    app_names = [app['name'] for app in installed_apps]
    return (
        None,
        f"Manual review needed: Found installed applications: {', '.join(app_names)}. Ensure administrator approval is required for all installed applications.",
    )


def check_1_4_2_stale_applications(installed_apps):
    """Ensure stale applications are reviewed and inactive ones are removed."""
    if installed_apps:
        app_names = [app['name'] for app in installed_apps]
        return (
            None,
            f"Manual review needed: Found installed applications: {', '.join(app_names)}. Ensure stale or inactive applications are removed.",
        )

    return (
        5,
        "Compliant: No installed applications found. All applications are accounted for.",
    )


def check_1_4_3_least_privilege_for_installed_apps(installed_apps):
    """Ensure installed applications are granted the least privilege required."""
    if not installed_apps:
        return (
            5,
            "Compliant: No installed applications found. This ensures that no unnecessary permissions are granted to third-party apps.",
        )

    app_names = [app['name'] for app in installed_apps]
    return (
        None,
        f"Manual review needed: Found installed applications: {', '.join(app_names)}. Ensure they follow the principle of least privilege.",
    )


def check_1_4_4_secure_webhooks(webhooks):
    """Ensure only secured webhooks (https and SSL verification) are used."""
    compliance_score = 5
    non_compliant_hooks = []

    if not webhooks:
        return (
            compliance_score,
            "Compliant: No webhooks found. This ensures no external services are configured to interact with the repository.",
        )

    for webhook in webhooks:
        if not webhook["url"].startswith("https://") or not webhook.get(
            "enable_ssl_verification", False
        ):
            non_compliant_hooks.append(webhook["url"])

    if non_compliant_hooks:
        return (
            0,
            f"Non-compliant: Found insecure webhooks: {', '.join(non_compliant_hooks)}. Ensure all webhooks use HTTPS and have SSL verification enabled.",
        )

    return (
        compliance_score,
        "Compliant: All webhooks are secure and use HTTPS with SSL verification.",
    )


"""1.5.X CODE RISKS"""


def check_1_5_1_secret_detection_enabled(approval_data):
    """Check if secret detection scanner is enabled in approval settings."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Ensure secret detection is enabled in the project's approval settings.",
        )

    for rule in approval_data["rules"]:
        # Get the list of scanners for the rule
        scanners = rule.get("scanners", [])
        if "secret_detection" in scanners:
            return (
                5,
                "Compliant: Secret detection is enabled in the project's approval settings.",
            )

    return (
        0,
        "Non-compliant: Secret detection is not enabled. Please ensure secret detection scanning is configured in the project's approval settings.",
    )


def check_1_5_2_ci_configuration_file_exists(repo_tree, project_data):
    """Check if a CI configuration file exists in the repository."""
    project_name = project_data.get("path_with_namespace", "unknown_project")

    if repo_tree:
        return (
            5,
            f"Compliant: CI configuration file exists. Review the CI configuration at: https://gitlab.com/{project_name}/-/blob/main/.gitlab-ci.yml",
        )
    else:
        return (
            0,
            "Non-compliant: No CI configuration file found. Please ensure a CI configuration file is present in the repository.",
        )


def check_1_5_3_iac_scanner_in_approval_settings(approval_data):
    """Check if Infrastructure as Code (IaC) scanning is enabled in the project's approval settings."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Please verify Infrastructure as Code (IaC) scanning manually.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "iac_scanning" in scanners:
            return (
                5,
                "Compliant: Infrastructure as Code (IaC) scanning is enabled in the project's approval settings.",
            )

    return (
        0,
        "Non-compliant: Infrastructure as Code (IaC) scanning is not enabled. Please enable IaC scanning in the CI pipeline configuration.",
    )


def check_1_5_4_sast_scanning_enabled(approval_data):
    """Check if SAST (Static Application Security Testing) is enabled in the approval settings."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Please ensure SAST scanning is enabled for code vulnerabilities.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "sast" in scanners:
            return 5, "Compliant: SAST scanning is enabled for code vulnerabilities."

    return (
        0,
        "Non-compliant: SAST scanning is not enabled. Please ensure SAST is configured and running for code vulnerabilities.",
    )


def check_1_5_5_dependency_scanning_enabled(approval_data):
    """Check if Dependency Scanning is enabled in the project approval settings."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Please ensure Dependency Scanning is enabled for project dependencies.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "dependency_scanning" in scanners:
            return 5, "Compliant: Dependency Scanning is enabled in the project."

    return (
        0,
        "Non-compliant: Dependency Scanning is not enabled. Please enable Dependency Scanning in the project.",
    )



def check_1_5_6_license_scanning_enabled(approval_data):
    """
    Check if the dependency scanner is enabled according to the approval settings.

    Args:
        approval_data (dict): Approval settings data from GitLab API.

    Returns:
        tuple: (int, str) Compliance score and a compliance message.
    """
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Please ensure Dependency Scanning is enabled for project dependencies.",
        )

    for rule in approval_data.get("rules", []):
        scanners = rule.get("scanners", [])
        if "dependency_scanning" in scanners:
            return (
                5,
                "Compliant: Dependency Scanning is enabled according to the approval settings."
            )

    return (
        0,
        "Non-compliant: Dependency Scanning is not enabled according to the approval settings. "
        "Please enable it in the project settings."
    )

def check_1_5_7_dast_scanner(approval_data):
    """Check if the DAST (Dynamic Application Security Testing) scanner is enabled in approval settings."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Please ensure DAST scanning is enabled for dynamic vulnerabilities.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "dast" in scanners:
            return 5, "Compliant: DAST scanning is enabled for dynamic vulnerabilities."

    return (
        0,
        "Non-compliant: DAST scanning is not enabled. Please ensure DAST scanning is enabled in the project.",
    )


def check_1_5_8_dast_api_scanner(approval_data):
    """Check if DAST-API security scanning is enabled in the approval settings for the project."""
    if not approval_data or "rules" not in approval_data:
        return (
            0,
            "Non-compliant: No approval rules found. Please ensure DAST-API scanning is enabled for API security vulnerabilities.",
        )

    for rule in approval_data["rules"]:
        scanners = rule.get("scanners", [])
        if "api_fuzzing" in scanners or "dast_api" in scanners:
            return (
                5,
                "Compliant: DAST-API scanner is enabled for API runtime security weaknesses.",
            )

    return (
        0,
        "Non-compliant: DAST-API scanner is not enabled. Please enable DAST-API scanning in the project.",
    )


"""Runs every check"""


async def run_all_checks(
    project_data,
    approval_settings_data,
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
    approvals_data,
    group_settings,
    group_members,
    main_branch,
):
    """Run all the checks defined in this file using run_checks from common_utils."""

    ### False = Automated, True = Manual, and Manual sometimes

    checks = [
        (check_1_1_1_version_control_tracking, [], False),  # Automated
        (
            check_1_1_2_jira_integration_and_requirements,
            [project_data, jira_data],
            False,
        ),  # Automated
        (
            check_1_1_3_strongly_authenticated_approval,
            [approval_settings_data],
            False,
        ),  # Automated
        (check_1_1_4_remove_approvals_link, [approvals_data], True),
        (
            check_1_1_5_restrict_dismissal_of_code_reviews,
            [protected_branches_data],
            True,
        ),
        (check_1_1_6_codeowners_configuration, [codeowners_data], False),
        (
            check_1_1_7_codeowners_review_required,
            [codeowners_data, protected_branches_data],
            False,
        ),
        (check_1_1_8_inactive_branches, [branches_data], False),
        (check_1_1_9_all_checks_passed_before_merge, [protected_branches_data], False),
        (check_1_1_10_branches_up_to_date, [project_data], False),
        (check_1_1_11_all_comments_resolved, [project_data], False),
        (check_1_1_12_signed_commits_required, [push_rules], False),
        (check_1_1_13_linear_history_required, [project_data], False),
        (check_1_1_14_branch_protection_for_admins, [protected_branches_data], False),
        (
            check_1_1_15_pushing_merging_restricted_to_trusted,
            [protected_branches_data],
            False,
        ),
        (check_1_1_16_force_push_disabled, [protected_branches_data], False),
        (check_1_1_17_branch_deletion_denied, [protected_branches_data], False),
        (check_1_1_18_scan_for_risks, [approval_settings_data], False),
        (check_1_1_19_audit_branch_protection_changes, [audit_events], False),
        (
            check_1_1_20_default_branch_protection,
            [protected_branches_data, project_data],
            False,
        ),
        (check_1_2_1_security_md_file, [project_data, security_md_file], False),
        (check_1_2_2_repository_creation_restricted, [group_settings], False),
        (check_1_2_3_repository_deletion_limited, [project_members], True),
        (check_1_2_4_issue_deletion_limited, [project_members], True),
        (check_1_2_5_forks_tracked, [forks_data], True),
        (check_1_2_6_visibility_change_tracked, [audit_events], False),
        (check_1_2_7_inactive_repository, [main_branch], False),
        (check_1_3_1_inactive_project_users, [project_events], True),
        (check_1_3_2_limit_top_level_group_creation, [group_settings], True),
        (check_1_3_3_minimum_number_of_administrators, [group_members], True),
        (check_1_3_4_mfa_for_contributors, [group_settings], False),
        (check_1_3_5_mfa_enforcement, [group_settings], False),  # Automated
        (check_1_3_6_company_approved_email, [group_settings], False),
        (
            check_1_3_7_two_administrators_per_repository,
            [project_members],
            False,
        ),
        (check_1_3_8_strict_base_permissions, [project_members], False),  # Manual
        (check_1_3_9_verified_domain, [], True),
        (
            check_1_3_10_scm_email_notifications_restricted_to_verified_domains,
            [],
            True,
        ),
        (check_1_3_11_ssh_certificates_enforcement, [], True),
        (
            check_1_3_12_ip_restrictions,
            [is_self_managed, check_ip_restrictions],
            True,
        ),  # Manual sometimes
        (check_1_3_13_code_anomalies, [project_events], False),
        (
            check_1_4_1_admin_approval_for_installed_apps,
            [installed_apps],
            True,
        ),
        (check_1_4_2_stale_applications, [installed_apps], True),
        (
            check_1_4_3_least_privilege_for_installed_apps,
            [installed_apps],
            True,
        ),
        (check_1_4_4_secure_webhooks, [webhooks], False),
        (
            check_1_5_1_secret_detection_enabled,
            [approval_settings_data],
            False,
        ),
        (
            check_1_5_2_ci_configuration_file_exists,
            [repo_tree, project_data],
            False,
        ),
        (
            check_1_5_3_iac_scanner_in_approval_settings,
            [approval_settings_data],
            False,
        ),
        (check_1_5_4_sast_scanning_enabled, [approval_settings_data], False),
        (
            check_1_5_5_dependency_scanning_enabled,
            [approval_settings_data],
            False,
        ),
        (
            check_1_5_6_license_scanning_enabled,
            [approval_settings_data],
            False,
        ),
        (check_1_5_7_dast_scanner, [approval_settings_data], False),
        (check_1_5_8_dast_api_scanner, [approval_settings_data], False),
    ]

    # Use run_checks to execute all the checks
    return run_checks(checks, context_name="Source Code Compliance Checks")
