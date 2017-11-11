from .Features.DepthExtractor import DepthExtractor
from .Features.CharsLengthExtractor import CharsLengthExtractor


class FeatureExtractor:
    supported_features = {
        'depth': DepthExtractor('max'),
        'depth_avg': DepthExtractor('mean'),
        'chars_length_avg': CharsLengthExtractor('mean'),
        'chars_length_max': CharsLengthExtractor('max')  # it's full program length if use original Kotlin AST
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

    def extract(self):
        feature_values = {}

        for feature in self.features:
            feature_values[feature] = self.supported_features[feature].extract(self.ast)

        return feature_values
