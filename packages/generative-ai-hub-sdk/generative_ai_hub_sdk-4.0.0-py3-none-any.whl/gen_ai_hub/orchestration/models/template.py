from typing import List, Optional, Union, NamedTuple

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.message import Message


class TemplateValue(NamedTuple):
    """
    Represents a named value for use in template substitution.

    This class pairs a name with a corresponding value, which can be a string,
    integer, or float. It's designed to be used in template rendering processes
    where named placeholders are replaced with specific values.

    Args:
        name: The identifier for this template value.
        value: The actual value to be used in substitution.
    """

    name: str
    value: Union[str, int, float]


class Template(JSONSerializable):
    """
    Represents a configurable template for generating prompts or conversations.

    This class encapsulates a series of prompt messages along with optional default values
    for template variables. It provides a structured way to define and serialize
    templates for use in various natural language processing tasks.

    Args:
        messages: A list of prompt messages that form the template.
        defaults: A list of default values for template variables.
    """

    def __init__(
        self,
        messages: List[Message],
        defaults: Optional[List[TemplateValue]] = None,
    ):
        self.messages = messages
        self.defaults = defaults or []

    def to_dict(self):
        return {
            "template": [message.to_dict() for message in self.messages],
            "defaults": {default.name: default.value for default in self.defaults},
        }
