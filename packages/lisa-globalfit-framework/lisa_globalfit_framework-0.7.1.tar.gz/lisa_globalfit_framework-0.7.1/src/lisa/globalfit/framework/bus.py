from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

from deprecated import deprecated

from lisa.globalfit.framework.msg.subjects import Subject


@deprecated(reason="use PullEventBus instead")
class EventBus:
    async def connect(self) -> None:
        pass

    async def publish(self, subject: Subject, data: bytes) -> None:
        pass

    async def subscribe(self, subject: Subject, callback: Callable) -> None:
        pass

    async def unsubscribe(self, subject: Subject) -> None:
        pass

    async def close(self) -> None:
        pass


@dataclass
class MessageStream:
    name: str
    subjects: list[Subject]


class AckMessage(ABC):
    @abstractmethod
    async def ack(self) -> None: ...

    @abstractmethod
    async def in_progress(self) -> None: ...

    @abstractmethod
    async def nack(self) -> None: ...

    @abstractmethod
    async def discard(self) -> None: ...

    @property
    @abstractmethod
    def data(self) -> bytes: ...

    @property
    @abstractmethod
    def subject(self) -> Subject: ...


class PullSubscriber(ABC):
    @abstractmethod
    async def fetch_message(self) -> AckMessage: ...

    @abstractmethod
    async def unsubscribe(self) -> None: ...


class PullEventBus(ABC):
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def add_stream(self, stream: MessageStream) -> None: ...

    @abstractmethod
    async def subscribe(
        self, subject: Subject, durable: str | None
    ) -> PullSubscriber: ...

    @abstractmethod
    async def publish(self, subject: Subject, data: bytes) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
