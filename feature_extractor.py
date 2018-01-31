import json

from .lib.Helpers.AstReader import AstReader
from .lib.FeatureExtraction.FeatureExtractor import FeatureExtractor


def feature_extractor(ast_file, features, output):
    root = AstReader.read(ast_file)
    features_extractor = FeatureExtractor(root, features)
    features_extracted = features_extractor.extract()

    with open(output, 'w') as f:
        f.write(json.dumps(features_extracted, default=str))
