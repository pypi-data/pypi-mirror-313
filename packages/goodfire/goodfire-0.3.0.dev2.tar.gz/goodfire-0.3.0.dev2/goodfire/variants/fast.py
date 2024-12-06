from collections import OrderedDict
from typing import Literal, Union, overload

from typing_extensions import TypedDict

from ..controller.controller import Controller
from ..features.features import Feature, FeatureGroup
from .variants import SUPPORTED_MODELS, VariantInterface


class FeatureDelta(TypedDict):
    mode: Literal["nudge", "pin"]
    value: Union[float, bool]


class FeatureEdits:
    """A collection of feature modifications with ordered tracking.

    This class manages a set of feature edits using an OrderedDict to maintain
    the order in which edits were applied.
    """

    def __init__(self):
        self._edits: OrderedDict[Feature, FeatureDelta] = OrderedDict()

    def __getitem__(self, feature: Feature) -> FeatureDelta:
        return self._edits[feature]

    def __setitem__(self, feature: Feature, delta: FeatureDelta):
        self._edits[feature] = delta

    def __delitem__(self, feature: Feature):
        self._edits.pop(feature, None)

    def __iter__(self):
        return iter(list(self._edits.items()))

    def __len__(self):
        return len(self._edits)


class Variant(VariantInterface):
    """A class representing a variant of a base model with feature modifications.

    This class allows for creating variants of a base model by applying
    feature modifications through either nudging or pinning values.

    Args:
        base_model (str): Identifier of the base model to create variants from

    Attributes:
        base_model (str): The base model identifier
        edits (FeatureEdits): Collection of feature modifications
    """

    def __init__(self, base_model: SUPPORTED_MODELS):
        self.base_model = base_model
        self.edits: FeatureEdits = FeatureEdits()

    @overload
    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, None],
        mode: Literal["nudge"] = "nudge",
    ) -> None: ...

    @overload
    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, bool, None],
        mode: Literal["pin"] = "pin",
    ) -> None: ...

    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, bool, None],
        mode: Literal["nudge", "pin"] = "nudge",
    ):
        """Set or modify feature values in the variant.

        Args:
            feature (Union[Feature, FeatureGroup]): Feature(s) to modify
            value (Union[float, bool, None]): Value to apply:
                - float: For numerical adjustments
                - bool: For binary states (pin mode only)
                - None: To clear the modification

            mode (Literal["nudge", "pin"], optional): Modification mode:
                - "nudge": Bias the feature strength
                - "pin": Set the feature strength to a fixed value

                Defaults to "pin".
        """
        if value is None:
            self.clear(feature)
            return

        if isinstance(feature, Feature):
            self.edits[feature] = {
                "mode": mode,
                "value": value,
            }
        else:
            for f in feature:
                self.edits[f] = {"mode": mode, "value": value}

    def clear(self, feature: Union[Feature, FeatureGroup]):
        """Remove modifications for specified feature(s).

        Args:
            feature (Union[Feature, FeatureGroup]): Feature(s) to clear modifications for
        """
        if isinstance(feature, Feature):
            del self.edits[feature]
        else:
            for f in feature:
                del self.edits[f]

    def reset(self):
        """Remove all feature modifications."""
        self.edits = FeatureEdits()

    def __repr__(self):
        return str(self)

    def __str__(self):
        edits = "{"
        for feature, edit in self.edits:
            edits += f"\n      {feature}: {edit},"
        edits += "\n   }"

        return f"Variant(\n   base_model={self.base_model},\n   edits={edits}\n)"

    def json(self):
        """Convert the variant to a JSON-compatible dictionary.

        Returns:
            dict: Dictionary containing base model and feature configurations
        """
        return {
            "base_model": self.base_model,
            "fastmodel_config": [
                {
                    "feature_id": str(feature.uuid),
                    "feature_label": feature.label,
                    "max_activation_strength": feature.max_activation_strength,
                    "index_in_sae": feature.index_in_sae,
                    "mode": edit["mode"],
                    "value": edit["value"],
                }
                for feature, edit in self.edits
            ],
        }

    @property
    def controller(self) -> Controller:
        """Get a controller instance with the variant's modifications applied.

        Returns:
            Controller: Controller instance with feature modifications
        """
        controller = Controller()

        for feature, edit in self.edits:
            value = edit["value"]
            if isinstance(value, bool):
                value = 0.5 if value else -0.3

            if edit["mode"] == "nudge":
                controller[feature] += edit["value"]
            else:
                controller[feature] = edit["value"]

        return controller
