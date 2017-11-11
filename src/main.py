import sys

from lib.Helpers.AstReader import AstReader
from lib.FeatureExtraction.FeatureExtractor import FeatureExtractor

if len(sys.argv) <= 1:
    sys.stderr.write('File with AST not specified.\n')
    exit()

ast_file = sys.argv[1]

root = AstReader.read(ast_file)

features = FeatureExtractor(root)
