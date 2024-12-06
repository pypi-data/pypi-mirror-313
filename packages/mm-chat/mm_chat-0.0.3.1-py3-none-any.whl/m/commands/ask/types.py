from typing import TypedDict


class ChatOptions(TypedDict, total=False):
    model: str


class ChatConfig(TypedDict):
    openai_api_key: str
    openai_base_url: str
    options: ChatOptions
