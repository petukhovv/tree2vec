import json
import argparse

from lib.Helpers.AstReader import AstReader
from lib.FeatureExtraction.FeatureExtractor import FeatureExtractor

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', nargs=1, type=str, help='file with AST')
parser.add_argument('--output', '-o', nargs=1, type=str,
                    help='output file, which will contain features and feature values as JSON')
parser.add_argument('--is_normalize', action='store_true',
                    help='normalization necessary of vectors on the maximum value')
args = parser.parse_args()

ast_file = args.input[0]
output = args.output[0]
no_normalize = not args.is_normalize

root = AstReader.read(ast_file)

simple_features = [
    'depth',
    'depth_avg',
    'chars_length_avg',
    'chars_length_max'
]

features = [{
    'type': 'all_ngrams',
    'params': {
        'n': 3,
        'max_distance': 3,
        'no_normalize': no_normalize
    }
}]

features.extend(map(lambda feature: {'type': feature}, simple_features))

features_extractor = FeatureExtractor(root, features)
features = features_extractor.extract()

with open(output, 'w') as f:
    f.write(json.dumps(features, default=str))
