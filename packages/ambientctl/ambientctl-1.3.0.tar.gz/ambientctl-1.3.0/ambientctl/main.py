import click

from ambientctl.commands import auth, daemon, data, health, onboarding, ping, software


@click.group()
def cli():
    pass


# PING COMMAND
@cli.command("ping", help="Ping the local server or backend.")
@click.argument("endpoint", default="backend")
def ping_command(endpoint):
    ping.ping(endpoint)


@cli.group("daemon", help="Manage the Ambient Edge Server daemon.")
def daemon_command():
    pass


# DAEMON COMMANDS
@daemon_command.command("install", help="Install the Ambient Edge Server daemon.")
@click.option(
    "-e",
    "--env-vars",
    help="Environment variables to pass to the service. \
E.g., 'VAR1=VALUE1,VAR2=VALUE2'",
)
def install_command(env_vars):
    daemon.install(env_vars)


@daemon_command.command("start", help="Start the Ambient Edge Server daemon.")
def start_command():
    daemon.start()


@daemon_command.command("stop", help="Stop the Ambient Edge Server daemon.")
def stop_command():
    daemon.stop()


@daemon_command.command("restart", help="Restart the Ambient Edge Server daemon.")
@click.option(
    "--wait",
    is_flag=True,
    help="Wait for the service to start after restarting.",
)
def restart_command(wait: bool):
    daemon.restart(wait=wait)


@daemon_command.command(
    "status", help="Get the status of the Ambient Edge Server daemon."
)
def status_command():
    daemon.status()


@daemon_command.command("logs", help="Get the logs of the Ambient Edge Server daemon.")
@click.option(
    "--json",
    is_flag=True,
    help="Output the logs in JSON format.",
)
@click.option(
    "--level",
    default="",
    help="The log level to filter by.",
)
@click.option(
    "--module",
    default=None,
    help="The module to filter by.",
)
def logs_command(json, level, module):
    daemon.logs(json_format=json, level=level, module=module)


# AUTH COMMAND
@cli.group(
    "auth",
    help="Manage authentication between the Ambient Edge Server \
and the Ambient Backend.",
)
def auth_command():
    pass


@auth_command.command("status", help="Check the status of the node's authentication.")
def auth_status_command():
    auth.check_status()


@auth_command.command("authorize", help="Authorize the node with the server.")
@click.option("-n", "--node-id", required=True, help="The node ID to authorize.")
@click.option("-t", "--token", required=True, help="The token to use.")
def authorize_command(node_id, token):
    auth.authorize_node(node_id, token)


# DATA COMMAND
@cli.command("data", help="Get data from the Ambient Edge Server.")
@click.argument("operation", type=click.Choice(["read", "create", "update", "delete"]))
@click.argument("resource")
def data_command(operation, resource):
    data.run(operation, resource)


# HEALTH COMMANDs
@cli.group("health", help="Check the health of the Ambient Edge Server.")
def health_command():
    pass


@health_command.command("check-in", help="Check in with the Ambient Edge Server.")
def check_in_command():
    health.check_in()


# ONBOARDING COMMANDs
@cli.group("onboarding", help="Onboard the Ambient Edge Server.")
def onboarding_command():
    pass


@onboarding_command.command("begin", help="Begin the onboarding process.")
def begin_command():
    onboarding.run_onboarding()


@onboarding_command.command(
    "check-packages", help="Check if all required packages are installed."
)
def check_packages_command():
    onboarding.check_packages()


@onboarding_command.command("swarm", help="Check ensure swarm is initialized.")
def check_swarm_command():
    onboarding.handle_swarm_onboarding()


# SOFTWARE COMMANDs
@cli.group("software", help="Manage the Ambient Edge Server software.")
def software_command():
    pass


@software_command.command("upgrade", help="Upgrade the Ambient Edge Server software.")
def upgrade_command():
    software.upgrade()
