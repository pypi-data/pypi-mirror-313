import os
import pathlib
from typing import Optional, Dict, Tuple

from thestage_core.entities.config_entity import ConfigEntity

from thestage.helpers.error_handler import error_handler
from thestage.services.service_factory import ServiceFactory
from thestage.services.config_provider.config_provider import ConfigProvider


def get_current_directory() -> pathlib.Path:
    return pathlib.Path.cwd()


@error_handler()
def validate_config_and_get_service_factory(
        working_directory: Optional[str] = None,
) -> ServiceFactory:
    local_path = get_current_directory() if not working_directory else os.path.abspath(working_directory)
    config_provider = ConfigProvider(local_path=local_path)
    service_factory = ServiceFactory(config_provider=config_provider)
    config: ConfigEntity = config_provider.get_full_config()

    validation_service = service_factory.get_validation_service()
    validation_service.check_token(config=config)
    config_provider.save_global_config(config=config)

    return service_factory
