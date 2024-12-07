#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : example
# Author  : zhoubohan
# Date    : 2024/12/6
# Time    : 11:37
# Description :
"""
from lmdeployv1.client import (
    LMDeployClient,
    build_chat_messages,
    build_batch_chat_messages,
)

from lmdeployv1.api import BatchChatCompletionRequest

endpoint_uri = "http://10.211.18.203:8312/ep-svcdukcq"
client = LMDeployClient(endpoint=endpoint_uri)
image_url = "http://tools.bj.bcebos.com/images/an.jpeg?authorization=bce-auth-v1%2FALTAKTZhksfCVgZJ96g46t21lA%2F2024-12-06T03%3A41%3A30Z%2F-1%2Fhost%2F524f024252d15ac895f6f41ecf53ff57a53a03cb70d1656a46ace7e39d572041"
message = {image_url: "Is there any cat in the image? only answer yes or no."}


def test_chat_completion():
    req = build_chat_messages(message)
    resp = client.chat_completion(messages=req)
    choice = [c.message for c in resp.choices]
    assert len(choice[0].content) > 1
    print(f"chat response: {choice[0].content}")


def test_batch_chat_completion():
    msg = build_batch_chat_messages([message])
    resp = client.batch_chat_completion(BatchChatCompletionRequest(messages=msg))
    choice = [c.message for c in resp.choices]
    assert len(choice[0].content) > 1
    print(f"batch chat response: {choice[0].content}")


if __name__ == "__main__":
    test_chat_completion()
    test_batch_chat_completion()
