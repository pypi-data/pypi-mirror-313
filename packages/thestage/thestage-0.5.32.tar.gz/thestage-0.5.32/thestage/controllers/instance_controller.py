from pathlib import Path
from typing import Optional, List

from thestage.services.clients.thestage_api.dtos.enums.instance_rented_status import InstanceRentedBusinessStatus

from thestage.entities.rented_instance import RentedInstanceEntity
from thestage.entities.self_hosted_instance import SelfHostedInstanceEntity
from thestage.helpers.logger.app_logger import app_logger
from thestage.services.clients.thestage_api.dtos.enums.selfhosted_status import SelfhostedBusinessStatus
from thestage.services.instance.mapper.instance_mapper import InstanceMapper
from thestage.services.instance.mapper.selfhosted_mapper import SelfHostedMapper
from thestage.services.instance.instance_service import InstanceService
from thestage.i18n.translation import __
from thestage.controllers.utils_controller import \
    validate_config_and_get_service_factory

import typer


app = typer.Typer(no_args_is_help=True, help=__("Manage server instances"))

rented = typer.Typer(no_args_is_help=True, help=__("Manage rented server instances"))
self_hosted = typer.Typer(no_args_is_help=True, help=__("Manage self-hosted instances"))

app.add_typer(rented, name="rented")
app.add_typer(self_hosted, name="self-hosted")


@rented.command(name="ls", help=__("List rented server instances"))
def rented_list(
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
        statuses: List[str] = typer.Option(
            None,
            '--status',
            '-s',
            help=__("Filter by status, use --status all to list all rented server instances"),
            is_eager=False,
        ),
):
    """
        Lists rented server instances
    """
    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    instance_service: InstanceService = service_factory.get_instance_service()
    instance_rented_status_map = service_factory.get_thestage_api_client().get_rented_business_status_map(config.main.thestage_auth_token)

    if not statuses:
        statuses = ({key: instance_rented_status_map[key] for key in [
            InstanceRentedBusinessStatus.ONLINE,
            InstanceRentedBusinessStatus.CREATING,
            InstanceRentedBusinessStatus.TERMINATING,
            InstanceRentedBusinessStatus.REBOOTING,
        ]}).values()

    if "all" in statuses:
        statuses = instance_rented_status_map.values()

    for input_status_item in statuses:
        if input_status_item not in instance_rented_status_map.values():
            typer.echo(__("'%invalid_status%' is not one of %valid_statuses%", {
                'invalid_status': input_status_item,
                'valid_statuses': str(list(instance_rented_status_map.values()))
            }))
            raise typer.Exit(1)

    typer.echo(__(
        "Listing rented server instances with the following statuses: %statuses%, to view all rented server instances, use --status all",
        placeholders={
            'statuses': ', '.join([status_item for status_item in statuses])
        }))

    backend_statuses: List[str] = [key for key, value in instance_rented_status_map.items() if value in statuses]

    instance_service.print(
        func_get_data=instance_service.get_rented_list,
        func_special_params={
            'statuses': backend_statuses,
        },
        mapper=InstanceMapper(),
        config=config,
        headers=list(map(lambda x: x.alias, RentedInstanceEntity.model_fields.values())),
        row=row,
        page=page,
        show_index="never",
    )

    typer.echo(__("Rented server instances listing complete"))
    raise typer.Exit(0)


@rented.command(name="connect", no_args_is_help=True, help=__("Connect to rented server instance"))
def instance_connect(
        instance_uid: Optional[str] = typer.Argument(
            help=__("Rented server instance unique ID"),
        ),
        private_ssh_key_path: str = typer.Option(
            None,
            "--private-key-path",
            "-pk",
            help=__("Path to private key that will be accepted by remote server (optional)"),
            is_eager=False,
        )
):
    """
        Connects to rented server instance
    """
    app_logger.info(f'Connect to rented server instance')

    if not instance_uid:
        typer.echo(__('Rented server instance unique ID is required'))
        raise typer.Exit(1)

    if private_ssh_key_path and not Path(private_ssh_key_path).is_file():
        typer.echo(f'No file found at provided path {private_ssh_key_path}')
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    instance_service: InstanceService = service_factory.get_instance_service()

    instance_service.connect_to_rented_instance(
        instance_rented_slug=instance_uid,
        config=config,
        input_ssh_key_path=private_ssh_key_path
    )

    app_logger.info(f'Stop connecting to rented server instance')
    raise typer.Exit(0)


@self_hosted.command(name="ls", help=__("List self-hosted instances"))
def self_hosted_list(
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
        statuses: List[str] = typer.Option(
            None,
            '--status',
            '-s',
            help=__("Filter by status, use --status all to list all self-hosted server instances"),
            is_eager=False,
        ),
):
    """
        Lists self-hosted instances
    """
    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    instance_service: InstanceService = service_factory.get_instance_service()
    selfhosted_instance_status_map = service_factory.get_thestage_api_client().get_selfhosted_business_status_map(config.main.thestage_auth_token)

    if not statuses:
        statuses = ({key: selfhosted_instance_status_map[key] for key in [
            SelfhostedBusinessStatus.AWAITING_CONFIGURATION,
            SelfhostedBusinessStatus.RUNNING,
            SelfhostedBusinessStatus.TERMINATED,
        ]}).values()

    if "all" in statuses:
        statuses = selfhosted_instance_status_map.values()

    for input_status_item in statuses:
        if input_status_item not in selfhosted_instance_status_map.values():
            typer.echo(__("'%invalid_status%' is not one of %valid_statuses%", {
                'invalid_status': input_status_item,
                'valid_statuses': str(list(selfhosted_instance_status_map.values()))
            }))
            raise typer.Exit(1)

    typer.echo(__(
        "Listing self-hosted instances with the following statuses: %statuses%, to view all self-hosted instances, use --status all",
        placeholders={
            'statuses': ', '.join([status_item for status_item in statuses])
        }))

    backend_statuses: List[str] = [key for key, value in selfhosted_instance_status_map.items() if value in statuses]

    instance_service.print(
        func_get_data=instance_service.get_self_hosted_list,
        func_special_params={
            'statuses': backend_statuses,
        },
        mapper=SelfHostedMapper(),
        config=config,
        headers=list(map(lambda x: x.alias, SelfHostedInstanceEntity.model_fields.values())),
        row=row,
        page=page,
        show_index="never",
    )

    typer.echo(__("Self-hosted instances listing complete"))
    raise typer.Exit(0)


@self_hosted.command(name="connect", no_args_is_help=True, help=__("Connect to self-hosted instance"))
def self_hosted_connect(
        instance_slug: Optional[str] = typer.Argument(help=__("Self-hosted instance unique ID"),),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for server instance (required when connecting to self-hosted instance)"),
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
        Connects to self-hosted instance
    """
    app_logger.info(f'Connect to self-hosted instance')

    if not instance_slug:
        typer.echo(__('Self-hosted instance unique ID is required'))
        raise typer.Exit(1)

    if private_ssh_key_path and not Path(private_ssh_key_path).is_file():
        typer.echo(f'No file found at provided path {private_ssh_key_path}')
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory()
    config = service_factory.get_config_provider().get_full_config()

    instance_service: InstanceService = service_factory.get_instance_service()

    instance_service.connect_to_selfhosted_instance(
        selfhosted_instance_slug=instance_slug,
        username=username,
        config=config,
        input_ssh_key_path=private_ssh_key_path
    )

    app_logger.info(f'Stop connecting to self-hosted instance')
    raise typer.Exit(0)
