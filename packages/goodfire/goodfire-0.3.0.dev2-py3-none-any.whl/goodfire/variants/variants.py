from typing import Literal, Protocol

from ..controller.controller import Controller

SUPPORTED_MODELS = Literal[
    "meta-llama/Meta-Llama-3-8B-Instruct", "meta-llama/Meta-Llama-3.1-70B-Instruct"
]


class VariantInterface(Protocol):
    base_model: SUPPORTED_MODELS

    @property
    def controller(self) -> Controller: ...
