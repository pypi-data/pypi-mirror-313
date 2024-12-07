from typing import Optional

from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.services.connect.connect_service import ConnectService
from thestage.services.logging.logging_service import LoggingService
from thestage.services.project.project_service import ProjectService
from thestage.services.remote_server_service import RemoteServerService
from thestage.services.container.container_service import ContainerService
from thestage.services.instance.instance_service import InstanceService
from thestage.services.app_config_service import AppConfigService
from thestage.services.clients.git.git_client import GitLocalClient
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider
from thestage.services.validation_service import ValidationService


class ServiceFactory:
    __config_provider: Optional[ConfigProvider] = None
    __thestage_api_client: Optional[TheStageApiClient] = None
    __git_local_client: Optional[GitLocalClient] = None
    __file_system_service: Optional[FileSystemServiceCore] = None

    def __init__(
            self,
            config_provider: Optional[ConfigProvider] = None,
    ):
        self.__config_provider = config_provider

    def get_config_provider(self) -> ConfigProvider:
        return self.__config_provider

    def get_validation_service(self, config_provider: Optional[ConfigProvider] = None,) -> ValidationService:
        return ValidationService(
                thestage_api_client=self.get_thestage_api_client(),
                config_provider=config_provider if config_provider else self.__config_provider,
            )

    def get_instance_service(self, config_provider: Optional[ConfigProvider] = None) -> InstanceService:
        return InstanceService(
                thestage_api_client=self.get_thestage_api_client(),
                config_provider=config_provider if config_provider else self.__config_provider,
                remote_server_service=self.get_remote_server_service(),
            )

    def get_container_service(self, config_provider: Optional[ConfigProvider] = None) -> ContainerService:
        return ContainerService(
                thestage_api_client=self.get_thestage_api_client(),
                config_provider=config_provider if config_provider else self.__config_provider,
                remote_server_service=self.get_remote_server_service(),
                file_system_service=self.get_file_system_service(),
            )

    def get_connect_service(self, config_provider: Optional[ConfigProvider] = None) -> ConnectService:
        return ConnectService(
            config_provider=config_provider if config_provider else self.__config_provider,
            thestage_api_client=self.get_thestage_api_client(),
            instance_service=self.get_instance_service(),
            container_service=self.get_container_service(),
            logging_service=self.get_logging_service(),
        )

    def get_project_service(self, config_provider: Optional[ConfigProvider] = None) -> ProjectService:
        return ProjectService(
            thestage_api_client=self.get_thestage_api_client(),
            config_provider=config_provider if config_provider else self.__config_provider,
            remote_server_service=self.get_remote_server_service(),
            file_system_service=self.get_file_system_service(),
            git_local_client=self.get_git_local_client(),
        )

    def get_remote_server_service(self) -> RemoteServerService:
        return RemoteServerService(
            config_provider=self.get_config_provider(),
            file_system_service=self.get_file_system_service(),
        )

    def get_thestage_api_client(self) -> TheStageApiClient:
        if not self.__thestage_api_client:
            self.__thestage_api_client = TheStageApiClient(api_url=self.__config_provider.get_full_config().main.thestage_api_url)
        return self.__thestage_api_client

    def get_git_local_client(self):
        if not self.__git_local_client:
            self.__git_local_client = GitLocalClient(file_system_service=self.get_file_system_service())
        return self.__git_local_client

    def get_file_system_service(self) -> FileSystemServiceCore:
        if not self.__file_system_service:
            self.__file_system_service = FileSystemServiceCore()
        return self.__file_system_service

    def get_app_config_service(self, config_provider: Optional[ConfigProvider] = None,) -> AppConfigService:
        return AppConfigService(
            validation_service=self.get_validation_service(config_provider),
            config_provider=config_provider if config_provider else self.__config_provider,
        )

    def get_logging_service(self, config_provider: Optional[ConfigProvider] = None) -> LoggingService:
        return LoggingService(
            thestage_api_client=self.get_thestage_api_client(),
            config_provider=config_provider if config_provider else self.__config_provider,
        )

