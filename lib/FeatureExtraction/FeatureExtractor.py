from .Features.DepthExtractor import DepthExtractor
from .Features.CharsLengthExtractor import CharsLengthExtractor
from .Features.NGramsExtractor import NGramsNumberExtractor
from .Features.AllNGramsExtractor import AllNGramsExtractor


class FeatureExtractor:
    supported_features = {
        'depth': DepthExtractor('max'),
        'depth_avg': DepthExtractor('mean'),
        'chars_length_avg': CharsLengthExtractor('mean'),
        'chars_length_max': CharsLengthExtractor('max'),  # it's full program length if use original Kotlin AST
        'ngram': NGramsNumberExtractor(),
        'all_ngrams': AllNGramsExtractor()  # extracting all n-grams
    }

    def __init__(self, ast, features):
        self.ast = ast
        self.features = None
        self.assign_feature_extractors(features)

    def assign_feature_extractors(self, features):
        for feature in features:
            if feature['type'] not in self.supported_features:
                raise Exception('Unsupported feature')

        self.features = features

    def extract(self):
        feature_values = {}

        for feature in self.features:
            feature_name = feature['params']['name'] if 'params' in feature and 'name' in feature['params'] else feature['type']
            feature_params = feature['params'] if 'params' in feature else None
            feature_value = self.supported_features[feature['type']].extract(self.ast, feature_params)
            if isinstance(feature_value, dict):
                feature_values = {**feature_values, **feature_value}
            else:
                feature_values[feature_name] = float(feature_value)

        return feature_values
