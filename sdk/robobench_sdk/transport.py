"""Byte transport between the runner and the controller process.

The runner binds an address and the controller connects to it. The transport
knows nothing about message contents; see `protocol` for that.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class TransportTimeout(Exception):
    """No data arrived within the requested timeout."""


class TransportClosed(Exception):
    """The other side disconnected."""


class Transport(ABC):
    @abstractmethod
    def send(self, data: bytes) -> None:
        """Send one message's bytes."""

    @abstractmethod
    def recv(self, timeout: float | None = None) -> bytes:
        """Block for one message. `timeout` in wall-clock seconds; None waits forever.

        Raises:
            TransportTimeout: nothing arrived in time.
            TransportClosed: the peer is gone.
        """

    @abstractmethod
    def poll(self, timeout: float = 0.0) -> bool:
        """Return True if a message is ready to `recv` without blocking."""

    @abstractmethod
    def close(self) -> None: ...


class ZmqTransport(Transport):
    """ZeroMQ PAIR socket transport. Works across processes and machines (tcp://, ipc://)."""

    @classmethod
    def bind(cls, address: str) -> "ZmqTransport":
        """Runner side. `address` like "tcp://127.0.0.1:0" (port 0 picks a free port)."""
        raise NotImplementedError

    @classmethod
    def connect(cls, address: str) -> "ZmqTransport":
        """Controller side."""
        raise NotImplementedError

    @property
    def address(self) -> str:
        """The concrete bound/connected address (with the real port filled in)."""
        raise NotImplementedError

    def send(self, data: bytes) -> None:
        raise NotImplementedError

    def recv(self, timeout: float | None = None) -> bytes:
        raise NotImplementedError

    def poll(self, timeout: float = 0.0) -> bool:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
