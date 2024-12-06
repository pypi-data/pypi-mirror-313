import json
from typing import Any

import click
import requests

from ambientctl.config import settings


def run(operation: str, resource: str) -> None:
    rest_method = settings.cred_to_rest_dict.get(operation, None)
    if rest_method is None:
        click.echo(f"Invalid operation: {operation}")
        return

    result = make_rest_call(resource, rest_method)

    click.echo(json.dumps(result, indent=4))


def make_rest_call(resource: str, method: str) -> Any:
    response = requests.request(method, f"{settings.ambient_server}/data/{resource}")
    response.raise_for_status()
    return response.json()
