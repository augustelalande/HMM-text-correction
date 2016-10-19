"""Probabilistic word generator class
"""
from random import random
from bisect import bisect, bisect_left


class ProbWords(object):
    """Class to generate random non-uniformly distirbuted words.

    Attributes:
        cummulative_prob (list): cummulative probabilty up to a certain index
        items (list): list of word indices indexed at the same place as their
                      probabilities and cummulative probabilities
        prob (list): probabilities of each item
    """
    def __init__(self):
        self.items = [0]
        self.prob = [0]
        self.cummulative_prob = [0]

    def push(self, item, prob):
        """Append a word to the generator

        Args:
            item (int): word index
            prob (float): word probability
        """
        self.items.append(item)
        self.prob.append(prob)
        self.cummulative_prob.append(self.cummulative_prob[-1] + prob)

    def guess(self):
        """Generate a random word according to their given distribution

        Returns:
            int: word index
        """
        if len(self.items) == 1:
            return 0
        guess = random() * self.cummulative_prob[-1]
        index = bisect(self.cummulative_prob, guess)
        return self.items[index]

    def options(self):
        """Iterate over the words stored in this generator

        Yields:
            tuple(int, float): word index and its probability
        """
        for i in range(1, len(self.items)):
            yield self.items[i], self.prob[i]

    def word_prob(self, item):
        """Find the probability of a particular word

        if the word is not in the list of words then a
        probability of 0 is returned

        Args:
            item (int): word index

        Returns:
            float: probability of word
        """
        index = bisect_left(self.items, item)
        if index == len(self.items) or self.items[index] != item:
            return 0
        return self.prob[index]
