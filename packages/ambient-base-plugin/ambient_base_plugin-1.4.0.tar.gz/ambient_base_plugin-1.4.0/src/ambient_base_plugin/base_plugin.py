from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, Union

import apluggy as pluggy
from ambient_backend_api_client import NodeOutput as Node
from ambient_base_plugin.models.configuration import ConfigPayload
from ambient_base_plugin.models.message import Message

hookspec = pluggy.HookspecMarker("ambient_system_sweep")
hookimpl = pluggy.HookimplMarker("ambient_system_sweep")


class BasePlugin(ABC):
    @abstractmethod
    async def configure(
        self, config: ConfigPayload, logger: Union[Logger, Any] = None
    ) -> None:
        pass

    @abstractmethod
    async def handle_event(self, message: Message) -> None:
        pass

    @hookspec
    async def run_system_sweep(self, node: Node) -> None:
        pass
