# Copyright 2022-2023 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xinference.model.llm.llm_family import PromptStyleV1

from ....types import ChatCompletionMessage
from ..utils import ChatModelMixin


def test_prompt_style_add_colon_single():
    prompt_style = PromptStyleV1(
        style_name="ADD_COLON_SINGLE",
        system_prompt=(
            "A chat between a curious human and an artificial intelligence assistant. The "
            "assistant gives helpful, detailed, and polite answers to the human's questions."
        ),
        roles=["user", "assistant"],
        intra_message_sep="\n### ",
    )
    chat_history = [
        ChatCompletionMessage(role=prompt_style.roles[0], content="Hi there."),
        ChatCompletionMessage(
            role=prompt_style.roles[1], content="Hello, how may I help you?"
        ),
    ]
    expected = (
        "A chat between a curious human and an artificial intelligence assistant. The assistant"
        " gives helpful, detailed, and polite answers to the human's questions."
        "\n### user: Hi there."
        "\n### assistant: Hello, how may I help you?"
        "\n### user: Write a poem."
        "\n### assistant:"
    )
    assert expected == ChatModelMixin.get_prompt(
        "Write a poem.", chat_history, prompt_style
    )


def test_prompt_style_add_colon_two():
    prompt_style = PromptStyleV1(
        style_name="ADD_COLON_TWO",
        system_prompt=(
            "A chat between a curious user and an artificial intelligence assistant. The "
            "assistant gives helpful, detailed, and polite answers to the user's questions."
        ),
        roles=["USER", "ASSISTANT"],
        intra_message_sep=" ",
        inter_message_sep="</s>",
    )
    chat_history = [
        ChatCompletionMessage(role=prompt_style.roles[0], content="Hi there."),
        ChatCompletionMessage(
            role=prompt_style.roles[1], content="Hello, how may I help you?"
        ),
    ]
    expected = (
        "A chat between a curious user and an artificial intelligence assistant. The "
        "assistant gives helpful, detailed, and polite answers to the user's questions. "
        "USER: Hi there. "
        "ASSISTANT: Hello, how may I help you?</s>"
        "USER: Write a poem. "
        "ASSISTANT:"
    )
    assert expected == ChatModelMixin.get_prompt(
        "Write a poem.", chat_history, prompt_style
    )


def test_prompt_style_no_colon_two():
    prompt_style = PromptStyleV1(
        style_name="NO_COLON_TWO",
        system_prompt="",
        roles=[" <reserved_102> ", " <reserved_103> "],
        intra_message_sep="",
        inter_message_sep="</s>",
        stop_token_ids=[2, 195],
    )
    chat_history = [
        ChatCompletionMessage(role=prompt_style.roles[0], content="Hi there."),
        ChatCompletionMessage(
            role=prompt_style.roles[1], content="Hello, how may I help you?"
        ),
    ]
    expected = (
        " <reserved_102> Hi there."
        " <reserved_103> Hello, how may I help you?</s>"
        " <reserved_102> Write a poem."
        " <reserved_103> "
    )
    assert expected == ChatModelMixin.get_prompt(
        "Write a poem.", chat_history, prompt_style
    )


def test_prompt_style_llama2():
    prompt_style = PromptStyleV1(
        style_name="LLAMA2",
        system_prompt=(
            "<s>[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer"
            " as helpfully as possible, while being safe. Your answers should not include any"
            " harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please"
            " ensure that your responses are socially unbiased and positive in nature.\n\nIf a"
            " question does not make any sense, or is not factually coherent, explain why instead"
            " of answering something not correct. If you don't know the answer to a question,"
            " please don't share false information.\n<</SYS>>\n\n"
        ),
        roles=["[INST]", "[/INST]"],
        intra_message_sep=" ",
        inter_message_sep=" </s><s>",
        stop_token_ids=[2],
    )
    chat_history = [
        ChatCompletionMessage(role=prompt_style.roles[0], content="Hi there."),
        ChatCompletionMessage(
            role=prompt_style.roles[1], content="Hello, how may I help you?"
        ),
    ]
    expected = (
        "<s>[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer"
        " as helpfully as possible, while being safe. Your answers should not include any"
        " harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please"
        " ensure that your responses are socially unbiased and positive in nature.\n\nIf a"
        " question does not make any sense, or is not factually coherent, explain why instead"
        " of answering something not correct. If you don't know the answer to a question,"
        " please don't share false information.\n<</SYS>>\n\nHi there.[/INST] Hello, how may I help"
        " you? </s><s>[INST] Write a poem. [/INST]"
    )
    assert expected == ChatModelMixin.get_prompt(
        "Write a poem.", chat_history, prompt_style
    )
