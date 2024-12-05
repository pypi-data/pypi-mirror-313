"""
Base Agent class
"""

import logging
from abc import abstractmethod

from fence import LLM
from fence.links import logger as link_logger
from fence.memory.base import BaseMemory, FleetingMemory

logger = logging.getLogger(__name__)

# Suppress the link logger
link_logger.setLevel("INFO")


class BaseAgent:
    """Base Agent class"""

    def __init__(
        self,
        identifier: str | None = None,
        model: LLM = None,
        description: str | None = None,
        memory: BaseMemory | None = None,
        environment: dict | None = None,
    ):
        """
        Initialize the Agent object.

        :param identifier: An identifier for the agent. If none is provided, the class name will be used.
        :param model: An LLM model object.
        :param description: A description of the agent.
        :param environment: A dictionary of environment variables to pass to delegates and tools.
        """
        self.environment = environment or {}
        self.identifier = identifier or self.__class__.__name__
        self.model = model
        self.description = description

        # Memory setup
        self.memory = memory or FleetingMemory()

        # Set system message
        self._system_message = None

    @abstractmethod
    def run(self, prompt: str) -> str:
        """
        Run the agent

        :param prompt: The initial prompt to feed to the LLM
        """
        raise NotImplementedError

    def format_toml(self):
        """
        Returns a TOML-formatted key-value pair of the agent name,
        the description (docstring) of the agent.
        """

        # Preformat the arguments
        toml_string = f"""[[agents]]
agent_name = "{self.identifier}"
agent_description = "{self.description or self.__doc__}"
"""

        return toml_string

    def _flush_memory(self):
        """Clear or reset the agent's memory context."""

        # Check if there are any messages in the memory
        self.memory.messages = self.memory.get_messages()

        # Check if there is a system message in the memory
        self.memory.system = self.memory.get_system_message()

        # If no system message is present, add a new one
        if not self.memory.system:
            self.memory.set_system_message(content=self._system_message)
