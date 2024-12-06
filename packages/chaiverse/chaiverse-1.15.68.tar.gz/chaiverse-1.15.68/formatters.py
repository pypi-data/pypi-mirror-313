from dataclasses import dataclass
from functools import lru_cache
from inspect import isclass
from typing import Optional, List
import sys

from pydantic import BaseModel, Field, validator


class _PromptFormatter(BaseModel):
    memory_template: Optional[str] = Field(default = "{bot_name}'s Persona: {memory}\n####\n")
    prompt_template: Optional[str] = Field(
        default="{prompt}\n<START>\n"
    )
    bot_template: str = Field(default="{bot_name}: {message}\n")
    user_template: str = Field(default="{user_name}: {message}\n")
    response_template: str = Field(default="{bot_name}:")
    truncate_by_message: Optional[bool] = Field(default=False)

    # TODO: Need to do this to test the XL reward model
    #       Consider actually deleting this, or reworking how the validation
    #       works so that it only happens on the submission

    #@validator("memory_template")
    #def validate_memory(cls, memory_template):
    #    if "{memory}" not in memory_template:
    #        raise ValueError("Formatter's memory_template must contain '{memory}'!")
    #    return memory_template

    #@validator("prompt_template")
    #def validate_formatter(cls, prompt_template):
    #    if "{prompt}" not in prompt_template:
    #        raise ValueError("Formatter's prompt_template must contain '{prompt}'!")
    #    return prompt_template

    #@validator("bot_template")
    #def validate_bot(cls, bot_template):
    #    if "{message}" not in bot_template:
    #        raise ValueError("Formatter's bot_template must contain '{message}'!")
    #    return bot_template

    #@validator("user_template")
    #def validate_user(cls, user_template):
    #    if "{message}" not in user_template:
    #        raise ValueError("Formatter's user_template must contain '{message}'!")
    #    return user_template


class PygmalionFormatter(_PromptFormatter):
    pass


class VicunaFormatter(_PromptFormatter):
    memory_template: str = "### Instruction:\n{memory}\n"
    prompt_template: str = "### Input:\n{prompt}\n"
    bot_template: str = "{bot_name}: {message}\n"
    user_template: str = "{user_name}: {message}\n"
    response_template: str = "### Response:\n{bot_name}:"


class ChatMLFormatter(_PromptFormatter):
    memory_template: str = "<|im_start|>system\n{memory}<|im_end|>\n"
    prompt_template: str = "<|im_start|>user\n{prompt}<|im_end|>\n"
    bot_template: str = "<|im_start|>assistant\n{bot_name}: {message}<|im_end|>\n"
    user_template: str = "<|im_start|>user\n{user_name}: {message}<|im_end|>\n"
    response_template: str = "<|im_start|>assistant\n{bot_name}:"


class EmptyFormatter(_PromptFormatter):
    memory_template: str = ""
    prompt_template: str = ""
    bot_template: str = ""
    user_template: str = ""
    response_template: str = ""


class XLRewardFormatter(_PromptFormatter):
    memory_template: str = ""
    prompt_template: str = ""
    bot_template: str = Field(default="{bot_name}: {message}\n")
    user_template: str = Field(default="{user_name}: {message}\n")
    response_template: str = ""


class ModeratorFormatter(_PromptFormatter):
    memory_template: str = "{memory}\n"
    prompt_template: str = "{prompt}\n"
    bot_template: str = "{bot_name}: {message}\n"
    user_template: str = "{user_name}: {message}\n"
    response_template: str = ""


@lru_cache()
def get_available_formatters():
    formatters = {}
    current_module = sys.modules[__name__]
    for key in dir(current_module):
        cls = getattr(current_module, key)
        if isclass(cls) and issubclass(cls, _PromptFormatter) and ("PromptFormatter" not in key):
            key = key.replace("Formatter", "")
            formatters[key] = cls()
    return formatters


class PromptFormatter(_PromptFormatter):
    memory_template: Optional[str] = Field(
        title="Memory template",
        description="A template controlling how your model handles a bot's permanent memory. Must contain `{memory}`.",
        default = "{bot_name}'s Persona: {memory}\n####\n",
        enum=[formatter.memory_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    prompt_template: Optional[str] = Field(
        title="Prompt template",
        description="A template controlling how your model handles a bot temporary prompt. Must contain `{prompt}'.",
        default="{prompt}\n<START>\n",
        enum=[formatter.prompt_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    bot_template: str = Field(
        title="Bot message template",
        description="A template controlling how your model handles a bot's messages. Must contain `{bot_name}' and `{message}'.",
        default="{bot_name}: {message}\n",
        enum=[formatter.bot_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    user_template: str = Field(
        title="User message template",
        description="A template controlling how your model handles the user's messages. Must contain `{user_name}' and `{message}'.",
        default="{user_name}: {message}\n",
        enum=[formatter.user_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    response_template: str = Field(
        title="Bot response template",
        description="A template controlling how your model is prompted for a bot response. Must contain `{bot_name}'.",
        default="{bot_name}:",
        enum=[formatter.response_template for formatter in get_available_formatters().values()],
        format="select2",
        options={
            "enum_titles": list(get_available_formatters().keys()),
            "select2": {
                "tags": True,
            }
        }
    )
    truncate_by_message: Optional[bool] = Field(
        title="Truncate by message",
        description="Truncate the conversation history in the context window on a message-by-message basis, rather than a character-by-character basis.",
        default=False,
        format="checkbox"
    )
