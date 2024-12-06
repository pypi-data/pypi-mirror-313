from functools import cache

from m.config.load import load_config

from .types import ChatConfig

chat_config: ChatConfig = load_config()["chat"]  # type: ignore

default_model = chat_config["options"].get("model", "gpt-4o-mini")


@cache
def get_client():
    from promplate.llm.openai import SyncChatOpenAI

    return SyncChatOpenAI(api_key=chat_config.get("openai_api_key"), base_url=chat_config.get("openai_base_url"))
