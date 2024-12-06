from typing import List, Optional

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.content_filter import ContentFilter


class InputFiltering(JSONSerializable):
    """Module for managing and applying input content filters.

        Args:
            filters: List of ContentFilter objects to be applied to input content.
    """

    def __init__(
            self,
            filters: List[ContentFilter]
    ):
        self.filters = filters

    def to_dict(self):
        return {
            "filters": [f.to_dict() for f in self.filters],
        }


class OutputFiltering(JSONSerializable):
    """Module for managing and applying output content filters.

        Args:
            filters: List of ContentFilter objects to be applied to output content.
            stream_options: Module-specific streaming options.
    """

    def __init__(self,
                 filters: List[ContentFilter],
                 stream_options: Optional[dict] = None
                 ):
        self.filters = filters
        self.stream_options = stream_options

    def to_dict(self):
        config = {
            "filters": [f.to_dict() for f in self.filters],
        }

        if self.stream_options:
            config["stream_options"] = self.stream_options

        return config
