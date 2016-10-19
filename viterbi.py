from math import factorial, exp
from utils.edit_distance import levenshtein
from utils.data_parser import load_vocab, load_bigrams
from utils.search_tree import SearchTree

vocab = load_vocab()
bigrams = load_bigrams()


def viterbi(observations, n=3):
    tree = SearchTree()

    for level, o in enumerate(observations):
        for node in tree.level(level):
            best_probs = [0 for _ in range(n)]
            best_words = [0 for _ in range(n)]

            for word, state_prob in bigrams[node.word].options():
                obsv_prob = observation_prob(o, vocab[word])
                prob = obsv_prob * state_prob * node.prob
                if prob > min(best_probs):
                    index = best_probs.index(min(best_probs))
                    best_probs[index] = prob
                    best_words[index] = word

            for p, w in zip(best_probs, best_words):
                tree.push(node, w, p)

    leaf_level = len(observations)
    best_leaf = Node(0, 0, None, 0)

    for node in tree.level(leaf_level):
        if node.prob > best_leaf.prob:
            best_leaf = node

    sentence = [vocab[w] for w in tree.path(best_leaf)]

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
    print_sentence(viterbi(test_sentence))

