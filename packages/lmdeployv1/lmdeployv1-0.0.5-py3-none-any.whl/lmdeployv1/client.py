#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : client
# Author  : zhoubohan
# Date    : 2024/11/29
# Time    : 14:18
# Description :
"""
import json
import os
from typing import Iterable, Union, List, Mapping

import httpx
from bceidaas.auth.bce_credentials import BceCredentials
from openai import (
    OpenAI,
    AsyncOpenAI,
    Stream,
    DEFAULT_MAX_RETRIES,
    NotGiven,
    NOT_GIVEN,
    Timeout,
)
from openai.pagination import SyncPage
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_content_part_image_param import (
    ImageURL,
)
from openai.types.model import Model
from tenacity import retry, stop_after_attempt

from lmdeployv1.api import BatchChatCompletionRequest, BatchChatCompletionResponse


class CustomOpenAI(OpenAI):
    """
    CustomOpenAI
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int = 2,
        default_headers: dict[str, str] | None = None,
        default_query: dict[str, object] | None = None,
        http_client=None,
        _strict_response_validation: bool = False,
    ) -> None:
        """
        Constructor
        :param api_key:
        :param organization:
        :param project:
        :param base_url:
        :param timeout:
        :param max_retries:
        :param default_headers:
        :param default_query:
        :param http_client:
        :param _strict_response_validation:
        """
        # 如果api_key为None,设置为空字符串
        if api_key is None:
            api_key = "sk-xxxxx"

        super().__init__(
            api_key=api_key,
            organization=organization,
            project=project,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )


class CustomAsyncOpenAI(AsyncOpenAI):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        # 自定义初始化逻辑
        if api_key is None:
            # 比如设置一个默认的api_key
            api_key = "sk-xxxx"

        super().__init__(
            api_key=api_key,
            organization=organization,
            project=project,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )


class LMDeployClient(object):
    """
    LMDeployClient is a client for lm deploy
    """

    def __init__(
        self,
        endpoint: str,
        base_url: str = "",
        credentials: BceCredentials = None,
        max_retries: int = 1,
        timeout_in_seconds: int = 30,
        is_async: bool = False,
    ):
        """
        Constructor
        """
        self._endpoint = endpoint
        self._base_url = base_url
        self._credentials = credentials
        self._is_async = is_async
        self._max_retries = max_retries
        self._timeout_in_seconds = timeout_in_seconds

        if self._base_url == "":
            self._base_url = "v1"

        self._endpoint = (
            self._endpoint.rstrip("/") + "/" + self._base_url.strip("/") + "/"
        )

        if is_async:
            self._openai_client = AsyncOpenAI(
                base_url=self._endpoint,
                max_retries=self._max_retries,
                timeout=self._timeout_in_seconds,
            )

            self._http_client = httpx.AsyncClient(
                base_url=self._endpoint,
                timeout=self._timeout_in_seconds,
            )

        else:
            self._openai_client = CustomOpenAI(
                base_url=self._endpoint,
                max_retries=self._max_retries,
                timeout=self._timeout_in_seconds,
            )

            self._http_client = httpx.Client(
                base_url=self._endpoint,
                timeout=self._timeout_in_seconds,
            )

    async def async_models(self) -> SyncPage[Model]:
        """
        Get models
        """
        return await self._openai_client.models.list()

    def models(self) -> SyncPage[Model]:
        """
        Get models
        """
        return self._openai_client.models.list()

    async def async_available_models(self) -> Union[str, ValueError]:
        """
        Async Get available models
        """
        models = await self.async_models()
        if len(models.data) == 0:
            return ValueError("No available models")

        return models.data[0].id

    def available_models(self) -> Union[str, ValueError]:
        """
        Get available models
        """
        models = self.models()
        if len(models.data) == 0:
            return ValueError("No available models")

        return models.data[0].id

    def chat_completion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: str = "",
        n: int = 1,
        max_completion_tokens: int = 512,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.6,
        frequency_penalty: float = 0.6,
        repetition_penalty: float = 1.2,
        stream: bool = False,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Chat completion
        """
        return self._openai_client.chat.completions.create(
            messages=messages,
            model=model,
            n=n,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=stream,
            extra_body={
                "repetition_penalty": repetition_penalty,
            },
        )

    async def chat_acompletion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: str = "",
        n: int = 1,
        max_completion_tokens: int = 512,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.6,
        frequency_penalty: float = 0.6,
        repetition_penalty: float = 1.2,
        stream: bool = False,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Async Chat completion
        """
        return await self._openai_client.chat.completions.create(
            messages=messages,
            model=model,
            n=n,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=stream,
            extra_body={
                "repetition_penalty": repetition_penalty,
            },
        )

    async def batch_chat_acompletion(
        self,
        request: BatchChatCompletionRequest,
    ) -> BatchChatCompletionResponse:
        """
        Async batch chat completion
        """

        @retry(stop=stop_after_attempt(self._max_retries), reraise=True)
        async def _batch_chat_acompletion(request):
            response = await self._http_client.post(
                url="chat/batch_completions",
                json=request,
            )

            await response.aclose()
            response.raise_for_status()

            return BatchChatCompletionResponse.model_validate(response.json())

        return await _batch_chat_acompletion(request.model_dump())

    def batch_chat_completion(
        self,
        request: BatchChatCompletionRequest,
    ) -> BatchChatCompletionResponse:
        """
        Batch chat completion
        """

        @retry(stop=stop_after_attempt(self._max_retries), reraise=True)
        def _batch_chat_completion(request):
            response = self._http_client.post(
                url="chat/batch_completions",
                json=request,
            )

            response.close()
            response.raise_for_status()

            return BatchChatCompletionResponse.model_validate(response.json())

        return _batch_chat_completion(request.model_dump())


