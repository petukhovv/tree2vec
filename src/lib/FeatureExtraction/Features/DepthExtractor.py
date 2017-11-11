import numpy


class DepthExtractor:
    metric = 'mean'

    metrics = {
        'mean': numpy.mean,
        'min': numpy.min,
        'max': numpy.max
    }

    def __init__(self, ast):
        self.ast = ast

    def __call__(self):
        return self.extract()

    def dfs(self, nodes, depths, path_number):
        if len(depths) <= path_number:
            depths.append(1)
        else:
            depths[path_number] += 1
        for node in nodes:
            if 'children' in node:
                depths = self.dfs(node['children'], depths, path_number)
            path_number += 1

        return depths

    def extract(self):
        depths = self.dfs(self.ast, [], 0)

        return self.metrics[self.metric](depths)
