import sys

from pprint import pprint

from lib.Helpers.AstReader import AstReader
from lib.FeatureExtraction.FeatureExtractor import FeatureExtractor

if len(sys.argv) <= 1:
    sys.stderr.write('File with AST not specified.\n')
    exit()

ast_file = sys.argv[1]

root = AstReader.read(ast_file)

features_extractor = FeatureExtractor(root, ['depth'])
features = features_extractor.extract()

pprint(features)
