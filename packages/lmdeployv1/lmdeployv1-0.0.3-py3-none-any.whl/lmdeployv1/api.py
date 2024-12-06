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
from typing import Optional, List, Literal
from pydantic import BaseModel

from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionMessage
from openai.types.chat.chat_completion import ChoiceLogprobs


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
