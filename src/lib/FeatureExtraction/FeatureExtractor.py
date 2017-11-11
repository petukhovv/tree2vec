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

    def extract(self):
        feature_values = {}

        for feature in self.features:
            feature_values[feature] = self.features[feature](self.ast)

        return feature_values
