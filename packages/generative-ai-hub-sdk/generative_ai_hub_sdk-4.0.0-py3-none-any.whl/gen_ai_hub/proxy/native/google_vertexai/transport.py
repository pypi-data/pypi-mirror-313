import json
from typing import Dict, List, Optional, Sequence, Tuple, Union

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.cloud.aiplatform_v1beta1.services.prediction_service.transports import (
    PredictionServiceRestTransport as PredictionServiceRestTransport_,
)
from google.cloud.aiplatform_v1beta1.types import prediction_service
from google.protobuf import json_format

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


class PatchedPredictionServiceRestTransport(PredictionServiceRestTransport_):
    """PatchedPredictionServiceRestTransport is created to resolve an issue in the Vertex AI SDK.
    This class should be removed as soon as the bug is resolved upstream. The issue is that the
    Python requests library is not called with the parameter stream=True within the _StreamGenerateContents
    __call__ method. The __call__ method has been copied over and was only adjusted at places marked
    with PATCHED.
    Bug is reported at https://github.com/googleapis/gapic-generator-python/issues/2076.
    """

    # The original implementation of _StreamGenerateContent is missing the stream=True parameter in the call to the
    # proxy. This is necessary to enable streaming responses from the API.
    class _StreamGenerateContent(
        PredictionServiceRestTransport_._StreamGenerateContent
    ):
        def __call__(
            self,
            request: prediction_service.GenerateContentRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the stream generate content method over HTTP.

            Args:
                request (~.prediction_service.GenerateContentRequest):
                    The request object. Request message for [PredictionService.GenerateContent].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.prediction_service.GenerateContentResponse:
                    Response message for
                [PredictionService.GenerateContent].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta1/{model=projects/*/locations/*/endpoints/*}:streamGenerateContent",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1beta1/{model=projects/*/locations/*/publishers/*/models/*}:streamGenerateContent",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_stream_generate_content(
                request, metadata
            )
            pb_request = prediction_service.GenerateContentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=False
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                stream=True,  # PATCHED
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = rest_streaming.ResponseIterator(
                response, prediction_service.GenerateContentResponse
            )
            resp = self._interceptor.post_stream_generate_content(resp)
            return resp

        pass
