import pickle
from threading import Lock
from typing import Any

from quantplay.model.instrument_data import InstrumentDataType


class PickleUtils:
    @staticmethod
    def save_data(data: Any, file_name: str):
        with open(f"/tmp/{file_name}.pickle", "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_data(file_name: str):
        with open(f"/tmp/{file_name}.pickle", "rb") as disk_data:
            unserialized_data = pickle.load(disk_data)

        return unserialized_data


class InstrumentData:
    __instance = None

    @staticmethod
    def get_instance():
        if InstrumentData.__instance is None:
            InstrumentData()

        return InstrumentData.__instance

    def __init__(self) -> None:
        if InstrumentData.__instance is not None:
            raise Exception("Instrument Data load failed")

        self.instrument_data: dict[str, dict[str, InstrumentDataType]] = {}
        self.lock = Lock()

        InstrumentData.__instance = self

    def load_data(self, file_name: str):
        if file_name in self.instrument_data:
            return self.instrument_data[file_name]

        try:
            self.lock.acquire()
            with open(f"/tmp/{file_name}.pickle", "rb") as disk_data:
                unserialized_data = pickle.load(disk_data)
            self.instrument_data[file_name] = unserialized_data
            self.lock.release()
        except Exception:
            self.lock.release()
            raise Exception(f"file [{file_name}] not found on disk")

        return self.instrument_data[file_name]
