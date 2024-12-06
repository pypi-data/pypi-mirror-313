from pathlib import Path
from typing import Optional

from thestage.i18n.translation import __
from thestage.helpers.logger.app_logger import app_logger
from thestage.controllers.utils_controller import get_current_directory, validate_config_and_get_service_factory
from thestage import __app_name__, __version__

import typer

from thestage.services.connect.connect_service import ConnectService

app = typer.Typer(no_args_is_help=True)


@app.command(no_args_is_help=False)
def version():
    """
        Returns the application's name and version
    """
    app_logger.info(f'Start version from {get_current_directory()}')
    typer.echo(
        __("%app_name% v%version%", {'app_name': __app_name__, 'version': __version__}))
    raise typer.Exit(0)


@app.command(name="connect", no_args_is_help=True, help=__("Connect to server instance or container using unique ID"))
def connect(
        uid: Optional[str] = typer.Argument(
            help=__("Unique ID of server instance or container"), ),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for the server instance (required when connecting to self-hosted instance)"),
            is_eager=False,
        ),
        private_ssh_key_path: str = typer.Option(
            None,
            "--private-key-path",
            "-pk",
            help=__("Path to private key that will be accepted by remote server (optional)"),
            is_eager=False,
        ),
):
    """
        Connects to entity with a unique ID
    """
    app_logger.info(f'Connect to some entity with UID')

    if private_ssh_key_path and not Path(private_ssh_key_path).is_file():
        typer.echo(f'No file found at provided path {private_ssh_key_path}')
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()

    connect_service: ConnectService = service_factory.get_connect_service()

    connect_service.connect_to_entity(uid=uid, username=username, private_key_path=private_ssh_key_path)


    app_logger.info(f'Stop connect to entity')
    raise typer.Exit(0)
