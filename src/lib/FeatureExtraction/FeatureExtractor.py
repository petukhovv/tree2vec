import json

from .Features import DepthExtractor


class FeatureExtractor:
    supported_features = {
        'depth': DepthExtractor
    }

    def __init__(self, ast, features):
        self.ast = ast
        self.features = None
        self.assign_feature_extractors(features)

    def assign_feature_extractors(self, features):
        for feature in features:
            if feature not in self.supported_features:
                raise Exception('Unsupported feature')

        self.features = features
