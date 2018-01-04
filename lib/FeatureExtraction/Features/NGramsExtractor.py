import copy


class NGramsNumberExtractor:
    def matches_paths_correct(self, matches_paths, node, params, depth):
        """
        Check and correct matches path depending on allowed node types and distances

        :param matches_paths: Matches paths object (with candidates and found properties = n-grams number)
        :param node: Node, for which creating paths branching point
        :param params: N-gram number extractor params
        :param depth: Recursive depth

        :return: Corrected matches paths object
        """
        ngram_length = len(params['node_types'])
        matches_path_mutable = copy.deepcopy(matches_paths)

        for matches_path in matches_paths['candidates']:
            depth_diff = depth - matches_path['depth']

            if matches_path in matches_path_mutable['candidates'] and depth_diff <= 0:
                matches_path_mutable['candidates'].remove(matches_path)

            if matches_path in matches_path_mutable['candidates'] \
                    and matches_path['length'] < ngram_length \
                    and params['node_types'][matches_path['length']] == node['type'] \
                    and depth_diff <= params['max_distance']:

                if matches_path['length'] + 1 == ngram_length:
                    matches_path_mutable['candidates'].remove(matches_path)
                    matches_path_mutable['found'] += 1
                else:
                    matches_path_index = matches_path_mutable['candidates'].index(matches_path)
                    matches_path_mutable['candidates'][matches_path_index]['length'] += 1
                    matches_path_mutable['candidates'][matches_path_index]['depth'] = depth

        return matches_path_mutable

    def paths_branching_point_create(self, matches_paths, node, params, depth):
        """
        Create paths candidates for specified node (depending on children node types)

        :param matches_paths: Matches paths object (with candidates and found properties = n-grams number)
        :param node: Node, for which creating paths branching point
        :param params: N-gram number extractor params
        :param depth: Recursive depth

        :return: Matches paths object with created paths candidates
        """
        if 'children' in node and params['node_types'][0] == node['type']:
            for node_child in node['children']:
                if params['node_types'][1] == node_child['type']:
                    new_path = {'length': 1, 'depth': depth}
                    matches_paths['candidates'].append(new_path)

        return matches_paths

    def dfw(self, nodes, matches_paths, params, depth):
        """
        Depth-first walk in specified AST

        :param nodes: AST or sub-AST
        :param matches_paths: Matches paths object (with candidates and found properties = n-grams number)
        :param params: N-gram number extractor params
        :param depth: Recursive depth

        :return:
        """
        for node in nodes:
            # Unigrams
            if len(params['node_types']) == 1 and node['type'] == params['node_types'][0]:
                matches_paths['found'] += 1
            # N-grams (N > 1)
            elif node['type'] in params['node_types']:
                matches_paths = self.matches_paths_correct(matches_paths, node, params, depth)
                matches_paths = self.paths_branching_point_create(matches_paths, node, params, depth)

            if 'children' in node:
                matches_paths = self.dfw(node['children'], matches_paths, params, depth=depth + 1)

            matches_paths['nodes_number'] += 1

        return matches_paths

    def normalize(self, ngrams_number, nodes_number, params):
        """
        Normalize n-grams found by number of AST nodes

        :param ngrams_number: N-grams found number
        :param nodes_number: AST nodes number
        :param params: N-gram number extractor params

        :return: Normalized n-grams value
        """
        return float(ngrams_number) / (nodes_number - len(params['node_types']))

    def extract(self, ast, params):
        """
        Run n-grams extractor

        :param ast: AST
        :param params: N-gram number extractor params

        :return: N-grams number
        """
        matches_paths = {'candidates': [], 'found': 0, 'nodes_number': 0}
        matches_paths = self.dfw(ast, matches_paths, params, depth=0)
        ngrams_number = self.normalize(matches_paths['found'], matches_paths['nodes_number'], params)

        return ngrams_number
