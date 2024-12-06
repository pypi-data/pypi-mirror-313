import json
import time

import click
import requests

from ambientctl.config import settings


def check_in():
    max_retries = 10
    retry_interval = 2
    while max_retries > 0:
        try:
            response = requests.request(
                "GET", f"{settings.ambient_server}/health/check-in"
            )
            response.raise_for_status()
            click.echo(json.dumps(response.json(), indent=4))
            return
        except Exception:
            click.echo("error occurred.")
            max_retries -= 1
            click.echo(f"Retrying in {retry_interval} seconds")
            time.sleep(retry_interval)
    return {"error": "Max retries exceeded"}
