import os

import click
import typer
from thestage_core.entities.config_entity import ConfigEntity

from thestage.i18n.translation import __
from thestage.entities.enums.yes_no_response import YesOrNoResponse
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.validation_service import ValidationService


class AppConfigService:

    __validation_service: ValidationService
    __config_provider: ConfigProvider

    def __init__(
            self,
            validation_service: ValidationService,
            config_provider: ConfigProvider,
    ):
        self.__validation_service = validation_service
        self.__config_provider = config_provider

    def app_change_token(
            self,
            config: ConfigEntity,
            token: str,
    ):
        if config.main.thestage_auth_token:
            response: YesOrNoResponse = typer.prompt(
                text=__('Do you want to change current token?'),
                show_choices=True,
                default=YesOrNoResponse.YES.value,
                type=click.Choice([r.value for r in YesOrNoResponse]),
                show_default=True,
            )
            if response == YesOrNoResponse.NO:
                raise typer.Exit(0)

        config.main.thestage_auth_token = token

        self.__validation_service.check_token(config=config)
        self.__config_provider.save_global_config(config=config)

    @staticmethod
    def app_remove_env():
        os.unsetenv('THESTAGE_CONFIG_FILE')
        os.unsetenv('THESTAGE_API_URL')
        os.unsetenv('THESTAGE_LOG_FILE')
        os.unsetenv('THESTAGE_AUTH_TOKEN')
