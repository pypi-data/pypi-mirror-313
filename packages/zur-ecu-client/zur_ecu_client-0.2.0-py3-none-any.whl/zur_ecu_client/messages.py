from dataclasses import dataclass
import json
from enum import Enum, IntEnum
from typing import List, Optional, Union

from zur_ecu_client.senml.senml_zur_names import SenmlNames
from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.util import value_by_key_prefix


class Messages:
    class AmiState(Enum):
        ACCELERATION = "acceleration"
        SKIDPAD = "skidpad"
        TRACKDRIVE = "trackdrive"
        BRAKETEST = "braketest"
        INSPECTION = "inspection"
        AUTOCROSS = "autocross"

    class EbsState(IntEnum):
        UNAVAILABLE = 1
        ARMED = 2
        ACTIVATED = 3

    class AsState(IntEnum):
        OFF = 1
        READY = 2
        DRIVING = 3
        EMERGENCY_BREAK = 4
        FINISH = 5

    @staticmethod
    def get_from_entry(data: dict):
        if "bn" in data:
            return Senml.Base.from_json(data)
        elif "n" in data:
            return Senml.Record.from_json(data)
        return TypeError

    @classmethod
    def parse(cls, data_str: str) -> dict:
        """
        Parses a senml content.
        Both a list with dictionary, or a list of list with dict are supported.
        e.g. both  `[{"bn": "DV", "n": "ctrl", "v": "sensor"}]` and
        `[[{"bn": "DV", "n": "ctrl", "v": "sensor"}], [{"bn": "DV", "n": "ctrl", "v": "other_value"}]]
        are supported.

        This was implemented this way, since the it was unclear which format the ECU used, or if both formats where used
        """
        data: List = json.loads(data_str)
        if len(data) == 0:
            return {}

        if isinstance(data[0], list):
            converted_data: dict = {}
            for msg in data:
                converted_data.update(cls.__parse_single_list_message(msg))
            return converted_data
        else:
            return cls.__parse_single_list_message(data)

    @staticmethod
    def __parse_single_list_message(data: List) -> dict:
        converted_data = {}
        device: str = ""
        topic: str = ""
        msg_type: str = ""
        header: str = ""
        for entry in data:
            if "bn" in entry:
                device = entry["bn"]
                topic = f':{entry["n"]}' if "n" in entry else ""
                msg_type = (
                    f':{value_by_key_prefix(entry, "v")}'
                    if value_by_key_prefix(entry, "v")
                    else ""
                )
                header = device + topic + msg_type
            else:
                data_name = SenmlNames(header + ":" + entry["n"])
                converted_data[data_name] = value_by_key_prefix(entry, "v")
        return converted_data


class Acknowledgment:
    def __init__(self, base: SenmlNames) -> None:
        self.base = base


class Data:
    def __init__(self, base: SenmlNames, data: List[SenmlNames]) -> None:
        self.base = base
        self.data = data
