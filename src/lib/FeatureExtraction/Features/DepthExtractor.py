class DepthExtractor:
    def __call__(self, ast):
        self.ast = ast

        return self.extract()

    def dfs(self, nodes, depths, path_number):
        depths[path_number - 1] += 1
        for node in nodes:
            path_number += 1
            if 'children' in node:
                depths = self.dfs(node['children'], depths, path_number)

        return depths

    def extract(self):
        return self.dfs(self.ast, [0], 1)
