import json
import logging
from typing import Any, Union

from ambient_backend_api_client import Command
from ambient_base_plugin import BasePlugin, ConfigPayload, Message
from run_command_plugin.services.command_service import (
    CommandService,
    command_service_factory,
)


class RunCommandPlugin(BasePlugin):
    def __init__(self):
        self.cmd_svc = None
        self.api_config = None
        self.logger = None

    async def configure(
        self, config: ConfigPayload, logger: Union[logging.Logger, Any] = None
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self.logger.debug("RunCommandPlugin.configure - config: {}", config)
        self.api_config = config.api_config
        assert (  # noqa: F631
            self.api_config is not None,
            "API Configuration is required for this plugin",
        )
        self.cmd_svc: CommandService = command_service_factory(
            logger=self.logger, node_id=config.node_id, platform=config.platform
        )
        await self.cmd_svc.init(self.api_config)
        self.logger.info("RunCommandPlugin configured")

    async def handle_event(self, message: Message) -> None:
        try:
            self.logger.info("Handling message for topic: {}", message.topic)

            msg_data: dict = json.loads(message.message)
            self.logger.debug(
                "RunCommandHanlder.handle - msg_data: {}",
                json.dumps(msg_data, indent=4),
            )

            cmd = Command.model_validate(msg_data)
            self.logger.debug("RunCommandHanlder.handle - cmd: {}", cmd)

            result = await self.cmd_svc.execute(cmd)
            self.logger.debug("RunCommandHanlder.handle - result: {}", result)

            self.logger.info(
                "Command executed {}",
                ("successfully" if result.is_ok() else "unsuccessfully"),
            )
        except Exception as e:
            self.logger.error("Error handling message: {}", e)
