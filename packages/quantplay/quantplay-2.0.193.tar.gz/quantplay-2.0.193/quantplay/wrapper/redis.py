import traceback
import redis  # type:ignore
from os import environ


class Redis:
    error = False
    __instance = None

    @staticmethod
    def get_instance():
        if Redis.__instance is None:
            Redis()

        return Redis.__instance

    def __init__(self) -> None:
        print("Creating Redis instance")
        if (
            environ.get("REDIS_HOST") is None
            or environ.get("REDIS_PORT") is None
            or environ.get("REDIS_PASSWORD") is None
        ):
            self.error = True
            return

        try:
            self.redis_client = redis.Redis(
                host=environ.get("REDIS_HOST", ""),
                port=int(environ.get("REDIS_PORT", 0)),
                password=environ.get("REDIS_PASSWORD", ""),
                decode_responses=True,
                ssl=True,
            )

        except Exception:
            traceback.print_exc()
            self.error = True

        Redis.__instance = self

    def get(self, key: int) -> None:
        if self.error:
            return None

        return self.redis_client.get(f"mkt:{key}")  # type: ignore

    def mget(self, keys: list[int]) -> None:
        if self.error:
            return None

        return self.redis_client.mget([f"mkt:{key}" for key in keys])  # type: ignore
