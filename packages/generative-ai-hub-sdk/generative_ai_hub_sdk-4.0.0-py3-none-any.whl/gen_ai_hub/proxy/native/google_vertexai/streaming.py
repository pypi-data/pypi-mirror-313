from typing import Union

import proto
import requests
from google.api_core.rest_streaming import ResponseIterator
from google.protobuf.message import Message


class ServerSentEventsResponseIterator(ResponseIterator):

    def __init__(
        self,
        response: requests.Response,
        response_message_cls: Union[proto.Message, Message],
        prefix: str = "data: ",
        suffix: str = "\n\n",
    ):
        super().__init__(response=response, response_message_cls=response_message_cls)
        self._prefix = prefix
        self._suffix = suffix

    def _process_chunk(self, chunk: str):
        self._obj += chunk

        if self._obj.endswith(self._suffix):
            if not self._obj.startswith(self._prefix):
                raise ValueError(
                    "Invalid streaming format, expected prefix %s, instead got %s"
                    % (self._prefix, self._obj)
                )
            self._obj = self._obj[len(self._prefix) : -len(self._suffix)]
            if self._obj[0] != "{" or self._obj[-1] != "}":
                raise ValueError(
                    "Can only parse JSON objects, instead got %s" % self._obj
                )
            self._ready_objs.append(self._obj)
            self._obj = ""
