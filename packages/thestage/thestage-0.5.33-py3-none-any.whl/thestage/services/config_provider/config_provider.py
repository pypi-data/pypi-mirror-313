import os
from pathlib import Path
from typing import Optional, Dict

import typer
from thestage_core.entities.config_entity import ConfigEntity
from thestage_core.services.config_provider.config_provider import ConfigProviderCore

from thestage.config import THESTAGE_AUTH_TOKEN, THESTAGE_API_URL
from thestage.helpers.ssh_util import parse_private_key
from thestage.services.connect.dto.remote_server_config import RemoteServerConfig
from thestage.services.project.dto.project_config import ProjectConfig


class ConfigProvider(ConfigProviderCore):
    def __init__(
            self,
            local_path: str,
    ):
        super(ConfigProvider, self).__init__(
            local_path=local_path,
        )

    def get_full_config(self, check_daemon: bool = False,) -> ConfigEntity:
        config_values = {}

        # read env data
        config_from_env = {}
        config_from_env['main'] = {}
        if THESTAGE_AUTH_TOKEN:
            config_from_env['main']['thestage_auth_token'] = THESTAGE_AUTH_TOKEN
        if THESTAGE_API_URL:
            config_from_env['main']['thestage_api_url'] = THESTAGE_API_URL

        if config_from_env:
            self.__update_config_values_dict(values_to_update=config_values, new_values=config_from_env)

        # read global config data
        config_from_file = self._read_config_file(self._global_config_file)
        if config_from_file:
            self.__update_config_values_dict(values_to_update=config_values, new_values=config_from_file)

        config = ConfigEntity.model_validate(config_values)

        if self._local_path:
            config.runtime.working_directory = str(self._local_path)
        if self._global_config_path and not config.runtime.config_global_path:
            config.runtime.config_global_path = str(self._global_config_path)

        if check_daemon:
            self.check_for_daemon(config=config)

        return config

    def save_project_config(self, project_config: ProjectConfig):
        self.__create_empty_project_config_if_missing()
        # self.read_project_config()
        project_config_path = self.__get_project_config_path(with_file=True)
        self._save_config_file(data=project_config.model_dump(), file_path=project_config_path)

    def save_remote_server_config(self, remote_server_config: RemoteServerConfig):
        self.__create_empty_project_config_if_missing()
        # self.read_project_config()
        project_config_path = self.__get_project_config_path(with_file=True)
        self._save_config_file(data=remote_server_config.model_dump(), file_path=project_config_path)


    def save_project_deploy_ssh_key(self, deploy_ssh_key: str, project_slug: str, project_id: int) -> str:
        deploy_key_dirpath = self._global_config_path.joinpath('project_deploy_keys')
        self._file_system_service.create_if_not_exists(deploy_key_dirpath)

        deploy_key_filepath = deploy_key_dirpath.joinpath(f'project_deploy_key_{project_id}_{project_slug}')
        self._file_system_service.create_if_not_exists_file(deploy_key_filepath)

        text_file = open(deploy_key_filepath, "w")
        text_file.write(deploy_ssh_key)
        text_file.close()
        os.chmod(deploy_key_filepath, 0o600)

        return str(deploy_key_filepath)

    def read_project_config(self) -> Optional[ProjectConfig]:
        project_data_dirpath = self.__get_project_config_path()
        if not project_data_dirpath.exists():
            return None
            # self._file_system_service.create_if_not_exists(project_data_dirpath)

        project_data_filepath = self.__get_project_config_path(with_file=True)
        if not project_data_filepath.exists():
            return None

        config_data = self._read_config_file(project_data_filepath) if project_data_filepath and project_data_filepath.exists() else {}
        return ProjectConfig.model_validate(config_data)


    def __create_empty_project_config_if_missing(self):
        project_data_dirpath = self.__get_project_config_path()
        if not project_data_dirpath.exists():
            self._file_system_service.create_if_not_exists(project_data_dirpath)

        project_data_filepath = self.__get_project_config_path(with_file=True)
        if not project_data_filepath.exists():
            self._file_system_service.create_if_not_exists_file(project_data_filepath)


    def __get_project_config_path(self, with_file: bool = False) -> Path:
        if with_file:
            return self._local_config_path.joinpath('project.json')
        else:
            return self._local_config_path


    def __get_remote_server_config_path(self) -> Path:
        return self._global_config_path.joinpath('remote_server_config.json')


    def update_remote_server_config_entry(self, ip_address: str, ssh_key_path: Optional[Path]):
        # double checking if key is parseable (fails if key is encrypted)
        # see remote_server_service for similar check
        if ssh_key_path:
            pkey = parse_private_key(str(ssh_key_path))

            if pkey is None:
                typer.echo("Could not identify provided private key (expected RSA, ECDSA, ED25519)")
                raise typer.Exit(1)

        config = self.read_remote_server_config()
        remote_server_config_filepath = self.__get_remote_server_config_path()
        if config:
            if not config.ip_address_to_ssh_key_map:
                config.ip_address_to_ssh_key_map = {}

            existing_path = config.ip_address_to_ssh_key_map.get(ip_address)
            if ssh_key_path and existing_path != str(ssh_key_path):
                config.ip_address_to_ssh_key_map.update({ip_address: str(ssh_key_path)})
                typer.echo(f'Updated ssh key for {ip_address}: {ssh_key_path}')

            if not ssh_key_path and existing_path:
                typer.echo(f"Private key at path {existing_path} was not found")
                config.ip_address_to_ssh_key_map.pop(ip_address, None)
        else:
            self._file_system_service.create_if_not_exists_file(remote_server_config_filepath)
            config = RemoteServerConfig(ip_address_to_ssh_key_map={ip_address: str(ssh_key_path)})

        self._save_config_file(data=config.model_dump(), file_path=remote_server_config_filepath)

        return str(remote_server_config_filepath)


    def read_remote_server_config(self) -> Optional[RemoteServerConfig]:
        config_filepath = self.__get_remote_server_config_path()
        if not config_filepath.is_file():
            return None

        config_data = self._read_config_file(config_filepath) if config_filepath and config_filepath.exists() else {}
        return RemoteServerConfig.model_validate(config_data)

    def get_valid_private_key_path_by_ip_address(self, ip_address: str) -> Optional[str]:
        remote_server_config = self.read_remote_server_config()
        if remote_server_config and remote_server_config.ip_address_to_ssh_key_map:
            private_key_path = remote_server_config.ip_address_to_ssh_key_map.get(ip_address)
            if private_key_path and Path(private_key_path).is_file():
                return private_key_path
            elif private_key_path:
                self.update_remote_server_config_entry(ip_address, None)
        return None

    @staticmethod
    def __update_config_values_dict(values_to_update: Dict, new_values: Dict):
        if 'main' in new_values:
            if 'main' in values_to_update:
                values_to_update['main'].update(new_values['main'])
            else:
                values_to_update['main'] = new_values['main']