from enum import Enum

from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_zur_names import SenmlNames
from zur_ecu_client.senml.util import value_by_key_prefix


class Senml:
    class Type(Enum):
        REQUEST = 1
        DATA = 2
        ACKNOWLEDGMENT = 3

    class Base:
        def __init__(self, bn, n, v):
            self.bn = bn
            self.n = n
            self.v = v

        @classmethod
        def from_json(cls, data):
            device = data["bn"]
            topic = f':{data["n"]}' if "n" in data else ""
            msg_type = (
                f':{value_by_key_prefix(data, "v")}'
                if value_by_key_prefix(data, "v")
                else ""
            )
            return cls(device, topic, msg_type)

    class Record:
        def __init__(self, n: SenmlNames, u: SenmlUnit = None, v: any = None):
            self.n = n
            self.u = u
            self.v = v

        @classmethod
        def from_json(cls, data):
            device = data["n"]
            unit = f':{data["u"]}' if "u" in data else None
            value = (
                f':{value_by_key_prefix(data, "v")}'
                if value_by_key_prefix(data, "v")
                else ""
            )
            return cls(device, unit, value)

    class Pack:
        def __init__(self, base, records: list = None):
            self.records = []
            self.base = base
            if records:
                self.records.append(records)
