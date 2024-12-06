#!/usr/bin/env python3

import click
import os
import asyncio
import json
import csv
from recommendations.gitlab.source_code import run_all_checks as source_code_checks
from recommendations.gitlab.build_pipelines import (
    run_all_checks as build_pipeline_checks,
)
from recommendations.gitlab.dependencies import run_all_checks as dependency_checks
from recommendations.gitlab.artifacts import run_all_checks as artifact_checks

from services.gitlab_service import (
    fetch_gitlab_data,
    fetch_merge_requests,
    fetch_codeowners_file,
    fetch_approval_settings,
    fetch_protected_branches,
    fetch_branches,
    fetch_jira_integration,
    fetch_push_rules,
    fetch_audit_events,
    fetch_security_md_file,
    fetch_forks_data,
    fetch_project_events,
    fetch_project_members,
    fetch_is_self_managed,
    fetch_check_ip_restrictions,
    fetch_installed_applications,
    fetch_project_webhooks,
    fetch_gitlab_config,
    fetch_latest_pipeline_jobs,
    fetch_repository_tree,
    fetch_job_logs,
    fetch_environments,
    fetch_gitlab_runners,
    fetch_gitlab_commit_history,
    fetch_release_artifacts,
    fetch_dependency_files,
    fetch_pipeline_artifacts,
    fetch_sbom_artifacts,
    fetch_group_push_rules,
    fetch_security_scanning,
    fetch_license_scanning,
    fetch_group_settings,
)

# Global variable to hold fetched data
global_data = {}


def fetch_all_gitlab_data(project_id, token):
    """Helper function to fetch all necessary GitLab data."""

    gitlab_data = fetch_gitlab_data(project_id, token)
    global_data["gitlab_data"] = gitlab_data

    # Extract group_id
    group_id = gitlab_data.get("namespace", {}).get("id")

    # Check if self-managed
    is_self_managed = fetch_is_self_managed(token)
    global_data["is_self_managed"] = is_self_managed

    group_settings = fetch_group_settings(group_id, token)
    global_data["group_settings"] = group_settings

    fetch_funcs = {
        "approval_data": fetch_approval_settings,
        "merge_requests": fetch_merge_requests,
        "codeowners_data": fetch_codeowners_file,
        "protected_branches_data": fetch_protected_branches,
        "branches_data": fetch_branches,
        "jira_data": fetch_jira_integration,
        "push_rules": fetch_push_rules,
        "audit_events": fetch_audit_events,
        "security_md_file": lambda proj_id, tok: fetch_security_md_file(
            proj_id, tok, branch="master"
        ),
        "forks_data": fetch_forks_data,
        "project_events": fetch_project_events,
        "project_members": fetch_project_members,
        "check_ip_restrictions": lambda proj_id, tok: (
            fetch_check_ip_restrictions(group_id, tok) if is_self_managed else None
        ),
        "installed_apps": fetch_installed_applications,
        "webhooks": fetch_project_webhooks,
        "gitlab_config": lambda proj_id, tok: fetch_gitlab_config(
            proj_id, tok, branch="master"
        ),
        "pipeline_jobs": lambda proj_id, tok: fetch_latest_pipeline_jobs(
            proj_id, tok, num_jobs=10
        ),
        "pipeline_ids": lambda proj_id, tok: [
            job["pipeline"]["id"]
            for job in fetch_latest_pipeline_jobs(proj_id, tok, num_jobs=10)
        ],
        # "repo_tree": lambda proj_id, tok: fetch_repository_tree(
        #     proj_id, tok, ref="master"
        # ),
        "job_logs": lambda proj_id, tok: [
            fetch_job_logs(proj_id, tok, job["id"])
            for job in fetch_latest_pipeline_jobs(proj_id, tok, num_jobs=1)
        ],
        "environments": fetch_environments,
        "runners": fetch_gitlab_runners,
        "commit_history": lambda proj_id, tok: fetch_gitlab_commit_history(
            proj_id, tok, file_path=".gitlab-ci.yml"
        ),
        "artifacts": fetch_release_artifacts,
        "dependency_files": lambda proj_id, tok: fetch_dependency_files(
            proj_id, tok, branch="master"
        ),
        "job_artifacts": lambda proj_id, tok: {
            job["pipeline"]["id"]: fetch_pipeline_artifacts(proj_id, tok, job["id"])
            for job in fetch_latest_pipeline_jobs(proj_id, tok, num_jobs=10)
        },
        "sbom_artifacts": fetch_sbom_artifacts,
        "group_push_rules": lambda proj_id, tok: fetch_group_push_rules(group_id, tok),
        "security_scan_data": fetch_security_scanning,
        "license_scanning": fetch_license_scanning,
    }

    for key, func in fetch_funcs.items():
        if key != "gitlab_data":
            global_data[key] = func(project_id, token)


