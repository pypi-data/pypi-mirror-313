import getpass
import grp
import json
import os
import pathlib
import pwd
import subprocess
import time
from typing import Optional

import click
import jinja2
import requests
from file_read_backwards import FileReadBackwards

from ambient_client_common.utils import logger
from ambientctl.config import settings
from ambientctl.models.system_service import ServiceConfigLinux


def install(env_vars: Optional[str] = None, silent: bool = False):
    logger.info("Installing service...")
    if not silent:
        click.echo("Installing service...")
    logger.debug(f"Environment variables: {env_vars}")
    # build payload request
    env_dict = None
    try:
        if env_vars:
            env_dict = {}
            for env_var in env_vars.split(","):
                key, value = env_var.split("=")
                env_dict[key] = value
            logger.info(f"Environment variables: {env_dict}")
    except Exception as e:
        logger.error(f"Failed to parse environment variables: {e}")
        click.secho("Failed to parse environment variables.", fg="red", bold=True)
        raise click.Abort() from e

    # render jinja template
    try:
        template_path = pathlib.Path(__file__).parent.parent / "templates"
        logger.debug("files in template directory: {}", list(template_path.iterdir()))
        service_config = build_service_config(env_dict)
        logger.debug("service config: {}", service_config.model_dump_json(indent=4))
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
        logger.debug("template_loader created.")
        template_env = jinja2.Environment(loader=template_loader, autoescape=True)
        logger.debug("template_env created.")
        # list the files in the template directory
        logger.debug("Templates: {}", template_loader.list_templates())
        template = template_env.get_template("ambient_edge_server.service.jinja2")
        logger.debug("template created.")
        output = template.render(service=service_config.model_dump())
        logger.info("Template rendered.")
        logger.debug("Rendered template: {}", output)
    except Exception as e:
        logger.error(f"Failed to render template: {e}")
        click.secho("Failed to render template.", fg="red", bold=True)
        raise click.Abort() from e

    # write to file
    try:
        daemon_file = pathlib.Path("/etc/systemd/system/ambient_edge_server.service")
        daemon_file.write_text(output)
    except Exception as e:
        logger.error(f"Failed to write service file: {e}")
        click.secho("Failed to write service file.", fg="red", bold=True)
        raise click.Abort() from e

    # run systemctl daemon-reload
    try:
        subprocess.run(["systemctl", "daemon-reload"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to reload daemon: {e}")
        click.secho("Failed to reload daemon.", fg="red", bold=True)
        raise click.Abort() from e

    logger.info("Service installed successfully!")
    if not silent:
        click.echo("Service installed successfully!")

    restart(silent=silent)


def start():
    try:
        url = f"{settings.ambient_server}/daemon/start"
        response = requests.post(url)
        response.raise_for_status()
        click.echo(response.text)
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to start service: {e}")
        exit(1)


def stop():
    try:
        url = f"{settings.ambient_server}/daemon/stop"
        response = requests.post(url)
        response.raise_for_status()
        click.echo(response.text)
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to stop service: {e}")
        exit(1)


def restart(silent: bool = False, wait: bool = False):
    try:
        url = f"{settings.ambient_server}/daemon/restart"
        response = requests.post(url)
        response.raise_for_status()
        if not silent:
            click.echo(json.dumps(response.json(), indent=4))
    except requests.exceptions.RequestException as e:
        click.echo(
            f"Failed to restart service via server: {e}\n\
Restarting via CLI...\nPassword may be required!"
        )
        restart_cmd = ["sudo", "systemctl", "restart", "ambient_edge_server.service"]
        try:
            output = subprocess.run(
                restart_cmd, check=True, text=True, capture_output=True
            )
            click.echo(output.stdout)
        except subprocess.CalledProcessError as e:
            click.echo(f"Failed to restart service via CLI: {e}")
            raise click.Abort() from e

    if wait:
        click.echo("Waiting for service to start...")
        wait_until_service_is_running()
        click.echo("Service is running.")


def status(silent: bool = False):
    try:
        url = f"{settings.ambient_server}/daemon/status"
        response = requests.get(url)
        response.raise_for_status()
        if not silent:
            click.echo(response.text)
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to get service status: {e}")
        exit(1)


def logs(json_format: bool = False, level: str = "", module: Optional[str] = None):
    home_path = pathlib.Path.home()
    log_file = home_path / ".ambient" / "logs" / "ambientctl.log"
    click.echo_via_pager(
        read_log_file_line_by_line(log_file, json_format, level, module)
    )


def build_service_config(env_vars: Optional[dict] = None) -> ServiceConfigLinux:
    logger.debug("building the service configuration ...")
    user = get_user()
    group = get_group()

    if env_vars:
        logger.debug(
            "LinuxDaemonService.build_service_config - environment variables: {}",
            env_vars,
        )
    return ServiceConfigLinux(
        user=user,
        group=group,
        environment=env_vars,
    )


def get_user() -> str:
    logger.debug("getting the current user ...")
    username = getpass.getuser()
    logger.info("current user: {}", username)
    return username


def get_group() -> str:
    logger.debug("getting the current group ...")

    uid = os.getuid()
    user_info = pwd.getpwuid(uid)
    primary_gid = user_info.pw_gid

    logger.debug(
        "-> uid: {}\n-> primary_gid: {}\n-> user_info: {}",
        uid,
        primary_gid,
        user_info,
    )

    group_info = grp.getgrgid(primary_gid)
    group_name = group_info.gr_name

    logger.info("current group: {}", group_name)
    logger.debug("-> group_info: {}", group_info)

    return group_name


def read_log_file_line_by_line(
    file_path, json_format: bool = False, level: str = "", module: Optional[str] = None
):
    """
    Generator to read a file line by line.

    :param file_path: Path to the log file.
    """
    with FileReadBackwards(file_path, encoding="utf-8") as frb:
        # getting lines by lines starting from the last line up
        for line in frb:
            parsed_line = parse_json_line(line, json_format, level, module)
            if parsed_line:
                yield parsed_line


def parse_json_line(
    line: str, json_format: bool = False, level: str = "", module: Optional[str] = None
) -> str:
    """
    Parse a JSON line and extract specified fields.

    :param line: A single line from the log file.
    :return: A formatted string with the selected fields or an error message.
    """
    try:
        new_line = ""
        json_data = json.loads(line)
        if json_format:
            new_line = json.dumps(json_data, indent=4)
        else:
            new_line = json_data.get("text", line)
        if level != "":
            if json_data.get("record", {}).get("level", {}).get("name", "") != level:
                new_line = ""
        if module:
            if module not in json_data.get("record", {}).get("name", ""):
                new_line = ""
        return new_line
    except json.JSONDecodeError:
        return f"Invalid JSON: {line}"


def wait_until_service_is_running():
    logger.info("Waiting for service to start...")
    # gotta wait 3 seconds because that's the server's delay
    time.sleep(3.5)
    max_wait_time = 60
    wait_interval = 1
    while max_wait_time > 0:
        if is_api_ready():
            logger.info("Service is running.")
            return
        max_wait_time -= wait_interval
        time.sleep(wait_interval)
    logger.error("Service failed to start.")


def is_api_ready() -> bool:
    try:
        url = f"{settings.ambient_server}/ping?endpoint=backend"
        response = requests.get(url)
        response.raise_for_status()
        logger.debug("API is ready.")
        return True
    except requests.exceptions.RequestException:
        logger.debug("API is not ready.")
        return False
