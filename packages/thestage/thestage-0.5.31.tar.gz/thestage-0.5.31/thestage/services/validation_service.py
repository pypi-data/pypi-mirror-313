from typing import Dict, Optional

import typer
from thestage_core.entities.config_entity import ConfigEntity, MainConfigEntity
from thestage_core.services.validation_service import ValidationServiceCore

from thestage.i18n.translation import __
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.clients.thestage_api.api_client import TheStageApiClient


class ValidationService(ValidationServiceCore):
    _thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
    ):
        super(ValidationService, self).__init__(
            thestage_api_client=thestage_api_client,
            config_provider=config_provider,
        )

    def check_token(
            self,
            config: ConfigEntity,
    ):
        token = config.main.thestage_auth_token
        if not token:
            token: str = typer.prompt(
                text=f'Authenticate using valid TheStage AI API token ({config.main.thestage_api_url})',
                show_choices=False,
                type=str,
                show_default=False,
            )

# TODO this fails with 503 error - AttributeError("'bytes' object has no attribute 'text'") from _parse_api_response method in core
        is_valid = self.validate_token(token,)
        if not is_valid:
            typer.echo(__(
                'API token is invalid: generate API token using TheStage AI WebApp'
            ))
            raise typer.Exit(1)

        config.main.thestage_auth_token = token
