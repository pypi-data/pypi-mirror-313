from mobicontrol.cli import mobicontrol
import click
from mobicontrol.utils import get_file_contents, get_filename_from_path
from mobicontrol.client.apps import upload_app, get_app
import json


@mobicontrol.group()
def app():
    pass


@app.command()
@click.option("--id", type=str, required=True)
@click.pass_context
def show(ctx, id: str):
    try:
        app = get_app(ctx.obj, id)
    except Exception as e:
        raise click.ClickException(f"Could not fetch app. {e}")

    click.echo(json.dumps(app))


@app.command()
@click.option("--file", type=click.Path(exists=True), required=True)
@click.pass_context
def upload(ctx, file: str):
    filename = get_filename_from_path(file)
    content = get_file_contents(file)

    try:
        app = upload_app(ctx.obj, filename, content)
    except Exception as e:
        raise click.ClickException(f"Could not upload app. {e}")

    click.echo(json.dumps(app))