def export_results(results, output_format):
    """Export results to the specified format (CSV or JSON)."""
    filename = f"results.{output_format}"
    if output_format == "json":
        with open(filename, "w") as json_file:
            json.dump(results, json_file, indent=4)
    elif output_format == "csv":
        with open(filename, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Check", "Compliance Score"])
            for check, score in results.items():
                writer.writerow([check, score])
    click.echo(f"Results saved as '{filename}'.")


@click.group()
def cli():
    """CLI for Security Recommendations."""
    global global_data

    # Load environment variables
    token = os.getenv("GITLAB_TOKEN")
    project_id = os.getenv("PROJECT_ID")

    if not token or not project_id:
        raise Exception("GITLAB_TOKEN or PROJECT_ID is missing.")

    # Fetch GitLab data once using a helper function
    fetch_all_gitlab_data(project_id, token)


@cli.command()
@click.option(
    "--output",
    type=click.Choice(["json", "csv"], case_sensitive=False),
    default="csv",  # Default to csv if no option is provided
    help="Output format for results: 'json' or 'csv'. Defaults to 'csv'.",
)
def check_gitlab(output):
    """Run GitLab-specific security checks and optionally export results."""
    click.echo("Running GitLab checks...")

    token = os.getenv("GITLAB_TOKEN")
    project_id = os.getenv("PROJECT_ID")

    # Run the async function using asyncio.run
    source_code_results = asyncio.run(
        source_code_checks(
            global_data["gitlab_data"],
            global_data["approval_data"],
            global_data["codeowners_data"],
            global_data["protected_branches_data"],
            global_data["branches_data"],
            global_data["jira_data"],
            global_data["push_rules"],
            global_data["audit_events"],
            global_data["security_md_file"],
            global_data["forks_data"],
            global_data["project_events"],
            global_data["project_members"],
            global_data["is_self_managed"],
            global_data["check_ip_restrictions"],
            global_data["installed_apps"],
            global_data["webhooks"],
            global_data["gitlab_config"],
        )
    )

    build_pipeline_results = asyncio.run(
        build_pipeline_checks(
            global_data["pipeline_jobs"],
            # global_data["repo_tree"],
            global_data["job_logs"],
            project_id,
            token,
            global_data["environments"],
            global_data["project_members"],
            global_data["gitlab_config"],
            global_data["webhooks"],
            global_data["runners"],
            global_data["commit_history"],
            global_data["approval_data"],
            global_data["artifacts"],
            global_data["dependency_files"],
            global_data["job_artifacts"],
            global_data["pipeline_ids"],
        )
    )

    dependency_results = asyncio.run(
        dependency_checks(
            global_data["dependency_files"],
            global_data["job_artifacts"],
            global_data["approval_data"],
            global_data["sbom_artifacts"],
            global_data["group_push_rules"],
            global_data["gitlab_config"],
            global_data["security_scan_data"],
            global_data["license_scanning"],
        )
    )

    artifact_results = asyncio.run(
        artifact_checks(
            global_data["job_artifacts"],
            global_data["project_members"],
            global_data["group_settings"],
            global_data["gitlab_data"],
            global_data["webhooks"],
        )
    )

    combined_results = {
        **source_code_results,
        **build_pipeline_results,
        **dependency_results,
        **artifact_results,
    }

    # If an output format is specified, export the results
    export_results(combined_results, output)


if __name__ == "__main__":
    cli()
