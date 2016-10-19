from collections import defaultdict


class Node:

    def __init__(self, word, prob, parent, level):
        self.word = word
        self.prob = prob
        self.parent = parent
        self.level = level


class SearchTree(object):

    def __init__(self):
        self.root = Node(153, 1, None, 0)
        self.levels = defaultdict(dict)
        self.levels[0][153] = self.root

    def push(self, parent, word, prob):
        level = parent.level + 1
        node = Node(word, prob, parent, level)
        if word in self.levels[level].keys():
            if prob > self.levels[level][word].prob:
                self.levels[level][word] = node
        else:
            self.levels[level][word] = node

    def level(self, level):
        for word in self.levels[level].keys():
            yield self.levels[level][word]

    def path(self, node):
        path = []
        while node != self.root:
            path.append(node.word)
            node = node.parent
        return reversed(path)
