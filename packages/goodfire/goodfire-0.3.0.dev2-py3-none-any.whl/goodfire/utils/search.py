from itertools import combinations

from ..features.features import FeatureGroup


class FeatureSearch:
    def __init__(self, feature_group: FeatureGroup):
        self.feature_group = feature_group

    def grid(self, k_features_per_combo: int = 2):
        """Perform a grid search over all possible combinations of features"""

        # Get all possible combinations of features
        return combinations(self.feature_group, k_features_per_combo)
