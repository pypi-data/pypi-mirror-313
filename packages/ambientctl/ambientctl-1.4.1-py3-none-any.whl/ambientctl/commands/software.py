from typing import Optional

import click
import requests

from ambientctl import config
from ambientctl.commands.daemon import restart


def upgrade(version: Optional[str] = None):
    try:
        url = f"{config.settings.ambient_server}/software/upgrade"
        response = requests.post(url)
        response.raise_for_status()
        click.echo(response.text)
        restart(wait=True)
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to upgrade service: {e}")
        raise click.Abort() from e
