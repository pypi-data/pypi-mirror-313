
import re
from pathlib import Path
from typing import Optional, List

from thestage.entities.container import DockerContainerEntity
from thestage.services.clients.thestage_api.dtos.enums.container_pending_action import DockerContainerAction
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.i18n.translation import __
from thestage.services.clients.thestage_api.dtos.enums.container_status import DockerContainerStatus
from thestage.services.container.container_service import ContainerService
from thestage.services.container.mapper.container_mapper import ContainerMapper
from thestage.helpers.logger.app_logger import app_logger
from thestage.controllers.utils_controller import validate_config_and_get_service_factory, get_current_directory

import typer

from thestage.services.logging.logging_service import LoggingService

app = typer.Typer(no_args_is_help=True, help=__("Manage containers"))


@app.command(name='ls', help=__("List containers"))
def list_items(
        row: int = typer.Option(
            5,
            '--row',
            '-r',
            help=__("Set number of rows displayed per page"),
            is_eager=False,
        ),
        page: int = typer.Option(
            1,
            '--page',
            '-p',
            help=__("Set starting page for displaying output"),
            is_eager=False,
        ),
        project_uid: str = typer.Option(
            None,
            '--project-uid',
            '-puid',
            help=__("Filter containers by project unique ID"),
            is_eager=False,
        ),
        statuses: List[str] = typer.Option(
            None,
            '--status',
            '-s',
            help=__("Filter by status, use --status all to list all containers"),
            is_eager=False,
        ),
):
    """
        Lists containers
    """
    app_logger.info(f'Start container lists from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container_service.print_container_list(
        config=config,
        row=row,
        page=page,
        project_uid=project_uid,
        statuses=statuses,
    )

    typer.echo(__("Containers listing complete"))
    raise typer.Exit(0)


@app.command(name="info", no_args_is_help=True, help=__("Help get container details"))
def item_details(
        container_uid: Optional[str] = typer.Argument(hidden=False, help=__("Container unique ID")),
):
    """
        Lists container details
    """
    app_logger.info(f'Start container details')

    if not container_uid:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_container(
        config=config,
        container_slug=container_uid,
    )

    if not container:
        typer.echo(__("Container not found: %container_item%", {'container_item': str(container_uid) if container_uid else ''}))
        raise typer.Exit(1)

    typer.echo(__("STATUS: %status%", {'status': str(container.frontend_status.status_translation if container and container.frontend_status else 'UNKNOWN')}))
    typer.echo(__("UNIQUE ID: %slug%", {'slug': str(container.slug)}))
    typer.echo(__("TITLE: %title%", {'title': str(container.title)}))
    typer.echo(__("IMAGE: %image%", {'image': str(container.docker_image)}))

    if container.instance_rented:
        typer.echo(
            __("RENTED SERVER INSTANCE UNIQUE ID: %instance_slug%", {'instance_slug': str(container.instance_rented.slug)})
        )
        typer.echo(
            __("RENTED SERVER INSTANCE STATUS: %instance_status%",
               {'instance_status': str(container.instance_rented.frontend_status.status_translation if container.instance_rented.frontend_status else 'UNKNOWN')})
        )

    if container.selfhosted_instance:
        typer.echo(
            __("SELF-HOSTED INSTANCE UNIQUE ID: %instance_slug%", {'instance_slug': str(container.selfhosted_instance.slug)})
        )
        typer.echo(
            __("SELF-HOSTED INSTANCE STATUS: %instance_status%",
               {'instance_status': str(container.selfhosted_instance.frontend_status.status_translation if container.selfhosted_instance.frontend_status else 'UNKNOWN')})
        )

    if container.mappings and (container.mappings.port_mappings or container.mappings.directory_mappings):
        if container.mappings.port_mappings:
            typer.echo(__("CONTAINER PORT MAPPING:"))
            for src, dest in container.mappings.port_mappings.items():
                typer.echo(f"    {src} : {dest}")

        if container.mappings.directory_mappings:
            typer.echo(__("CONTAINER DIRECTORY MAPPING:"))
            for src, dest in container.mappings.directory_mappings.items():
                typer.echo(f"    {src} : {dest}")

    raise typer.Exit(0)


