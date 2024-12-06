import click
import requests

from ambientctl.config import settings


def ping(endpoint: str):
    click.echo(f"Pinging {endpoint}...")
    if endpoint == "self":
        click.echo("Pong!")
        return
    elif endpoint == "backend" or endpoint == "server":
        ping_server(endpoint)
        return

    click.echo("error: endpoint not found")


def ping_server(endpoint: str):
    url = f"{settings.ambient_server}/ping?endpoint={endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        click.echo(response.json(), color=True)
    except Exception as e:
        click.echo(f"error: {e}")
        return
