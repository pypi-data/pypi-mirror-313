from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Union

from rich.console import Console

from .base_model import ConversationRole, _BedrockModel

if TYPE_CHECKING:
    from botocore.config import Config

logger = logging.getLogger()

console = Console()


class _Nova(_BedrockModel):
    date_stamp = datetime.now().strftime("%A, %B %d, %Y")  # noqa: DTZ005
    system_prompt = f"""
The current date is {date_stamp}.

Objective: To facilitate effective and safe interactions with users by providing accurate, helpful,
and contextually appropriate responses.

Guidelines:

    Clarity and Conciseness:
        Provide clear and concise answers to user queries.
        Avoid unnecessary jargon unless the user specifically requests it.

    Accuracy and Reliability:
        Base responses on verified and up-to-date information.
        When unsure, indicate uncertainty and suggest potential sources for verification.

    Context Awareness:
        Understand and maintain context throughout the conversation.
        Ask clarifying questions if the user's query is ambiguous.

    User-Centric Approach:
        Prioritize the user's needs and preferences.
        Use a friendly and respectful tone.

    Ethical Considerations:
        Avoid generating or promoting harmful, misleading, or inappropriate content.
        Respect user privacy and confidentiality.

    Limitations and Boundaries:
        Acknowledge limitations in knowledge and capabilities.
        Refrain from engaging in sensitive topics such as personal medical advice, legal advice, or financial advice.

    Feedback and Improvement:
        Encourage users to provide feedback on the interaction.
        Use feedback to improve and refine responses.

""".replace("\n", " ")

    def _model_params(self) -> dict:
        return {
            "inferenceConfig": {
                "maxTokens": 2000,
                "temperature": 0.7,
                "topP": 0.9,
                "stopSequences": ["\n\nHuman:"],
            },
            "system": [{"text": self.system_prompt}],
        }

    def _create_invoke_body(self) -> dict:
        return {
            "messages": self.messages,
        }

    def _handle_response(self, body: dict) -> str:
        response_message = body["output"]["message"]["content"][0]

        if "text" not in response_message:
            raise RuntimeError("Unexpected response type to prompt: " + response_message["type"])

        return response_message["text"]

    def append_message(self, role: ConversationRole, message: str) -> None:
        self.messages.append({"role": role.value, "content": [{"text": message}]})

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        super().__init__(
            boto_config=boto_config,
        )


class NovaMicro(_Nova):
    name = "Nova-Micro"

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "us.amazon.nova-micro-v1:0"

        super().__init__(
            boto_config=boto_config,
        )


class NovaLite(_Nova):
    name = "Nova-Lite"

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "us.amazon.nova-lite-v1:0"

        super().__init__(
            boto_config=boto_config,
        )


example = {
    "additionalModelRequestFields": {},
    "inferenceConfig": {"maxTokens": 512, "stopSequences": [], "temperature": 0.7, "topP": 0.9},
    "messages": [{"content": [{"text": "what is your name"}], "role": "user"}],
}


class NovaPro(_Nova):
    name = "Nova-Pro"

    def __init__(self, boto_config: Union[None, Config] = None) -> None:
        self._model_id = "us.amazon.nova-pro-v1:0"

        super().__init__(
            boto_config=boto_config,
        )
