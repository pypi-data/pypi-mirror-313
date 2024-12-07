from __future__ import annotations
import asyncio
from pydantic import parse_obj_as
import logging
import json
import httpx
from typing import Generator, List, Optional, Union

from gpt_router.models import (
    GPTRouterMetadata,
    ImageGenerationRequest,
    ImageGenerationResponse,
    ModelGenerationRequest,
    GenerationResponse,
    ChunkedGenerationResponse,
    ModelRouterEmbeddingsGenerationRequest,
    ModelRouterGenerationResponse,
    ModelRouterEmbeddingsGenerationResponse
)
from gpt_router.exceptions import (
    GPTRouterApiTimeoutError,
    GPTRouterBadRequestError,
    GPTRouterStreamingError,
    GPTRouterForbiddenError,
    GPTRouterInternalServerError,
    GPTRouterNotAvailableError,
    GPTRouterTooManyRequestsError,
    GPTRouterUnauthorizedError,
)
from gpt_router.constants import DEFAULT_REQUEST_TIMEOUT

from tenacity import (
    Retrying,
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

logger = logging.getLogger(__name__)

STATUS_CODE_EXCEPTION_MAPPING = {
    400: GPTRouterBadRequestError,
    406: GPTRouterNotAvailableError,
    401: GPTRouterUnauthorizedError,
    403: GPTRouterForbiddenError,
    429: GPTRouterTooManyRequestsError,
    500: GPTRouterInternalServerError,
    503: GPTRouterNotAvailableError,
}


class ServerError(Exception):
    pass


class GPTRouterClient:
    models = None
    request_timeout = DEFAULT_REQUEST_TIMEOUT

    def __init__(
        self,
        base_url,
        api_key,
        request_timeout: int = 60,
        stream_read_timeout: Optional[int] = None,
        additional_metadata: Optional[GPTRouterMetadata] = None,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.request_timeout = request_timeout
        self.additional_metadata = additional_metadata
        self.stream_read_timeout = (
            request_timeout if stream_read_timeout is None else stream_read_timeout
        )

    async def agenerate_embeddings(
        self,
        *,
        ordered_generation_requests: List[
            ModelRouterEmbeddingsGenerationRequest
        ],
        model_router_metadata: Optional[GPTRouterMetadata] = None,
    ) -> ModelRouterGenerationResponse:
        api_payload = {
            "data": [
                {
                    **request.dict(),
                    "order": index + 1,
                }
                for index, request in enumerate(ordered_generation_requests)
            ],
        }
        api_payload = self.add_metadata_info(api_payload, model_router_metadata)
        response = await self._async_api_call(
            path="/v1/generate/embeddings",
            method="POST",
            payload=api_payload,
        )
        return ModelRouterEmbeddingsGenerationResponse.parse_obj(response)

    def add_metadata_info(
        self,
        payload: dict,
        model_router_metadata: Optional[GPTRouterMetadata] = None,
    ):
        metadata = {}
        if self.additional_metadata:
            metadata.update(self.additional_metadata.dict())
        if model_router_metadata:
            metadata.update(model_router_metadata.dict())

        payload.update(
            {
                "metadata": metadata,
                "tag": metadata.get("tag"),
                "createdByUserId": metadata.get("created_by_user_id"),
                "historyId": (
                    str(metadata["history_id"]) if metadata.get("history_id") else None
                ),
                "appId": metadata.get("appId"),
            }
        )

        payload = {k: v for k, v in payload.items() if v is not None}
        return payload

    async def _async_api_call(self, *, path: str, method: str, payload: dict, **kwargs):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method,
                    url=self.base_url.rstrip("/")
                    + ("/api" if not self.base_url.endswith("/api") else "")
                    + path,
                    headers={
                        "content-type": "application/json",
                        "ws-secret": self.api_key,
                    },
                    json=payload,
                    timeout=self.request_timeout,
                )
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 202 or response.status_code == 204:
                    return None
                else:
                    error_class = STATUS_CODE_EXCEPTION_MAPPING.get(
                        response.status_code, Exception
                    )
                    raise error_class(response.json())
        except httpx.TimeoutException as err:
            logger.error(f"Timeout error: {err}")
            raise GPTRouterApiTimeoutError("Api Request timed out")

    def _api_call(self, *, path: str, method: str, payload: dict, **kwargs):
        try:
            with httpx.Client() as client:
                response = client.request(
                    method,
                    url=self.base_url.rstrip("/")
                    + ("/api" if not self.base_url.endswith("/api") else "")
                    + path,
                    headers={
                        "content-type": "application/json",
                        "ws-secret": self.api_key,
                    },
                    json=payload,
                    timeout=self.request_timeout,
                )
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 202 or response.status_code == 204:
                    return None
                else:
                    error_class = STATUS_CODE_EXCEPTION_MAPPING.get(
                        response.status_code, Exception
                    )
                    raise error_class(response.json())
        except httpx.TimeoutException as err:
            logger.error(f"Timeout error: {err}")
            raise GPTRouterApiTimeoutError("Api Request timed out")

    async def astream_events(self, *, path: str, method: str, payload: dict, **kwargs):
        retry_count = kwargs.get("stream_retry_count") or 1
        stop_stream_signal = kwargs.get("stop_stream_signal")
        async_retrying = AsyncRetrying(
            stop=stop_after_attempt(retry_count),
            wait=wait_fixed(0.5),
            retry=(
                retry_if_exception_type(httpx.ReadTimeout)
                | retry_if_exception_type(ServerError)
                | retry_if_exception_type(httpx.ReadError)
            ),
            before_sleep=lambda retry_state: logger.warn(
                f"Read timeout. Retrying... (Attempt {retry_state.attempt_number} of {retry_count})"
            ),
        )
        attempt_number = 0
        async for attempt in async_retrying:
            attempt_number += 1

            if attempt_number < retry_count:
                read_timeout = self.stream_read_timeout
            else:
                read_timeout = self.request_timeout
            try:
                async with httpx.AsyncClient() as client:
                    async with client.stream(
                        method,
                        url=self.base_url.rstrip("/")
                        + ("/api" if not self.base_url.endswith("/api") else "")
                        + path,
                        data=json.dumps(payload),
                        headers={
                            "Content-type": "application/json",
                            "ws-secret": self.api_key,
                        },
                        timeout=httpx.Timeout(self.request_timeout, read=read_timeout),
                    ) as response:
                        if response.status_code >= 500:
                            raise ServerError("Server error")
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if stop_stream_signal and stop_stream_signal.is_set():
                                logger.info("Stopping stream due to signal")
                                await response.aclose()
                                return
                            try:
                                if line.strip() == "":
                                    continue

                                line_type, line_data = (
                                    segment.strip() for segment in line.split(":", 1)
                                )

                                if line_type != "data":
                                    continue

                                data: dict = json.loads(line_data.strip())
                                if data["event"] == "error":
                                    raise GPTRouterStreamingError(data)
                                yield parse_obj_as(ChunkedGenerationResponse, data)
                            except GPTRouterStreamingError as e:
                                raise e
                            except Exception:
                                continue

                        return
            except (httpx.ReadTimeout, ServerError, httpx.ReadError) as err:
                logger.error(str(err))
                if attempt_number == retry_count:
                    logger.error("All retry attempts failed")
                    raise
            except httpx.HTTPStatusError as err:
                raise Exception(
                    f"HTTP Error {err.response.status_code}: {err.response.text}"
                ) from err
            except httpx.TimeoutException as err:
                raise TimeoutError("Request timed out") from err
            finally:
                if stop_stream_signal and stop_stream_signal.is_set():
                    logger.info("Stream stopped due to signal")
                    return

    def stream_events(
        self, *, path: str, method: str, payload: dict, **kwargs
    ) -> Generator[ChunkedGenerationResponse]:
        retry_count = kwargs.get("stream_retry_count") or 1
        retrying = Retrying(
            stop=stop_after_attempt(retry_count),
            wait=wait_fixed(0.5),
            retry=(
                retry_if_exception_type(httpx.ReadTimeout)
                | retry_if_exception_type(ServerError)
                | retry_if_exception_type(httpx.ReadError)
            ),
            before_sleep=lambda retry_state: logger.warn(
                f"Read timeout. Retrying... (Attempt {retry_state.attempt_number} of {retry_count})"
            ),
        )

        attempt_number = 0
        for attempt in retrying:
            attempt_number += 1

            if attempt_number < retry_count:
                read_timeout = self.stream_read_timeout
            else:
                read_timeout = self.request_timeout

            try:
                with httpx.Client() as client:
                    with client.stream(
                        method=method,
                        url=self.base_url.rstrip("/")
                        + ("/api" if not self.base_url.endswith("/api") else "")
                        + path,
                        data=json.dumps(payload),
                        headers={
                            "Content-type": "application/json",
                            "ws-secret": self.api_key,
                        },
                        timeout=httpx.Timeout(self.request_timeout, read=read_timeout),
                    ) as response:
                        if response.status_code >= 500:
                            raise ServerError("Server error")
                        response.raise_for_status()
                        for line in response.iter_lines():
                            try:
                                if line.strip() == "":
                                    continue

                                line_type, line_data = (
                                    segment.strip() for segment in line.split(":", 1)
                                )
                                if line_type != "data":
                                    continue

                                data = json.loads(line_data.strip())
                                if data["event"].lower() == "error":
                                    raise GPTRouterStreamingError(data["message"])
                                yield parse_obj_as(ChunkedGenerationResponse, data)
                            except GPTRouterStreamingError as e:
                                raise e
                            except Exception:
                                continue
                        return
            except (httpx.ReadTimeout, ServerError, httpx.ReadError) as err:
                logger.error(str(err))
                if attempt_number == retry_count:
                    logger.error("All retry attempts failed")
                    raise
            except httpx.HTTPStatusError as err:
                raise Exception(
                    f"HTTP Error {err.response.status_code}: {err.response.text}"
                ) from err
            except httpx.TimeoutException as err:
                raise TimeoutError("Request timed out") from err

    def generate(
        self,
        *,
        ordered_generation_requests: List[ModelGenerationRequest],
        is_stream=False,
        model_router_metadata: Optional[GPTRouterMetadata] = None,
        **kwargs,
    ) -> Union[GenerationResponse, Generator[ChunkedGenerationResponse]]:
        api_path = "/v1/generate"
        api_method = "POST"
        api_payload = {
            "stream": is_stream,
            "data": [
                request.dict(exclude_none=True, by_alias=True)
                for request in ordered_generation_requests
            ],
        }
        api_payload = self.add_metadata_info(api_payload, model_router_metadata)
        if is_stream:
            return self.stream_events(
                path=api_path,
                method=api_method,
                payload=api_payload,
                **kwargs,
            )
        result = self._api_call(
            path=api_path,
            method=api_method,
            payload=api_payload,
            **kwargs,
        )
        return parse_obj_as(GenerationResponse, result)

    async def agenerate(
        self,
        *,
        ordered_generation_requests: List[ModelGenerationRequest],
        is_stream=False,
        model_router_metadata: Optional[GPTRouterMetadata] = None,
        stop_stream_signal: Optional[asyncio.Event] = None,
        **kwargs,
    ) -> GenerationResponse:
        api_path = "/v1/generate"
        api_method = "POST"
        api_payload = {
            "stream": is_stream,
            "data": [
                request.dict(exclude_none=True, by_alias=True)
                for request in ordered_generation_requests
            ],
        }
        api_payload = self.add_metadata_info(api_payload, model_router_metadata)
        if is_stream:
            return self.astream_events(
                path=api_path,
                method=api_method,
                payload=api_payload,
                stop_stream_signal=stop_stream_signal,
                **kwargs,
            )
        result = await self._async_api_call(
            path=api_path,
            method=api_method,
            payload=api_payload,
            **kwargs,
        )
        return parse_obj_as(GenerationResponse, result)

    async def agenerate_images(
        self, *, image_generation_request: ImageGenerationRequest
    ) -> List[ImageGenerationResponse]:
        api_path = "/v1/generate/generate-image"
        api_method = "POST"
        api_payload = image_generation_request.dict()

        api_response = await self._async_api_call(
            path=api_path,
            method=api_method,
            payload=api_payload,
        )
        generated_images = api_response.get("response", [])
        if isinstance(generated_images, dict):
            generated_images = self._extract_images_from_dict(generated_images)

        return [
            parse_obj_as(ImageGenerationResponse, generated_img)
            for generated_img in generated_images
        ]

    def _extract_images_from_dict(self, image_dict: dict) -> List[dict]:
        if artifacts := image_dict.get("artifacts"):
            return artifacts
        
        if image_urls := image_dict.get("imageUrls"):
            return [{"url": url} for url in image_urls]

        return []
