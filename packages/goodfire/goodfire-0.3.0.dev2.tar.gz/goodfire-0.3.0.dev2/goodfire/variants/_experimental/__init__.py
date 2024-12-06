from ...controller.controller import Controller
from ...utils.logger import logger
from ..variants import SUPPORTED_MODELS, VariantInterface

has_warned = False


class ProgrammableVariant(VariantInterface):
    """A programmable variant which takes in a controller object. See the conditional
    feature interventions section of the advanced notebook for example usage."""

    def __init__(self, base_model: SUPPORTED_MODELS):
        global has_warned

        if not has_warned:
            logger.warning(
                "ProgrammableVariants are an experimental feature and may change in the future."
            )
            has_warned = True

        self.base_model = base_model
        self._controller = Controller()

    @property
    def controller(self) -> Controller:
        return self._controller

    def reset(self):
        self._controller = Controller()
