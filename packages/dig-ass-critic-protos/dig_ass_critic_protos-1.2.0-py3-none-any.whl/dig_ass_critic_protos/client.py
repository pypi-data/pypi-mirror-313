from typing import Any
from uuid import uuid4

from agi_med_protos import HeaderClient
from loguru import logger

from . import DigitalAssistantCriticStub, DigitalAssistantCriticRequest, DigitalAssistantCriticResponse
from .dto import CriticRequest, CriticHeaders

type Metadata = list[tuple[str, int | bool | str]]


class CriticClient(HeaderClient[CriticRequest, CriticHeaders]):
    def __init__(self, address: str) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantCriticStub(self._channel)  # type: ignore[no-untyped-call]

    def __call__(self, request: CriticRequest) -> float:
        metadata: Metadata = self._generate_metadata(request.headers)
        grpc_request: DigitalAssistantCriticRequest = request.to_grpc_request()
        response: DigitalAssistantCriticResponse = self._stub.GetTextResponse(grpc_request, metadata=metadata)
        return response.Score

    def _generate_metadata(self, headers: CriticHeaders, **_: Any) -> Metadata:
        if not headers.get("extra_uuid"):
            extra_uuid = str(uuid4())
            logger.warning(f"Forgot extra_uuid in headers. Will be filling {extra_uuid=}")
            headers["extra_uuid"] = extra_uuid
        metadata: Metadata = super()._generate_metadata(headers)
        return metadata
