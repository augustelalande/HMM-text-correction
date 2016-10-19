"""Tree structure for searching the states of a sentence
"""
from collections import defaultdict


class Node:

    def __init__(self, word, prob, parent, level):
        """Stores the information of nodes generated by the SearchTree class

        Args:
            word (int): word index
            prob (float): word probability
            parent (Node): parent node
            level (int): node level on tree
        """
        self.word = word
        self.prob = prob
        self.parent = parent
        self.level = level


class SearchTree(object):
    """Tree structure for storing the nodes generated by viterbi's algorithm

    Attributes:
        levels (dict): Dictionary storing dictionary of the nodes at each level
        root (Node): root node
    """
    def __init__(self):
        self.root = Node(153, 1, None, 0)
        self.levels = defaultdict(dict)
        self.levels[0][153] = self.root

    def push(self, parent, word, prob):
        """create a new node on the tree

        Args:
            parent (Node): parent node
            word (int): word index
            prob (float): word prob
        """
        level = parent.level + 1
        node = Node(word, prob, parent, level)
        if word in self.levels[level].keys():
            # if a node already exists but with a lower probability
            # replace with the new node since only the higher probability one
            # can possibly lead to the optimal solution
            if prob > self.levels[level][word].prob:
                self.levels[level][word] = node
        else:
            self.levels[level][word] = node

    def level(self, level):
        """Iterates over the nodes on a particular level of the tree

        Args:
            level (int): Tree level over which to iterate

        Yields:
            Node: nodes at level
        """
        for word in self.levels[level].keys():
            yield self.levels[level][word]

    def path(self, node):
        """Finds the set of words from a node to the root

        Args:
            node (Node): node from which to start the path

        Returns:
            list: list of word indices to the root
        """
        path = []
        while node != self.root:
            path.append(node.word)
            node = node.parent
        return reversed(path)
