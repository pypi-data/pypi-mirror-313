from mobicontrol.client.auth import authenticate
from mobicontrol.client import MobicontrolClient, ConfigurationError
import click


@click.group(invoke_without_command=True, name="mc")
@click.pass_context
def mobicontrol(ctx):
    try:
        ctx.obj = MobicontrolClient.load()
    except ConfigurationError as err:
        raise click.ClickException(str(err))

    if ctx.invoked_subcommand is None:
        ctx.obj.save()
        click.echo("Welcome to Mobicontrol CLI")

        if ctx.obj.base_url is None:
            click.echo("Please login first")
        else:
            click.echo("Your deployment server is located at: " + ctx.obj.base_url)


@mobicontrol.command()
@click.option("--url", envvar="MC_URL", required=True)
@click.option("--client_id", envvar="MC_CLIENT_ID", required=True)
@click.option("--client_secret", envvar="MC_CLIENT_SECRET", required=True)
@click.option("--username", envvar="MC_USERNAME", required=True)
@click.option("--password", envvar="MC_PASSWORD", required=True)
@click.pass_context
def login(ctx, url, client_id, client_secret, username, password):
    click.echo(f"Logging in as {username}")
    try:
        ctx.obj.base_url = url
        authenticate(ctx.obj, client_id, client_secret, username, password)
        ctx.obj.save()
    except Exception as e:
        click.echo(e)
        return

    click.echo("Successfully logged in!")


from . import apps, policies, apply
