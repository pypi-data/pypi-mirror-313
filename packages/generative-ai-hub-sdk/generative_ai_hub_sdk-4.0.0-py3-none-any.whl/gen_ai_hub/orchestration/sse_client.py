import json
from enum import Enum

import dacite
import requests

from typing import Iterable

from gen_ai_hub.orchestration.exceptions import OrchestrationError
from gen_ai_hub.orchestration.models.response import OrchestrationResponseStreaming


class SSEClient:

    def __init__(self, event_source: requests.Response, prefix: str = "data: ", final_message: str = '[DONE]'):
        self.event_source = event_source
        self.event_prefix = prefix
        self.final_message = final_message

    def __iter__(self) -> Iterable[OrchestrationResponseStreaming]:

        for line in self.event_source.iter_lines(decode_unicode=True):
            if not line or not line.startswith(self.event_prefix):
                continue

            event_data = line[len(self.event_prefix):]

            if event_data == self.final_message:
                break

            event = json.loads(event_data)

            if 'code' in event:
                raise OrchestrationError(
                    request_id=event.get("request_id"),
                    message=event.get("message"),
                    code=event.get("code"),
                    location=event.get("location"),
                    module_results=event.get("module_results", {}),
                )

            yield dacite.from_dict(
                data=event,
                data_class=OrchestrationResponseStreaming,
                config=dacite.Config(cast=[Enum]),
            )
