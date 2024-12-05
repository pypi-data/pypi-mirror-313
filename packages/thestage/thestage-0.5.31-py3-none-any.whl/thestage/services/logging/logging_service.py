import asyncio
from _signal import SIGINT
from asyncio import CancelledError, Task, StreamWriter
from datetime import datetime
from typing import Optional, Dict

import aioconsole
import typer
from httpx import ReadTimeout, ConnectError, ConnectTimeout
from requests.exceptions import ChunkedEncodingError
from thestage_core.entities.config_entity import ConfigEntity

from thestage.services.clients.thestage_api.dtos.enums.task_status import TaskStatus
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.logging.byte_print_style import BytePrintStyle
from thestage.services.logging.dto.log_message import LogMessage
from thestage.services.logging.dto.log_type import LogType
from thestage.i18n.translation import __
from thestage.services.abstract_service import AbstractService
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider
from rich import print

from thestage.services.logging.logging_constants import LOG_MESSAGE_CODE_TASK_FINISHED

is_logs_streaming = False


class LoggingService(AbstractService):
    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
    ):
        super(LoggingService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client


    @error_handler()
    def print_last_task_logs(self, config: ConfigEntity, task_id: int, logs_number: Optional[int]):
        logs = self.__thestage_api_client.query_user_logs(
            token=config.main.thestage_auth_token,
            task_id=task_id,
            limit=logs_number
        )
        for log_message in reversed(logs.queryResult):
            self.__print_log_line_object(log_message)


    @error_handler()
    def stream_container_logs(self, config: ConfigEntity, container: DockerContainerDto):
        typer.echo(__(
            f"Log stream for docker container '%container_slug%' started",
            {
                'container_slug': container.slug,
            }
        ))
        typer.echo(__("Press CTRL+C to stop"))
        try:
            for log_json in self.__thestage_api_client.get_container_log_stream(
                    token=config.main.thestage_auth_token,
                    container_id=container.id
            ):
                self.__print_log_line(log_json)
        except ChunkedEncodingError as e1:  # handling server timeout
            typer.echo(__('Log stream disconnected (1)'))
            raise typer.Exit(1)

        typer.echo(__('Log stream disconnected'))


    @error_handler()
    def stream_task_logs_with_controls(self, config: ConfigEntity, task_id: int):
        asyncio.run(
            self.__stream_task_logs_with_controls_async(
                config=config,
                task_id=task_id
            )
        )


    @error_handler()
    async def __stream_task_logs_with_controls_async(self, config: ConfigEntity, task_id: int):
        task_view_response: Optional[TaskViewResponse] = self.__thestage_api_client.get_task(
            token=config.main.thestage_auth_token,
            task_id=task_id,
        )

        task_status_map: Dict[str, str] = self.__thestage_api_client.get_task_localized_status_map(
            token=config.main.thestage_auth_token,
        )

        task = task_view_response.task

        if task:
            if task.frontend_status.status_key not in [TaskStatus.RUNNING, TaskStatus.SCHEDULED]:
                typer.echo(__("Task must be in status '%required_status%' to stream real-time logs. Task %task_id% status: '%status%'.", {
                    'task_id': str(task.id),
                    'status': task.frontend_status.status_translation,
                    'required_status': task_status_map.get(TaskStatus.RUNNING) or TaskStatus.RUNNING
                }))
                raise typer.Exit(1)
        else:
            typer.echo(__("Task with ID %task_id% was not found", {'task_id': task.id}))
            raise typer.Exit(1)

        typer.echo(__(
            f"Log stream for task %task_id% started",
            {
                'task_id': str(task.id),
            }
        ))

        typer.echo(__("CTRL+C to cancel the task. CTRL+D to disconnect from log stream."))

        print_logs_task = asyncio.create_task(self.print_task_logs(config.main.thestage_auth_token, task.id))
        input_task = asyncio.create_task(self.read_log_stream_input())

        def sigint_handler():
            input_task.cancel()

        loop = asyncio.get_event_loop()
        for signal_item in [SIGINT]:  # SIGINT == CTRL+C
            loop.add_signal_handler(signal_item, sigint_handler)

        done, pending = await asyncio.wait([print_logs_task, input_task], return_when=asyncio.FIRST_COMPLETED)

        if input_task in done:
            print_logs_task.cancel()
            if not input_task.result():  # result is only expected if ctrl+D triggered EOFError
                typer.echo(f"\rTask {task_id} will be canceled")
                self.__thestage_api_client.stop_task_on_instance(
                    token=config.main.thestage_auth_token,
                    task_id=task.id,
                )


    async def read_log_stream_input(self):
        try:
            while True:
                input1 = await aioconsole.ainput()
        except EOFError:
            typer.echo(__("\rExited from task log stream"))
            return True
        except CancelledError:  # Always appears if async task is canceled and leaves huge traces
            pass


    async def print_task_logs(self, token: str, task_id: int):
        polling_interval_seconds: float = 4  # also adjust polling api method timeout if changed
        between_logs_sleeping_coef: float = 1  # we emulate delay between logs, but if for any reason code runs for too long - delays will be controlled with this coef
        last_iteration_log_timestamp: Optional[str] = None  # pointer to next iteration polling start (obtained from each response)
        last_log_id: Optional[str] = None  # pointer to next iteration polling start - to exclude the log id from result (obtained from each response)
        consecutive_error_count: int = 0  # connectivity errors count - stream will disconnect if too many errors in a row
        iteration_started_at: datetime  # used to control iteration duration - polling should be done at around exact rate
        errors_started_at: Optional[datetime] = None  # time since errors started to stream disconnect

        is_no_more_logs = False
        while not is_no_more_logs:
            log_wait_remaining_limit: float = polling_interval_seconds  # hard limit just in case
            iteration_started_at = datetime.utcnow()
            last_printed_log_timestamp: Optional[datetime] = None
            reader, writer = await aioconsole.get_standard_streams()

            # this shows (somewhat accurate) time difference between logs here and in real time. should not grow.
            # if last_iteration_log_timestamp:
            #     last_log_timestamp_parsed = datetime.strptime(last_iteration_log_timestamp, '%Y-%m-%dT%H:%M:%S.%f')
            #     stream_to_logs_diff = datetime.utcnow() - last_log_timestamp_parsed
            #     print_nonblocking(f'TDIFF {stream_to_logs_diff.total_seconds()}', writer)
            try:
                logs_response = await self.__thestage_api_client.poll_logs_httpx(
                    token=token,
                    task_id=task_id,
                    docker_container_id=None,
                    last_log_timestamp=last_iteration_log_timestamp,
                    last_log_id=last_log_id
                )

                if consecutive_error_count > 0:
                    consecutive_error_count = 0
                    errors_started_at = None
                    log_wait_remaining_limit = 0   # no log delays after reconnect

                last_iteration_log_timestamp = logs_response.lastLogTimestamp
                last_log_id = logs_response.lastLogId

                for log_item in logs_response.logs:
                    current_log_timestamp = datetime.strptime(log_item.timestamp[:26], '%Y-%m-%dT%H:%M:%S.%f')  # python does not like nanoseconds
                    if last_printed_log_timestamp is not None and log_wait_remaining_limit > 0:
                        logs_sleeptime = (current_log_timestamp - last_printed_log_timestamp).total_seconds() * between_logs_sleeping_coef
                        await asyncio.sleep(logs_sleeptime)
                        log_wait_remaining_limit -= logs_sleeptime
                    self.__print_log_line_object_nonblocking(log_item, writer)
                    last_printed_log_timestamp = current_log_timestamp
                    if log_item.messageCode == LOG_MESSAGE_CODE_TASK_FINISHED:
                        is_no_more_logs = True

                if is_no_more_logs:
                    break
            except (ReadTimeout, ConnectError, ConnectTimeout) as e:
                consecutive_error_count += 1
                if consecutive_error_count == 1:
                    print_nonblocking("Network issues, attempting to re-establish connection...", writer, BytePrintStyle.ORANGE)
                if not errors_started_at:
                    errors_started_at = datetime.utcnow()

            if consecutive_error_count > 7:
                seconds_with_error = (datetime.utcnow() - errors_started_at).total_seconds()
                print_nonblocking(f"Log stream: disconnected from server (connectivity issues for {seconds_with_error} seconds). Try 'thestage project task logs {task_id}' to reconnect.", writer)
                break

            # depending on iteration duration - sleep for the remaining time and adjust log sleep coefficient if needed
            iteration_duration = (datetime.utcnow() - iteration_started_at).total_seconds()
            if iteration_duration > polling_interval_seconds:
                between_logs_sleeping_coef *= 0.85
            else:
                await asyncio.sleep(polling_interval_seconds - iteration_duration)
                if between_logs_sleeping_coef < 1:
                    between_logs_sleeping_coef = min(1.0, between_logs_sleeping_coef * 1.15)


    def __print_log_line(self, log_message_raw_json: str):
        log_message = LogMessage.model_validate_json(log_message_raw_json)
        if not log_message.logType and log_message.message == 'ping':
            return
        self.__print_log_line_object(log_message)


    @staticmethod
    def __print_log_line_object(log_message: LogMessage):
        line_color: str = "grey78"

        if not log_message.logType and log_message.message == 'ping':
            return

        if log_message.logType == LogType.STDERR.value:
            line_color = "red"
        if log_message.message:
            print(f'[{line_color}][not bold]{log_message.message}[/not bold][/{line_color}]')

    @staticmethod
    def __print_log_line_object_nonblocking(log_message: LogMessage, writer: StreamWriter):
        if log_message.message:
            line_color: str = BytePrintStyle.RESET
            if log_message.logType == LogType.STDERR.value:
                line_color = BytePrintStyle.RED

            print_nonblocking(f'{log_message.message}', writer, line_color)


def print_nonblocking(line: str, writer: StreamWriter, color_code: str = BytePrintStyle.RESET):
    writer.write(str.encode(f'{color_code}{line}{BytePrintStyle.RESET}\r\n'))
