import os
from pathlib import Path

import click
from thestage_core.entities.config_entity import ConfigEntity
from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.entities.enums.yes_no_response import YesOrNoResponse
from thestage.i18n.translation import __
from thestage.helpers.logger.app_logger import app_logger
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.connect.connect_service import ConnectService
from thestage.services.service_factory import ServiceFactory
from thestage.controllers.utils_controller import get_current_directory, validate_config_and_get_service_factory

import typer

app = typer.Typer(no_args_is_help=True, help=__("Manage configuration settings"))


@app.command(name='get', no_args_is_help=False, help=__("Display all configuration settings"))
def config_get():
    """
        Lists all configuration settings
    """
    app_logger.info(f'Start config from {get_current_directory()}')

    local_path = get_current_directory()
    config_provider = ConfigProvider(local_path=local_path)
    config: ConfigEntity = config_provider.get_full_config()

    if not config:
        typer.echo(__('No configuration found'))
        raise typer.Exit(1)

    config_provider.save_global_config(config=config)

    typer.echo(__('THESTAGE TOKEN: %token%', {'token': config.main.thestage_auth_token or ''}))
    typer.echo(__('THESTAGE API LINK: %link%', {'link': config.main.thestage_api_url or ''}))

    if config.runtime.config_global_path:
        typer.echo(__('CONFIG PATH: %path%', {'path': str(config.runtime.config_global_path or '') + f'/config.json'}))

    raise typer.Exit(0)


@app.command(name='set', no_args_is_help=True, help=__("Update configuration settings"))
def config_set(
    token: str = typer.Option(
            None,
            "--api-token",
            "-t",
            help=__("Set or update API token"),
            is_eager=False,
        ),
):
    """
        Updates configuration settings
    """
    app_logger.info(f'Start config from {get_current_directory()}')

    config_provider = ConfigProvider(local_path=get_current_directory())
    service_factory = ServiceFactory(config_provider)

    app_service = service_factory.get_app_config_service()

    if token:
        app_service.app_change_token(config=config_provider.get_full_config(), token=token)

    typer.echo('Configuration updated successfully')
    raise typer.Exit(0)


@app.command(name='clear', no_args_is_help=False, help=__("Clear configuration"))
def config_clear():
    """
        Clears all configuration settings
    """
    app_logger.info(f'Start config from {get_current_directory()}')
    local_path = get_current_directory()
    config_provider = ConfigProvider(local_path=local_path)
    config_dir = config_provider.get_full_config().runtime.config_global_path
    config_provider.remove_all_config()
    typer.echo(f'Removed {config_dir}')

    raise typer.Exit(0)


@app.command(name='upload-ssh-key', no_args_is_help=True, help=__("Send your public SSH key to the platform and / or rented server instance"))
def config_set(
        ssh_public_key: str = typer.Argument(
            help=__("Path to your public SSH key file or your public SSH key contents"),
        ),
        instance_rented_slug: str = typer.Option(
            None,
            "--instance-uid",
            "-uid",
            help=__("Unique ID of your rented instance to add the key to (optional)"),
            is_eager=False,
        )
):
    """
        Sends SSH key to the platform
    """

    app_logger.info(f'Start config from {get_current_directory()}')

    config_provider = ConfigProvider(local_path=get_current_directory())
    service_factory = ServiceFactory(config_provider)
    connect_service: ConnectService = service_factory.get_connect_service()

    is_path_provided_confirmed = False
    ssh_key_contents = ssh_public_key

    if ssh_public_key.startswith("/") or ssh_public_key.startswith("~") or ssh_public_key.endswith(".pub") or len(ssh_public_key) < 30:
        is_path_provided_confirmed = True

    ssh_key_path = Path(ssh_public_key).absolute()
    if is_path_provided_confirmed and not ssh_key_path.exists():
        typer.echo(f"No key was found at {ssh_key_path}")
        raise typer.Exit(1)

    if is_path_provided_confirmed or ssh_key_path.exists():
        if '.' not in ssh_key_path.name:
            proceed_with_no_extension: YesOrNoResponse = typer.prompt(
                text=f"File '{ssh_key_path.name}' probably contains a private key. Proceed?",
                show_choices=True,
                default=YesOrNoResponse.YES.value,
                type=click.Choice([r.value for r in YesOrNoResponse]),
                show_default=True,
            )
            if proceed_with_no_extension == YesOrNoResponse.NO:
                raise typer.Exit(0)
        ssh_key_contents = ssh_key_path.open("r").read()
        if 'private key-----' in ssh_key_contents.lower():
            typer.echo(f"{ssh_key_path} is identified as a private key. Please provide a public SSH key.")
            raise typer.Exit(1)

    connect_service.upload_ssh_key(
        public_key_contents=ssh_key_contents,
        instance_slug=instance_rented_slug,
    )

    raise typer.Exit(0)
