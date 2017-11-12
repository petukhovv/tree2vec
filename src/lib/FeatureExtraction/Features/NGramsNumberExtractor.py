import numpy

from pprint import pprint


class NGramsNumberExtractor:
    def dfs(self, nodes, matches_paths, params, depth):
        ngram_length = len(params['node_types'])
        new_node = {
            'length': 1,
            'depth': depth
        }

        for node in nodes:
            matches_candidates = matches_paths['candidates']
            if node['type'] in params['node_types']:
                for matches_path in matches_paths['candidates']:
                    depth_diff = depth - matches_path['depth']

                    if matches_path in matches_candidates and depth_diff <= 0:
                        matches_candidates.remove(matches_path)

                    if matches_path in matches_candidates\
                            and matches_path['length'] < ngram_length\
                            and params['node_types'][matches_path['length']] == node['type']\
                            and depth_diff <= params['max_distance']:

                        if matches_path['length'] + 1 == ngram_length:
                            matches_candidates.remove(matches_path)
                            matches_paths['found_matches'] += 1
                        else:
                            matches_path['length'] += 1
                            matches_path['depth'] = depth

                matches_paths['candidates'] = matches_candidates

                if 'children' in node and params['node_types'][0] == node['type']:
                    for node_child in node['children']:
                        if params['node_types'][1] == node_child['type']:
                            matches_paths['candidates'].append(new_node)

            if 'children' in node:
                matches_paths = self.dfs(node['children'], matches_paths, params, depth + 1)

        return matches_paths

    def extract(self, ast, params):
        ngram_candidates = self.dfs(ast, {'candidates': [], 'found_matches': 0}, params, 0)

        return ngram_candidates['found_matches']
