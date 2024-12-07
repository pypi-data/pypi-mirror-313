from dataclasses import dataclass
from typing import Any

from agi_med_common.models import ChatItem
from agi_med_protos.dto import RequestWithHeaders
from google.protobuf.json_format import ParseDict

from . import CriticHeaders
from .. import DigitalAssistantCriticRequest


@dataclass
class CriticRequest(RequestWithHeaders[CriticHeaders]):
    text: str
    chat: ChatItem

    def to_grpc_request(self) -> DigitalAssistantCriticRequest:
        grpc_request = DigitalAssistantCriticRequest()
        req_dict: dict[str, Any] = {"Text": self.text, "Chat": self.chat.model_dump(by_alias=True)}
        ParseDict(req_dict, grpc_request, ignore_unknown_fields=True)
        return grpc_request
