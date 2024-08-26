from collections import defaultdict
from itertools import combinations
import json



class ArgumentRelationOutput:
    def __init__(self):
        pass
    
    def find_all_paths(self, graph, start, end, path=None):
        """
        Finds all paths from start to end in a given graph.

        Args:
            graph (dict): Adjacency list representing the graph.
            start (str): Starting node.
            end (str): Ending node.
            path (list, optional): Current path. Defaults to None.

        Returns:
            list: List of paths from start to end.
        """
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def construct_tree(self, sentences, relations):
        """
        Constructs a tree from sentences and relations.

        Args:
            sentences (list): List of sentences.
            relations (list): List of tuples (parent, child, relation_type).

        Returns:
            dict: A tree structure where keys are parents and values are lists of (child, relation_type) tuples.
        """
        graph = defaultdict(list)
        for parent, child, relation_type in relations:
            graph[parent].append(child)
        
        all_paths = {}
        for start, end in combinations(sentences, 2):
            paths = self.find_all_paths(graph, start, end)
            if paths:
                all_paths[(start, end)] = paths
        
        used_relations = set()
        for paths in all_paths.values():
            for path in paths:
                for i in range(len(path) - 1):
                    used_relations.add((path[i], path[i + 1]))

        tree = defaultdict(list)
        for parent, child, relation_type in relations:
            if (parent, child) in used_relations:
                tree[parent].append((child, relation_type))

        # Remove indirect paths
        for start, end in all_paths:
            if len(all_paths[(start, end)]) > 1:
                for i in range(len(all_paths[(start, end)]) - 1):
                    path1 = all_paths[(start, end)][i]
                    path2 = all_paths[(start, end)][i + 1]
                    min_length = min(len(path1), len(path2))
                    for j in range(min_length):
                        parent = path1[j]
                        child = path2[j]
                        if (parent, child) in tree[start]:
                            tree[start].remove((child, tree[start][0][1]))  # Assumes the relation type is uniform for each parent-child pair

        return dict(tree)

    def get_paths(self, tree, start, end, path=None):
        """
        Retrieves all paths from start to end in a given tree.

        Args:
            tree (dict): Tree structure where keys are nodes and values are lists of (child, relation_type) tuples.
            start (str): Starting node.
            end (str): Ending node.
            path (list, optional): Current path. Defaults to None.

        Returns:
            list: List of paths from start to end.
        """
        if path is None:
            path = []
        path.append(start)
        if start == end:
            return [path]
        if start not in tree:
            return []
        paths = []
        for child, relation_type in tree[start]:
            if child not in path:
                newpaths = self.get_paths(tree, child, end, path[:])
                for newpath in newpaths:
                    newpath.append(relation_type)
                    paths.append(newpath)
        return paths

    def format(self, sentences, relations, remove_indirect_edges=True):
        """
        Formats the argument relations based on the provided sentences and relations.

        Args:
            sentences (list): List of sentences.
            relations (list): List of tuples (parent, child, relation_type).
            remove_indirect_edges (bool, optional): Whether to remove indirect edges. Defaults to True.

        Returns:
            dict: A dictionary with formatted argument relations.
        """
        argument_relations = {}
        if remove_indirect_edges:
            tree = self.construct_tree(sentences, relations)
            all_paths = []
            for i in range(len(sentences) - 1):
                start = sentences[i]
                end = sentences[i + 1]
                paths = self.get_paths(tree, start, end)
                all_paths.extend(paths)
            for path in all_paths:
                if path:
                    argument_relations[path[0]] = path[1:]
        else:
            # Create a dictionary with all relations without removing indirect edges
            for parent, child, relation_type in relations:
                if parent not in argument_relations:
                    argument_relations[parent] = []
                argument_relations[parent].append((child, relation_type))
        return argument_relations




class TurninatorOutput:
    @staticmethod
    def format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span,dialog=False, aif={}, x_aif={}):
        aif['nodes'] = nodes
        aif['edges'] =  edges
        aif['locutions'] =  locutions
        aif['schemefulfillments'] = schemefulfillments
        aif['descriptorfulfillments'] = descriptorfulfillments
        aif['participants'] =  participants
        x_aif['AIF'] = aif
        x_aif['ova'] =  OVA
        x_aif['dialog'] =  dialog
        x_aif['text'] =  {'txt': text_with_span}
        return json.loads(json.dumps(x_aif))