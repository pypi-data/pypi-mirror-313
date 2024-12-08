import abc

from typing import Literal, Optional

from clipped.compact.pydantic import Field
from clipped.config.schema import BaseSchemaModel
from clipped.utils.enums import PEnum

from congruent.schemas.message import Message
from congruent.utils.tokens import count_tokens


class HistoryKind(str, PEnum):
    MEMORY = "memory"


class History(BaseSchemaModel):
    _USE_DISCRIMINATOR = True

    @abc.abstractmethod
    def add_message(self, message: Message):
        raise NotImplementedError()

    @abc.abstractmethod
    def _load_messages(self, n: int = None) -> list[Message]:
        raise NotImplementedError()

    def get_messages(self, n: int = None, max_tokens: int = None) -> list[Message]:
        messages = self._load_messages(n=n)

        # sort in reverse timestamp order
        messages = sorted(messages, key=lambda m: m.timestamp, reverse=True)

        if max_tokens is None:
            final_messages = messages
        else:
            total_tokens = 0
            final_messages = []
            for msg in messages:
                msg_tokens = count_tokens(msg.content)
                if total_tokens + msg_tokens > max_tokens:
                    break
                else:
                    final_messages.append(msg)
                    total_tokens += msg_tokens

        return list(reversed(final_messages))

    @abc.abstractmethod
    def clear(self):
        raise NotImplementedError()


class MemoryHistory(History):
    _IDENTIFIER = HistoryKind.MEMORY

    kind: Literal[_IDENTIFIER] = _IDENTIFIER
    messages: list[Message] = Field(default_factory=list)
    max_messages: Optional[int] = None

    def add_message(self, message: Message):
        self.messages.append(message)
        if self.max_messages is not None:
            self.messages = self.messages[-self.max_messages :]

    def _load_messages(self, last_n: int = None) -> list[Message]:
        if last_n is None:
            return self.messages.copy()
        return self.messages[-last_n:]

    def clear(self):
        self.messages.clear()
