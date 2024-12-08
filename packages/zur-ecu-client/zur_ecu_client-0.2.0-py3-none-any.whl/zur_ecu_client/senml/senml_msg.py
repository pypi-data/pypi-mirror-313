from typing import List

from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.senml.senml_unit import SenmlUnit
from zur_ecu_client.senml.senml_zur_names import SenmlNames


class SenmlMessage:
    def __init__(self, msg_type: SenmlNames, msg_map: List[Senml.Record]) -> None:
        msg_type: List = msg_type.value.split(":")
        self.baseName = msg_type[0]
        self.name = msg_type[1]
        self.value = msg_type[2] if len(msg_type) > 2 else ""
        self.map = msg_map

    def get(self):
        msg = []
        msg_base = {"bn": self.baseName, "n": self.name}
        if self.value:
            msg_base["vs"] = self.value
        msg.append(msg_base)
        for item in self.map:
            if item.v is None:
                continue
            key = item.n.value.split(":")[-1]
            if type(item.v) is str:
                msg.append({"n": key, "vs": item.v})
            elif type(item.v) is bool:
                msg.append({"n": key, "vb": item.v})
            elif type(item.u) is SenmlUnit:
                msg.append({"n": key, "u": item.u.value, "v": item.v})
            else:
                msg.append({"n": key, "v": item.v})
        return msg
