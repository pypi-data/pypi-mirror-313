#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : api
# Author  : zhoubohan
# Date    : 2024/12/4
# Time    : 11:40
# Description :
"""
from typing import Optional, List, Literal, Iterable

from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChoiceLogprobs
from pydantic import BaseModel, field_serializer


class BatchChatChoice(BaseModel):
    """
    BatchChatChoice
    """

    index: int
    logprobs: Optional[ChoiceLogprobs] = None
    message: ChatCompletionMessage
    finish_reason: Literal[
        "stop", "length", "tool_calls", "content_filter", "function_call"
    ]
    usage: Optional[CompletionUsage] = None


class BatchChatCompletionRequest(BaseModel):
    """
    BatchChatCompletionRequest
    """

    messages: List[List[ChatCompletionMessageParam]]
    model: str = ""
    n: int = 1
    max_completion_tokens: int = 512
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 1.0
    presence_penalty: float = 0.6
    frequency_penalty: float = 0.6
    repetition_penalty: float = 1.2
    stream: bool = False

    @field_serializer("messages")
    def serialize_messages(
        self, messages: List[List[ChatCompletionMessageParam]], _info
    ):
        """
        serialize_messages: 解决ChatCompletionMessageParam包含复杂序列器的问题
        :param messages:
        :param _info:
        :return:
        """

        def serialize_message(msg):
            if isinstance(msg, dict):
                if isinstance(msg.get("content"), Iterable) and not isinstance(
                    msg["content"], str
                ):
                    msg["content"] = list(msg["content"])
            return msg

        return [[serialize_message(m) for m in sublist] for sublist in messages]


class BatchChatCompletionResponse(BaseModel):
    """
    BatchChatCompletionResponse
    """

    id: str
    choices: List[BatchChatChoice]
    created: int
    model: str
    object: Literal["batch.chat.completion"]
    service_tier: Optional[Literal["scale", "default"]] = None
    system_fingerprint: Optional[str] = None
    usage: Optional[CompletionUsage] = None
