"""Methods for loading word probabilities from files
"""
from collections import defaultdict
from utils.prob_words import ProbWords


def load_data():
    """Summary

    Returns:
        TYPE: Description
    """
    vocab = load_vocab()
    unigrams = load_unigrams()
    bigrams = load_bigrams()
    trigrams = load_trigrams()

    return vocab, unigrams, bigrams, trigrams


def load_vocab(src="data/vocab.txt"):
    """Create a list matching text words to indices

    Args:
        src (str, optional): path to vocab file

    Returns:
        list: words indexed according to source file
    """
    vocab = [None]

    with open(src) as f:
        for line in f:
            words = line.split()
            vocab.append(words[1])
    return vocab


def load_unigrams(src="data/unigram_counts.txt"):
    """Create a probabilitic word generator

    Args:
        src (str, optional): path to unigrams file

    Returns:
        ProbWords: random word generator
    """
    unigrams = ProbWords()

    with open(src) as f:
        for line in f:
            words = line.split()
            item = int(words[0])
            log_prob = float(words[1])
            prob = 10 ** log_prob
            unigrams.push(item, prob)
    return unigrams


def load_bigrams(src="data/bigram_counts.txt"):
    """Create a dictionary of probabilitic word generator

    index into the dictionary using the index of the word
    preceding the desired word.

    Args:
        src (str, optional): path to bigrams file

    Returns:
        dict: dictionary of random word generators
    """
    bigrams = defaultdict(ProbWords)

    with open(src) as f:
        for line in f:
            words = line.split()
            key = int(words[0])
            item = int(words[1])
            log_prob = float(words[2])
            prob = 10 ** log_prob
            bigrams[key].push(item, prob)
    return bigrams


def load_trigrams(src="data/trigram_counts.txt"):
    """Create a dictionary of probabilitic word generator

    index into the dictionary using the tuple of the indices of
    the two words preceding the desired word.
    key = (i - 2, i - 1)

    Args:
        src (str, optional): path to trigrams file

    Returns:
        TYPE: dictionary of random word generators
    """
    trigrams = defaultdict(ProbWords)

    with open(src) as f:
        for line in f:
            words = line.split()
            key = (int(words[0]), int(words[1]))
            item = int(words[2])
            log_prob = float(words[3])
            prob = 10 ** log_prob
            trigrams[key].push(item, prob)
    return trigrams