def format_base64_string(s: str) -> str:
    """
    Format base64 string
    """
    return f"data:image/jpeg;base64,{s}"


def build_batch_chat_messages(
    kv_list: List[dict[str, str]]
) -> List[List[ChatCompletionMessageParam]]:
    """
    Build batch chat messages
    :param kv_list: List{"image_url":"prompt"}
    :return:
    """
    messages: List[List[ChatCompletionMessageParam]] = []

    for kv in kv_list:
        for img_url, prompt in kv.items():
            content: List[ChatCompletionContentPartParam] = []
            text_param = ChatCompletionContentPartTextParam(type="text", text=prompt)
            content.append(text_param)

            image_url = ImageURL(url=img_url)
            image_param = ChatCompletionContentPartImageParam(
                type="image_url", image_url=image_url
            )
            content.append(image_param)

            message_param = ChatCompletionUserMessageParam(role="user", content=content)

            messages.append([message_param])

    return messages


def build_chat_messages(kv: dict[str, str]) -> List[ChatCompletionMessageParam]:
    """
    Build chat messages
    :param kv: {"image_url":"prompt"}
    :return:
    """
    content: List[ChatCompletionContentPartParam] = []

    for img_url, prompt in kv.items():
        text_param = ChatCompletionContentPartTextParam(type="text", text=prompt)
        content.append(text_param)

        image_url = ImageURL(url=img_url)
        image_param = ChatCompletionContentPartImageParam(
            type="image_url", image_url=image_url
        )
        content.append(image_param)

    messages: List[ChatCompletionMessageParam] = []

    message_param = ChatCompletionUserMessageParam(role="user", content=content)

    messages.append(message_param)

    return messages


if __name__ == "__main__":
    from lmdeployv1.client import LMDeployClient, build_batch_chat_messages
    from lmdeployv1.api import BatchChatCompletionRequest

    def batch_lmdeploy_inference(uri):
        """
        batch_lmdeploy_inference
        """
        server_uri = "http://10.211.18.203:8312/ep-svcdukcq"
        msg_dict = {uri: "what is this?"}
        messages = build_batch_chat_messages(kv_list=[msg_dict])

        # 初始化大模型client
        client = LMDeployClient(
            endpoint=server_uri,
        )

        model = client.available_models()

        req = BatchChatCompletionRequest(
            model=model,
            messages=messages,
            temperature=0.2,
            top_p=0.1,
            repetition_penalty=0.5,
        )

        resp = client.batch_chat_completion(req)

        answer = [choice.message for choice in resp.choices]

        print(answer)

    if __name__ == "__main__":
        batch_lmdeploy_inference(
            "http://yijian-dev-int.bce.baidu.com:8320/resource/windmill/store/07e17c96439e4d5da9f9c9817e1d2ad5/workspaces/wsvykgec/projects/spiproject/annotationsets/as001/ry5Kxpqj/data/rabbit.jpeg"
        )
    # os.environ.clear()
    # c = LMDeployClient(endpoint="http://10.211.18.203:8312/ep-svcdukcq")
    # msg = build_batch_chat_messages(
    #     [
    #         {
    #             "http://tools.bj.bcebos.com/images/an.jpeg?authorization=bce-auth-v1%2FALTAKTZhksfCVgZJ96g46t21lA%2F2024-12-05T13%3A26%3A06Z%2F-1%2Fhost%2Fa86c867813d355e5b43f4738540391638866264eac4a796f3be9ed49d6cab849": "是否带了安全帽"
    #         }
    #     ]
    # )
    # req = BatchChatCompletionRequest(messages=msg)
    # # print(req.model_dump())
    # print(c.batch_chat_completion(BatchChatCompletionRequest(messages=msg)))
