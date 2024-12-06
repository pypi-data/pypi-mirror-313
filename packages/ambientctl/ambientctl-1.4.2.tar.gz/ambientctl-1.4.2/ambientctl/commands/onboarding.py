import os
import subprocess
import time
from typing import Dict, Optional

import click
import requests
from ambient_backend_api_client import NodeOutput as Node

from ambient_client_common.utils import logger
from ambientctl import config
from ambientctl.commands import auth, daemon, data, health, software


def run_onboarding(
    node_id: Optional[str] = None,
    token: Optional[str] = None,
    env_vars: Optional[str] = None,
    auto_upgrade: bool = False,
):
    # welcome message
    click.secho(
        "Welcome to the Ambient Edge Server onboarding process.",
        fg="white",
        bold=True,
        reverse=True,
    )

    # check all packages are installed
    if auto_upgrade:
        upgrade_software(with_prompt=False)
    elif not auto_upgrade and node_id and token:
        # this is comming from the no_console_command
        pass
    else:
        upgrade_software()

    # install, restart, and verify daemon
    # if in dev mode, prompt for env vars as long as they are not provided
    if config.settings.ambient_dev_mode and not env_vars and not node_id and not token:
        env_vars = set_server_env_vars()
    install_and_verify_daemon(env_vars=env_vars)

    # authorize with backend
    authorize_backend(node_id=node_id, token=token)

    # ensure server is authorized
    ensure_authorized()

    # run health check-in
    run_health_check()

    # handle swarm onboarding
    handle_swarm_onboarding()

    # cycle certificate
    click.echo("Cycling certificate...")
    auth.cycle_certificate()

    # done
    done()


def set_server_env_vars() -> str:
    click.secho("Warning: You are running in development mode.", fg="yellow", bold=True)
    env_vars = click.prompt(
        text="Enter environment variables to pass to the server. \
E.g., 'VAR1=VALUE1,VAR2=VALUE2'",
        default="BACKEND_API_URL=https://api.ambientlabsdev.io,\
EVENT_BUS_API=https://events.ambientlabsdev.io,\
CONNECTION_SERVICE_URL=wss://sockets.ambientlabsdev.io,\
AMBIENT_LOG_LEVEL=DEBUG",
    )
    return env_vars


def upgrade_software(with_prompt: bool = True):
    if with_prompt:
        click.secho(
            "Would you like to upgrade the Ambient Edge Server software? [y/n]",
            bold=True,
        )
        answer = click.getchar()
        if answer.lower() != "y":
            return

    software.upgrade()


def install_missing_packages(
    package_report: Dict[str, dict], mock_install: bool = False
):
    click.echo("Installing required packages...")
    current_env = os.environ.copy()
    logger.debug("Current environment: {}", current_env)
    if mock_install:
        click.secho("Mock install enabled.", fg="yellow", bold=True)
        logger.info("Mock install enabled.")
    for package, report in package_report.items():
        if not report.get("ok", False):
            version = config.settings.version
            click.echo(f"Installing {package}={version}...")
            logger.info("Installing {}={}", package, version)
            if mock_install:
                time.sleep(0.5)
                click.echo(f"Successfully installed {package}.")
                continue
            result = subprocess.run(
                ["pip", "install", f"{package}=={version}"],
                capture_output=True,
                env=current_env,
            )
            if result.returncode != 0:
                click.secho(
                    f"Failed to install {package}. Please install manually.",
                    fg="red",
                    bold=True,
                )
            else:
                click.echo(f"Successfully installed {package}.")
    click.secho("All required packages are installed.", fg="green", bold=True)


def install_daemon(env_vars: Optional[str] = None):
    daemon.install(env_vars=env_vars, silent=True)


def restart_daemon():
    daemon.restart(silent=True)


def verify_daemon():
    daemon.status(silent=True)


def wait_untiL_daemon_is_running():
    daemon.wait_until_service_is_running()


def install_and_verify_daemon(env_vars: Optional[str] = None):
    steps = [
        install_daemon,
        wait_untiL_daemon_is_running,
        verify_daemon,
    ]
    progress_weights = [13, 68, 19]
    with click.progressbar(
        length=100, label="Installing Ambient Edge Server daemon"
    ) as bar:
        for i, step in enumerate(steps):
            # run the first step with env_vars
            if i == 0:
                step(env_vars)
            else:
                step()
            bar.update(progress_weights[i])


def authorize_backend(node_id: Optional[str] = None, token: Optional[str] = None):
    if not token or not node_id:
        node_id = click.prompt("Enter the node ID", type=int)
        token = click.prompt("Enter the token", type=str, hide_input=True)
    click.echo(f"Authorizing node {node_id} with token [{len(token)} chars] ...")
    daemon.wait_until_service_is_running()
    auth.authorize_node(node_id, token)
    daemon.restart(silent=False)
    daemon.wait_until_service_is_running()
    click.echo("Node authorized.")


def ensure_authorized():
    click.echo("Ensuring node is authorized...")
    auth.check_status()


def run_health_check():
    click.echo("Running health check-in...")
    health.check_in()


def done():
    click.secho("Onboarding complete.", fg="green", bold=True)


def handle_swarm_onboarding():
    node = Node.model_validate(data.make_rest_call("node", "GET"))
    if node.role != "manager":
        click.echo("Node is not a manager. Skipping swarm onboarding.")
        return

    click.echo("Node is a manager. Initiating swarm onboarding...")

    trigger_swarm_init()
    ensure_part_of_swarm()


def trigger_swarm_init():
    click.echo("Triggering swarm init...")
    response = requests.post(
        url="http://localhost:7417/plugins/docker_swarm_plugin/onboarding",
    )
    response.raise_for_status()
    click.echo("Swarm init triggered.")


def ensure_part_of_swarm():
    click.echo("Ensuring node is part of swarm...")
    response = requests.get(
        url="http://localhost:7417/plugins/docker_swarm_plugin/swarm_info",
    )
    response.raise_for_status()
    click.echo("Node is part of swarm.")
