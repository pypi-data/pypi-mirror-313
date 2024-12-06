from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Union

from rich.console import Console

from .base_model import _BedrockModel

if TYPE_CHECKING:
    from botocore.config import Config

logger = logging.getLogger()

console = Console()


class MistralLarge(_BedrockModel):
    name = "Mistral-Large"

    def _model_params(self) -> dict:
        return {
            "max_tokens": 200,
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 50,
        }

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "mistral.mistral-large-2402-v1:0"
        super().__init__(
            boto_config=boto_config,
        )

    def _format_messages(self) -> str:
        formatted_messages = ["<s>[INST]"]
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            formatted_message = f"{role}: {content}"
            formatted_messages.append(formatted_message)
        formatted_messages.append("[/INST]")
        return "\n".join(formatted_messages)

    def _create_invoke_body(self) -> dict:
        prompt = self._format_messages()
        return {"prompt": prompt}

    def _handle_response(self, body: dict) -> str:
        response_message = body["outputs"][0]

        return response_message["text"]
