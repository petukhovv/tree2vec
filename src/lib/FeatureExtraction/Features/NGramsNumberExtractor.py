import numpy

from pprint import pprint

class NGramsNumberExtractor:
    # Тут нужно реализовать составное условие:
    # 1) Пушить глубину рекурсии в элемент пути и сверять разницу между глубиной рекурсии, которая была на первом элементе пути и записываемом
    #       - если она больше переданной дистанции, сразу дропать этого кандидата на n-gram'у
    # 2) Сверять идентификатор пути - n узлов из n-gram'ы должны обязательно лежать на одном пути. Если не лежат - сразу дропать кандидата
    def dfs(self, nodes, matches_paths, params):
        for node in nodes:
            if node['type'] in params['node_types']:
                matches_path_index = 0
                for matches_path in matches_paths:
                    if matches_path < len(params['node_types']) and params['node_types'][matches_path] == node['type']:
                        matches_paths[matches_path_index] += 1
                    matches_path_index += 1

                if params['node_types'][0] == node['type']:
                    matches_paths.append(1)

            if 'children' in node:
                matches_paths = self.dfs(node['children'], matches_paths, params)

        return matches_paths

    def get_ngrams_number(self, ngram_candidates, params):
        return ngram_candidates.count(len(params['node_types']))

    def extract(self, ast, params):
        ngram_candidates = self.dfs(ast, [], params)
        ngrams_number = self.get_ngrams_number(ngram_candidates, params)

        return ngrams_number
