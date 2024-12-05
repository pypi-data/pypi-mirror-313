from mobicontrol.cli import mobicontrol
from mobicontrol.client.policies import (
    get_policies,
    create_policy,
    delete_policy,
    get_policy,
    add_app,
    get_apps,
    remove_app,
    get_assignments,
    assign_device_group,
    unassign_device_group,
)
import click
import json
from typing import Optional


@mobicontrol.group()
@click.option("--id", type=str, required=False)
@click.pass_context
def policy(ctx, id: Optional[str] = None):
    pass


@policy.command()
@click.pass_context
def list(ctx):
    try:
        policies = get_policies(ctx.obj)
    except Exception as e:
        raise click.ClickException(str(e))

    click.echo(json.dumps(policies))


@policy.command()
@click.option("--id", type=str, required=True)
@click.pass_context
def show(ctx, id: str):
    try:
        policy = get_policy(ctx.obj, id)
    except Exception as e:
        raise click.ClickException(f"Could not fetch policy. {e}")

    click.echo(json.dumps(policy))


@policy.command()
@click.option("--name", type=str, required=True)
@click.option("--kind", type=click.types.Choice(["ManagedGooglePlay"]), required=True)
@click.option("--description", type=str)
@click.pass_context
def create(ctx, name: str, kind: str, description: str = ""):
    try:
        policies = get_policies(ctx.obj, name_contains=name)
    except Exception as e:
        raise click.ClickException(f"Could not fetch policies. {e}")

    if len(policies) == 1:
        policy = policies[0]
    elif len(policies) > 1:
        raise click.ClickException(f"Found more than one policy with name {name}")
    else:
        policy = create_policy(ctx.obj, name, kind, description)

    click.echo(json.dumps(policy))


@policy.command()
@click.option("--id", type=str, required=True)
@click.pass_context
def delete(ctx, id: str):
    try:
        delete_policy(ctx.obj, id)
    except Exception as e:
        raise click.ClickException(f"Could not delete policy. {e}")


@policy.group()
def app():
    pass


@app.command("list")
@click.option("--id", type=str, required=True)
@click.pass_context
def list_apps(ctx, id: str):
    apps = get_apps(ctx.obj, id)

    click.echo(json.dumps(apps))


@app.command("create")
@click.option("--id", type=str, required=True)
@click.option("--app", type=str, required=True)
@click.option("--config", type=str, required=False)
@click.pass_context
def create_app(
    ctx, id: str, app: str, config: Optional[str] = None, remove: bool = False
):
    try:
        add_app(ctx.obj, id, app, config)
    except Exception as e:
        raise click.ClickException(f"Could not add app to policy. {e}")


@app.command("delete")
@click.option("--id", type=str, required=True)
@click.option("--app", type=str, required=True)
@click.pass_context
def delete_app(ctx, id: str, app: str):
    try:
        remove_app(ctx.obj, id, app)
    except Exception as e:
        raise click.ClickException(f"Could not remove app from policy. {e}")


@policy.group("assignment")
def assignment():
    pass


@assignment.command("list")
@click.option("--id", type=str, required=True)
@click.pass_context
def list_assignments(ctx, id: str):
    assignments = get_assignments(ctx.obj, id)

    if assignments is None:
        assignments = []

    click.echo(json.dumps(assignments))


@assignment.command("create")
@click.option("--id", type=str, required=True)
@click.option("--group", type=str, required=True)
@click.pass_context
def create_assignment(ctx, id: str, group: str):
    try:
        assign_device_group(ctx.obj, id, group)
    except Exception as e:
        raise click.ClickException(f"Could not assign policy to group. {e}")


@assignment.command("delete")
@click.option("--id", type=str, required=True)
@click.option("--group", type=str, required=True)
@click.pass_context
def delete_assignment(ctx, id: str, group: str):
    try:
        unassign_device_group(ctx.obj, id, group)
    except Exception as e:
        raise click.ClickException(f"Could not unassign policy from group. {e}")
