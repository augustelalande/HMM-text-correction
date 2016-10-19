from math import factorial, exp
from utils.edit_distance import levenshtein
from utils.data_parser import *
from utils.search_tree import *

from time import clock


vocab = load_vocab()
unigrams = load_unigrams()
bigrams = load_bigrams()
# inverse_bigrams = load_inverse_bigrams(unigrams)


# def viterbi(observations):
#     end = 152
#     max_prob = 0
#     optimal_sequence = []

#     for word, _ in unigrams.options():
#         sequence, sequence_prob = _viterbi_rec(observations, word)
#         if sequence_prob > max_prob:
#             max_prob = sequence_prob
#             optimal_sequence = sequence + [word]

#     sentence = [vocab[i] for i in optimal_sequence]
#     return sentence


# def _viterbi_rec(observations, prev):
#     obsv_prob = observation_prob(observations[-1], vocab[prev])

#     if obsv_prob < 0.004:
#         return [], 0
#     elif len(observations) == 1:
#         return [], obsv_prob * bigrams[153].word_prob(prev)

#     max_prob = 0
#     optimal_sequence = []

#     print(vocab[prev])

#     for word, _ in inverse_bigrams[prev].options():
#         state_prob = bigrams[word].word_prob(prev)
#         sequence, sequence_prob = _viterbi_rec(observations[:-1], word)
#         prob = obsv_prob * state_prob * sequence_prob
#         if prob > max_prob:
#             max_prob = prob
#             optimal_sequence = sequence + [word]

#     print(optimal_sequence)
#     return optimal_sequence, max_prob


# def viterbi(observations):
#     previous = 153
#     sequence = []
#     sequence_prob = 1

#     for o in observations:
#         max_prob = 0
#         best_word = 0

#         for word, state_prob in bigrams[previous].options():
#             obsv_prob = observation_prob(o, vocab[word])
#             prob = obsv_prob * state_prob * sequence_prob
#             if word == 10367 or word == 10640:
#                 print(word, state_prob, obsv_prob, sequence_prob, prob, max_prob)
#             if prob > max_prob:
#                 max_prob = prob
#                 best_word = word

#         previous = best_word
#         sequence_prob *= max_prob
#         sequence.append(best_word)

#     sentence = [vocab[i] for i in sequence]
#     return sentence

def viterbi(observations, n=3):
    tree = SearchTree()

    for level, o in enumerate(observations):
        for node in tree.level(level):
            best_probs = [0 for _ in range(n)]
            best_words = [0 for _ in range(n)]

            for word, state_prob in bigrams[node.word].options():
                obsv_prob = observation_prob(o, vocab[word])
                prob = obsv_prob * state_prob * node.prob
                # if word == 10361 or word == 10356:
                #     print(vocab[word], obsv_prob, state_prob, prob, node.prob)
                if prob > min(best_probs):
                    index = best_probs.index(min(best_probs))
                    best_probs[index] = prob
                    best_words[index] = word

            for p, w in zip(best_probs, best_words):
                tree.push(node, w, p)

    leaf_level = len(observations)
    best_leaf = Node(0, 0, None, 0)

    for node in tree.level(leaf_level):
        # print(vocab[node.word], node.prob, vocab[node.parent.word], node.parent.prob)
        if node.prob > best_leaf.prob:
            best_leaf = node

    sentence = [vocab[w] for w in tree.path(best_leaf)]

    # for node in tree.level(3):
    #     print(vocab[node.word], node.prob)

    return sentence


def observation_prob(obsv, hidden, lam=0.1):
    k = levenshtein(obsv, hidden)
    return lam ** k * exp(-lam) / factorial(k)


def print_sentence(sentence):
    text = ""

    for word in sentence:
        text += " "
        text += word
    print(text)

test_sentences = ["I think hat twelve thousand pounds",
                  "she haf heard them",
                  "She was ulreedy quit live",
                  "John Knightly wasn’t hard at work",
                  "he said nit word by"]

for test_sentence in test_sentences:
    test_sentence = test_sentence.split()
    # print(test_sentence)
    t = clock()
    print_sentence(viterbi(test_sentence))
    # print(clock() - t)
