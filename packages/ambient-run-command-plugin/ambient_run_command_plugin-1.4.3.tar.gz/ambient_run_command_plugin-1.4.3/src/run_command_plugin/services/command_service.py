import logging
import subprocess
from abc import ABC, abstractmethod
from typing import Optional

from ambient_backend_api_client import (
    ApiClient,
    Command,
    CommandNodeRelationship,
    CommandsApi,
    CommandStatusEnum,
    Configuration,
    UpdateNodeRelationship,
)
from result import Err, Ok, Result


class CommandService(ABC):
    @abstractmethod
    async def execute(self, command: Command) -> Result[None, str]:
        pass


class CommandServiceLinux(CommandService):
    def __init__(self, logger: logging.Logger, node_id: int):
        self.api_config: Optional[Configuration] = None
        self.node_id = node_id
        self.logger = logger
        self.logger.info("CommandServiceLinux initialized")

    async def init(self, api_config: Configuration) -> None:
        self.api_config = api_config
        self.logger.info("API config saved to CommandServiceLinux")

    async def execute(self, command: Command) -> Result[None, str]:
        self.logger.info("Executing command: {}", command.command)

        # update status to running
        update_cmd_result = await self.update_command(
            command.id, self.node_id, CommandStatusEnum.RUNNING
        )
        if update_cmd_result.is_err():
            err_msg = f"Failed to update command status to running: \
{update_cmd_result.unwrap_err()}"
            self.logger.error(err_msg)
            return update_cmd_result
        self.logger.debug(
            "CommandServiceLinux.execute - updated command status to running: {}",
            update_cmd_result.unwrap().model_dump_json(indent=4),
        )

        # Run the command
        self.logger.info("Running the command ...")
        result = self.run_command(command)
        if result.is_err():
            err_msg = f"Command failed: {result.unwrap_err()}"
            self.logger.error(err_msg)
            return result
        self.logger.info("Command executed successfully.")
        self.logger.debug(
            "CommandServiceLinux.execute - command result: {}", result.unwrap()
        )

        # update result
        self.logger.info("Updating command status ...")
        update_result = await self.update_command(
            command.id,
            self.node_id,
            CommandStatusEnum.SUCCESS if result.is_ok() else CommandStatusEnum.FAILURE,
            result,
        )
        if update_result.is_err():
            err_msg = f"Failed to update command status: {update_result.unwrap_err()}"
            self.logger.error(err_msg)
            return update_result
        self.logger.debug(
            "CommandServiceLinux.execute - updated command status: {}",
            update_result.unwrap().model_dump_json(indent=4),
        )
        self.logger.info("Command status updated successfully.")
        return Ok(None)

    async def update_command(
        self,
        command_id: int,
        node_id: int,
        status: CommandStatusEnum,
        result: Optional[Result[str, str]] = None,
    ) -> Result[CommandNodeRelationship, str]:
        async with ApiClient(configuration=self.api_config) as api_client:
            commands_api = CommandsApi(api_client)
            try:
                self.logger.debug(
                    "CommandServiceLinux.update_command - \
command API and api client objs: {}, {}",
                    commands_api,
                    api_client,
                )
                updated_output = (
                    await commands_api.update_command_outputs_commands_outputs_put(
                        update_node_relationship=UpdateNodeRelationship(
                            command_id=command_id,
                            node_id=node_id,
                            status=status,
                            error=(
                                result.unwrap_err()
                                if (result and result.is_err())
                                else None
                            ),
                            output=(
                                result.unwrap() if (result and result.is_ok()) else None
                            ),
                        )
                    )
                )
                self.logger.debug(
                    "CommandServiceLinux.update_command - updated command: {}",
                    updated_output.model_dump_json(indent=4),
                )
                return Ok(updated_output)
            except Exception as e:
                err_msg = f"Failed to update command: {e}"
                self.logger.error(err_msg)
                return Err(err_msg)

    def run_command(self, command: Command) -> Result[str, str]:
        try:
            result = subprocess.run(
                command.command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=command.timeout,
            )
            self.logger.debug("CommandServiceLinux.run_command - result: {}", result)
            return Ok(result.stdout.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            err_msg = f"Command failed: [subprocess.CalledProcessError] - {e}"
            self.logger.error(err_msg)
            return Err(err_msg)
        except Exception as e:
            err_msg = f"Command failed: {e}"
            self.logger.error(err_msg)
            return Err(err_msg)


def command_service_factory(
    logger: logging.Logger, node_id: int, platform: str
) -> CommandService:
    if platform == "linux":
        return CommandServiceLinux(logger, node_id)
    raise NotImplementedError(f"Platform {platform} not supported")
