from random import random
from bisect import bisect, bisect_left


class ProbWords(object):

    def __init__(self):
        self.items = [0]
        self.prob = [0]
        self.cummulative_prob = [0]

    def is_empty(self):
        if len(self.items) > 1:
            return False
        return True

    def push(self, item, prob):
        self.items.append(item)
        self.prob.append(prob)
        self.cummulative_prob.append(self.cummulative_prob[-1] + prob)

    def guess(self):
        if len(self.items) == 1:
            return 0
        guess = random() * self.cummulative_prob[-1]
        index = bisect(self.cummulative_prob, guess)
        return self.items[index]

    def options(self):
        for i in range(1, len(self.items)):
            yield self.items[i], self.prob[i]

    def word_prob(self, item):
        index = bisect_left(self.items, item)
        if index == len(self.items) or self.items[index] != item:
            return 0
        return self.prob[index]
