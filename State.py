from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from collections.abc import Sequence

class State(TypedDict):
    messages: Sequence[BaseMessage]
    summary: str  