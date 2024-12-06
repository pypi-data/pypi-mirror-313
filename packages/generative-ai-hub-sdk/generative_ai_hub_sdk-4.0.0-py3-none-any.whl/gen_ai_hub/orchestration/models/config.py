from typing import Optional, List
from warnings import warn

from gen_ai_hub.orchestration.models.content_filtering import InputFiltering, OutputFiltering
from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.content_filter import ContentFilter
from gen_ai_hub.orchestration.models.llm import LLM
from gen_ai_hub.orchestration.models.data_masking import DataMasking
from gen_ai_hub.orchestration.models.template import Template

class OrchestrationConfig(JSONSerializable):
    """
    Configuration for the Orchestration Service's content generation process.

    Defines modules for a harmonized API that combines LLM-based content generation
    with additional processing functionalities.

    The orchestration service allows for advanced content generation by processing inputs through a series of steps:
    template rendering, text generation via LLMs, and optional input/output transformations such as data masking
    or filtering.

    Args:
        template: Template object for rendering input prompts.
        llm: Language model for text generation.
        input_filtering: Module for filtering and validating input content before processing.
        output_filtering: Module for filtering and validating output content after generation.
        data_masking: Module for anonymizing or pseudonymizing sensitive information in inputs.
        stream_options: Global options for controlling streaming behavior.
        input_filters: List of content filters applied to inputs before processing.
            **Deprecated:** Will be removed in future versions. Use input_filtering instead.
        output_filters: List of content filters applied to outputs after generation.
            **Deprecated:** Will be removed in future versions. Use output_filtering instead.
    """

    def __init__(
            self,
            template: Template,
            llm: LLM,
            input_filtering: Optional[InputFiltering] = None,
            output_filtering: Optional[OutputFiltering] = None,
            data_masking: Optional[DataMasking] = None,
            stream_options: Optional[dict] = None,
            input_filters: Optional[List[ContentFilter]] = None,
            output_filters: Optional[List[ContentFilter]] = None,
    ):
        if input_filters is not None:
            warn(
                "The 'input_filters' parameter is deprecated and will be removed in a future version. "
                "Use 'input_filtering' instead.",
                DeprecationWarning,
                stacklevel=2
            )
        self.input_filters = input_filters

        if output_filters is not None:
            warn(
                "The 'output_filters' parameter is deprecated and will be removed in a future version. "
                "Use 'output_filtering' instead.",
                DeprecationWarning,
                stacklevel=2
            )
        self.output_filters = output_filters

        self.template = template
        self.llm = llm

        self.data_masking = data_masking
        self.input_filtering = input_filtering
        self.output_filtering = output_filtering

        self.stream_options = stream_options
        self._stream = False

    def _get_module_configurations(self):
        configs = {
            "templating_module_config": self.template.to_dict(),
            "llm_module_config": self.llm.to_dict(),
        }

        if self.data_masking:
            configs["masking_module_config"] = self.data_masking.to_dict()

        if filter_config := self._get_filter_config():
            configs["filtering_module_config"] = filter_config

        return configs

    def _get_filter_config(self):
        config = {}

        # Backward compatibility for deprecated input_filters and output_filters
        if self.input_filters and not self.input_filtering:
            self.input_filtering = InputFiltering(filters=self.input_filters)

        if self.output_filters and not self.output_filtering:
            self.output_filtering = OutputFiltering(filters=self.output_filters)

        if self.input_filtering:
            config["input"] = self.input_filtering.to_dict()

        if self.output_filtering:
            config["output"] = self.output_filtering.to_dict()

        return config

    def to_dict(self):
        config = {
            "module_configurations": self._get_module_configurations(),
            **({"stream": True} if self._stream else {}),
            **({"stream_options": self.stream_options} if self._stream and self.stream_options else {})
        }

        return config
