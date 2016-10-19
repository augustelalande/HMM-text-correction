from collections import defaultdict
from utils.prob_words import ProbWords


def load_data():
    vocab = load_vocab()
    unigrams = load_unigrams()
    bigrams = load_bigrams()
    trigrams = load_trigrams()

    return vocab, unigrams, bigrams, trigrams


def load_vocab(src="data/vocab.txt"):
    vocab = [None]

    with open(src) as f:
        for line in f:
            words = line.split()
            vocab.append(words[1])
    return vocab


def load_unigrams(src="data/unigram_counts.txt"):
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


def load_inverse_bigrams(unigrams, src="data/bigram_counts.txt"):
    inverse_bigrams = defaultdict(ProbWords)

    with open(src) as f:
        for line in f:
            words = line.split()
            key = int(words[1])
            item = int(words[0])
            log_prob = float(words[2])
            conditional = 10 ** log_prob
            A_prob = unigrams.word_prob(key)
            B_prob = unigrams.word_prob(item)
            prob = conditional * A_prob / B_prob
            inverse_bigrams[key].push(item, prob)
    return inverse_bigrams


def load_word_keys(src="data/vocab.txt"):
    word_keys = {}

    with open(src) as f:
        for line in f:
            words = line.split()
            word_keys[words[1]] = int(words[0])
    return vocab
