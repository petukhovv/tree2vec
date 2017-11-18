import numpy


class CharsLengthExtractor:
    metrics = {
        'mean': numpy.mean,
        'min': numpy.min,
        'max': numpy.max
    }

    def __init__(self, metric):
        self.metric = metric

    def dfw(self, nodes, lengths):
        for node in nodes:
            lengths.append(len(node['chars']))
            if 'children' in node:
                lengths = self.dfw(node['children'], lengths)

        return lengths

    def extract(self, ast, params):
        lengths = self.dfw(ast, [])

        return self.metrics[self.metric](lengths)
