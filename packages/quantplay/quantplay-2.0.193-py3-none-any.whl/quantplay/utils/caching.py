from threading import Event, Thread
from time import sleep
from typing import Any, Hashable


class InstrumentCache:
    def __init__(self) -> None:
        self.cache: dict[Hashable, Any] = {}
        self.ttl = 300

        self.stop_event = Event()
        self.stop_event.set()

        clear_thread = Thread(target=self.auto_clear, daemon=True)
        clear_thread.start()

    def __del__(self) -> None:
        self.stop_event.clear()

    def set(self, key: str, data: Any) -> None:
        self.cache[key] = data

    def get(self, key: str) -> Any | None:
        return self.cache.get(key, None)

    def delete(self, key: str) -> None:
        del self.cache[key]

    def clear(self) -> None:
        self.cache = {}

    def auto_clear(self) -> None:
        while self.stop_event.is_set():
            sleep(self.ttl)
            self.clear()
