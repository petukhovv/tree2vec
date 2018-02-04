from copy import copy


class AllNGramsExtractor:
    NONE_TYPE = 'NONE'
    NGRAMS_NAME_SPLIT_SYMBOL = ':'

    def ngrams_recurrent_build(self, n, params, ngrams_on_path, node_type):
        """
        Recurrent n-grams building: append of current node type to n-grams of previous nodes
            (according to max distance).

        :param n: n in n-gram (n-gram order)
        :param ngrams_on_path: temporary n-gram list for nodes, which are on the current path
        :param node_type: current node type

        :return: appendant 'n-grams on path' list
        """
        grams_on_path = []
        i = 0

        for ngrams in reversed(ngrams_on_path):
            if params['max_distance'] is not None and i >= params['max_distance']:
                continue
            if len(ngrams) < n:
                continue
            for gram in ngrams[n - 1]:
                gram_appendant = copy(gram)
                gram_appendant.append(node_type)
                grams_on_path.append(gram_appendant)
            i += 1

        return grams_on_path

    def dfw(self, node, params, ngrams, depth=1):
        """
        Depth-first walk in specified AST

        :param node: current node
        :param ngrams: object with n-gram arrays (temporary 'on_path' and finally 'all')
        :param depth: recursive depth

        :return: new object with n-gram arrays (temporary 'on_path' and finally 'all')
        """
        n_bound = min(params['n'], depth)
        ngrams_on_path_for_current = [None] * n_bound
        node_type = node['type'] if 'type' in node else self.NONE_TYPE
        i = 1
        while i < n_bound:
            ngrams_on_path_for_current[i] = self.ngrams_recurrent_build(i, params, ngrams['on_path'], node_type)
            i += 1

        ngrams_on_path_for_current[0] = [[node_type]]
        ngrams['on_path'].append(ngrams_on_path_for_current)
        ngrams['all'].append(ngrams_on_path_for_current)

        if 'children' in node:
            for child_node in node['children']:
                ngrams = self.dfw(child_node, params, ngrams, depth + 1)
                ngrams['on_path'].pop()

        ngrams['nodes_number'] += 1

        return ngrams

    def normalize(self, ngrams, ngrams_statistic):
        """
        Normalize n-grams number by n-grams statistic

        :param ngrams: n-grams map (e.g. 'gram1:gram2:gram3': 0.25)
        :param ngrams_statistic: array with n-grams occurrences number (e.g. [2,4,6])

        :return: normalized n-grams map
        """
        for ngram in ngrams:
            n = len(ngram.split(self.NGRAMS_NAME_SPLIT_SYMBOL))
            ngrams[ngram] /= ngrams_statistic[n - 1]

        return ngrams

    def is_gram_contain(self, gram, subgrams):
        def sublist_exists(list1, list2):
            return ''.join(map(str, list2)) in ''.join(map(str, list1))

        is_gram_contain = False
        for subgram in subgrams:
            if sublist_exists(gram, subgram):
                is_gram_contain = True

        return is_gram_contain

    def group(self, ngrams, params):
        """
        N-grams grouping, excluding and calculating statistic (n-grams occurrences number)

        :param ngrams: multidimensional array with n-grams
        :param params: all n-grams number extractor params

        :return: grouped n-grams (n-grams map, e.g. {'gram1:gram2:gram3': 0.25, 'gram1': 0.5})
        """
        ngram_grouped = {}
        ngram_statistic = [0] * params['n']
        is_exclude_strict_specified = 'exclude_strict' in params and isinstance(params['exclude_strict'], list)
        is_include_strict_specified = 'include_strict' in params and isinstance(params['include_strict'], list)\
                                      and len(params['include_strict']) != 0
        is_exclude_specified = 'exclude' in params and isinstance(params['exclude'], list)
        is_include_specified = 'include' in params and isinstance(params['include'], list)\
                               and len(params['include']) != 0

        for grams_by_n in ngrams:
            for grams in grams_by_n:
                for gram in grams:
                    if is_exclude_strict_specified and gram in params['exclude_strict']:
                        continue
                    if is_include_strict_specified and gram not in params['include_strict']:
                        continue
                    if is_exclude_specified and self.is_gram_contain(gram, params['exclude']):
                        continue
                    if is_include_specified and not self.is_gram_contain(gram, params['include']):
                        continue
                    ngram_name = self.NGRAMS_NAME_SPLIT_SYMBOL.join(gram)
                    ngram_statistic[len(gram) - 1] += 1
                    if ngram_name in ngram_grouped:
                        ngram_grouped[ngram_name] += 1
                    else:
                        ngram_grouped[ngram_name] = 1

        return {
            'grouped': ngram_grouped,
            'statistic': ngram_statistic
        }

    def extract(self, ast, params):
        ngrams = self.dfw(ast[0], params, {'all': [], 'on_path': [], 'nodes_number': 0})
        ngrams_info = self.group(ngrams['all'], params)
        ngrams_final = self.normalize(ngrams_info['grouped'], ngrams_info['statistic']) if not params['no_normalize']\
            else ngrams_info['grouped']

        return ngrams_final