@app.command(name="connect", no_args_is_help=True, help=__("Connect to container"))
def container_connect(
        container_uid: Optional[str] = typer.Argument(help=__("Container unique ID"),),
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
        Connects to container
    """
    app_logger.info(f'Connect to container')

    if not container_uid:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    if private_ssh_key_path and not Path(private_ssh_key_path).is_file():
        typer.echo(f'No file found at provided path {private_ssh_key_path}')
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container_service.connect_to_container(
        config=config,
        container_uid=container_uid,
        username=username,
        input_ssh_key_path=private_ssh_key_path,
    )

    app_logger.info(f'Stop connect to container')
    raise typer.Exit(0)


@app.command(name="upload", no_args_is_help=True, help=__("Upload file to container"))
def put_file(
        source_path: str = typer.Argument(help=__("Source file path"),),
        destination: Optional[str] = typer.Argument(help=__("Destination directory path in container. Format: container_uid:/path/to/file"),),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for the server instance (required when connecting to self-hosted instance)"),
            is_eager=False,
        ),
):
    """
        Uploads file to container
    """
    app_logger.info(f'Push file to container')

    container_args = re.match(r"^([\w\W]+?):([\w\W]+)$", destination)

    if container_args is None:
        typer.echo(__('Container unique ID and source file path are required as the second argument'))
        typer.echo(__('Example: container_uid:/path/to/file'))
        raise typer.Exit(1)
    container_slug = container_args.groups()[0]
    destination_path = container_args.groups()[1].rstrip("/")

    if not container_slug:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    # TODO delete when we change mappings
    if destination_path.startswith("/app/") or destination_path == "/app":
        typer.echo("/app/ is reserved for project code and must not contain custom files. Сonsider adding your files to the project repository")
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_container(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_if_container_running(
            container=container
        )

        typer.echo(__("Uploading file(s) to container '%container-slug%'", {'container-slug': container_slug}))

        container_service.put_file_to_container(
            container=container,
            src_path=source_path,
            destination_path=destination_path,
            username_param=username,
            copy_only_folder_contents=source_path.endswith("/")
        )
    else:
        typer.echo(__("Container not found: %container_item%", {'container_item': container_slug}))

    app_logger.info(f'End send files to container')
    raise typer.Exit(0)


@app.command(name="download", no_args_is_help=True, help=__("Download file from container"))
def download_file(
        source_path: str = typer.Argument(help=__("Source file path in container. Format: container_uid:/path/to/file"),),
        destination_path: str = typer.Argument(help=__("Destination directory path on local machine"),),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for the server instance (required when connecting to self-hosted instance)"),
            is_eager=False,
        ),
):
    """
        Downloads file from container
    """
    app_logger.info(f'Download file from container')

    container_args = re.match(r"^([\w\W]+?):([\w\W]+)$", source_path)

    if container_args is None:
        typer.echo(__('Container unique ID and source directory path are required as the first argument'))
        typer.echo(__('Example: container-uid:/path/to/file'))
        raise typer.Exit(1)
    container_slug = container_args.groups()[0]
    source_path = container_args.groups()[1]

    if not container_slug:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_container(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_if_container_running(
            container=container
        )

        typer.echo(__("Downloading files from container: '%container-slug%'", {'container-slug': container_slug}))

        container_service.get_file_from_container(
            container=container,
            src_path=source_path,
            destination_path=destination_path.rstrip("/"),
            username_param=username,
            copy_only_folder_contents=source_path.endswith("/"),
            config=config
        )
    else:
        typer.echo(__("Container not found: %container_item%", {'container_item': container_slug}))

    app_logger.info(f'End download files from container')
    raise typer.Exit(0)


@app.command(name="start", no_args_is_help=True, help=__("Start container"))
def start_container(
        container_uid: Optional[str] = typer.Argument(help=__("Container unique ID"), ),
):
    """
        Starts container
    """
    app_logger.info(f'Start container')

    if not container_uid:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container_service.request_docker_container_action(
        config=config,
        container_uid=container_uid,
        action=DockerContainerAction.START
    )

    app_logger.info(f'End start container')
    raise typer.Exit(0)


@app.command(name="stop", no_args_is_help=True, help=__("Stop container"))
def stop_container(
        container_uid: Optional[str] = typer.Argument(help=__("Container unique ID"), ),
):
    """
        Stops container
    """
    app_logger.info(f'Stop container')

    if not container_uid:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container_service.request_docker_container_action(
        config=config,
        container_uid=container_uid,
        action=DockerContainerAction.STOP
    )

    app_logger.info(f'End stop container')
    raise typer.Exit(0)


@app.command(name="restart", no_args_is_help=True, help=__("Restart container"))
def stop_container(
        container_uid: Optional[str] = typer.Argument(help=__("Container unique ID"), ),
):
    """
        Stops container
    """
    app_logger.info(f'Restart container')

    if not container_uid:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container_service.request_docker_container_action(
        config=config,
        container_uid=container_uid,
        action=DockerContainerAction.RESTART
    )

    app_logger.info(f'End stop container')
    raise typer.Exit(0)


@app.command(name="logs", no_args_is_help=True, help=__("Stream real-time container logs; log history is available in your TheStage AI account"))
def container_logs(
        container_uid: Optional[str] = typer.Argument(help=__("Container unique id")),
):
    """
        Streams real-time container logs
    """
    app_logger.info(f'View container logs')

    if not container_uid:
        typer.echo(__('Container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()
    logging_service: LoggingService = service_factory.get_logging_service()

    container: Optional[DockerContainerDto] = container_service.get_container(
        config=config,
        container_slug=container_uid,
    )

    if container:
        logging_service.stream_container_logs(
            config=config,
            container=container
        )
    else:
        typer.echo(__("Container not found: %container_slug%", {'container_slug': container_uid}))

    app_logger.info(f'Container logs - end')
    raise typer.Exit(0)
