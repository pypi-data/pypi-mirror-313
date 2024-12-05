from mobicontrol.cli import mobicontrol
import click
import yaml
import json
from mobicontrol.client.policies import (
    get_policies,
    create_policy,
    set_apps,
    set_assignments,
    delete_policy,
)
from mobicontrol.client.apps import upload_app
import requests
import base64
import os


def get_github_release_asset(
    owner: str, repo: str, tag: str, filename: str = ".apk"
) -> tuple[str, bytes]:
    github_token = os.environ.get("GITHUB_TOKEN")

    if github_token is None:
        raise click.ClickException(
            "GITHUB_TOKEN environment variable is required when using github-release source type."
        )

    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
        },
    )

    if resp.status_code != 200:
        raise click.ClickException(
            f"Could not fetch release from GitHub: {resp.text}",
        )

    release = resp.json()

    resp = requests.get(
        release["assets_url"],
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
        },
    )

    if resp.status_code != 200:
        raise click.ClickException(
            f"Could not fetch assets from GitHub release: {resp.text}",
        )

    releases = resp.json()

    for asset in releases:
        if filename in asset["name"]:
            asset = asset
            break
    else:
        raise click.ClickException(f"Could not find asset matching '{filename}'.")

    resp = requests.get(
        asset["url"],
        headers={
            "Accept": "application/octet-stream",
            "Authorization": f"Bearer {github_token}",
        },
    )

    if resp.status_code != 200:
        raise click.ClickException(
            f"Could not fetch asset from GitHub release: {resp.text}",
        )

    return asset["name"], base64.b64encode(resp.content)


def apply_apps(ctx, policy_id: str, apps: list[dict]):
    for app in apps:
        if "source" in app:
            if app["source"]["type"] == "github-release":
                filename, file = get_github_release_asset(
                    app["source"]["owner"],
                    app["source"]["repo"],
                    app["source"]["tag"],
                    app["source"].get("filename", ".apk"),
                )

                app["ReferenceId"] = upload_app(ctx.obj, filename, file)["ReferenceId"]

            if app["source"]["type"] == "mobicontrol":
                app["ReferenceId"] = app["source"]["referenceId"]

    payload = [
        {
            "ReferenceId": app.get("ReferenceId"),
            "IsMandatory": app.get("mandatory", True),
            "AppPriority": app.get("priority", 1),
            "AppConfiguration": json.dumps(app.get("config", {})),
        }
        for app in apps
    ]

    set_apps(ctx.obj, policy_id, payload)
    click.echo(f"Assigned {len(payload)} apps to policy.")


def apply_policy(ctx, manifest: dict):
    meta: dict = manifest["metadata"]
    try:
        policies = get_policies(ctx.obj, meta["name"])

        for policy in policies:
            if policy["Name"] == meta["name"]:
                policy = policy
                click.echo(f"Found existing policy with name {meta['name']}.")
                break
        else:
            policy = create_policy(
                ctx.obj, meta["name"], meta["kind"], meta.get("description", "")
            )
            click.echo(f"Created new policy with name {meta['name']}.")
    except Exception as e:
        raise click.ClickException(str(e))

    apps = manifest.get("apps", [])

    try:
        apply_apps(ctx, policy["ReferenceId"], apps)

        assignment_groups = manifest.get("assignmentGroups", [])
        set_assignments(ctx.obj, policy["ReferenceId"], assignment_groups)
        click.echo(f"Assigned policy to {len(assignment_groups)} device groups.")
    except Exception as e:
        raise click.ClickException(str(e))


def delete_policy_manifest(ctx, manifest: dict):
    meta = manifest["metadata"]
    try:
        policies = get_policies(ctx.obj, meta["name"])

        for policy in policies:
            if policy["Name"] == meta["name"]:
                policy = policy
                break
        else:
            raise click.ClickException(
                f"Could not find policy with name {meta['name']}"
            )
    except Exception as e:
        raise click.ClickException(str(e))

    try:
        delete_policy(ctx.obj, policy["ReferenceId"])
    except Exception as e:
        raise click.ClickException(str(e))


def get_files(path: str) -> list[str]:
    if os.path.isdir(path):
        paths: list[str] = []
        for root, dirs, files in os.walk(path):
            for file in files:
                paths.append(os.path.join(root, file))
        return paths
    else:
        return [path]


@mobicontrol.command()
@click.option("--file", type=click.Path(exists=True), required=True)
@click.pass_context
def apply(ctx, file: str):
    apply_paths = get_files(file)

    click.echo(f"Found {len(apply_paths)} files to apply.")
    for file in apply_paths:
        click.echo(f"Applying {file}.")
        with open(file) as f:
            data = yaml.safe_load(f)

        if data["resourceType"] == "policy":
            apply_policy(ctx, data)

        click.echo(f"{file} applied.")


@mobicontrol.command()
@click.option("--file", type=click.Path(exists=True), required=True)
@click.pass_context
def delete(ctx, file: str):
    apply_paths = get_files(file)

    click.echo(f"Found {len(apply_paths)} files to delete.")
    for file in apply_paths:
        with open(file) as f:
            data = yaml.safe_load(f)

        if data["resourceType"] == "policy":
            try:
                delete_policy_manifest(ctx, data)
                click.echo(f"Deleted {file}.")
            except Exception as e:
                click.echo(str(e))
