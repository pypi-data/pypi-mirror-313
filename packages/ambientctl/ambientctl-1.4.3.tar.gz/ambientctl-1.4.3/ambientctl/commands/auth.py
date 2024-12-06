import click
import requests

from ambientctl.config import settings


def check_status():
    url = f"{settings.ambient_server}/auth/status"
    try:
        response = requests.get(url)
        response.raise_for_status()
        click.echo(response.json()["status"])
    except Exception as e:
        click.echo(f"error: {e}")
        return


def authorize_node(node_id: str, token: str):
    url = f"{settings.ambient_server}/auth?node_id={node_id}&refresh_token={token}"
    try:
        response = requests.post(url)
        response.raise_for_status()
        click.echo(response.json())
    except Exception as e:
        click.echo(f"error: {e}")
        return


def cycle_certificate():
    url = f"{settings.ambient_server}/auth/cycle-certificate"
    try:
        response = requests.post(url)
        response.raise_for_status()
        click.echo(response.json())
    except Exception as e:
        click.echo(f"error: {e}")
        return
