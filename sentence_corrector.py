from math import factorial, exp
from utils.edit_distance import levenshtein
from utils.data_parser import load_vocab, load_bigrams
from utils.search_tree import SearchTree, Node

vocab = load_vocab()
bigrams = load_bigrams()


def correct_sentence(observations, n=3):
    """Implementation of the Viterbi algorithm to correct mistakes in a sentence

    The algorithm works by generating a search tree and appending to it
    the nodes with the highest probability at each place in the sentence.
    It keeps track of the n children node with the highest probability
    for each parent node in the tree.

    The maximum number of nodes is therefore sentence_length ^ n. But
    some nodes can be discarded for having a lower probability than an
    other node representing the same word on the same level.

    Args:
        observations (str): String of possibly incorrect observed words
        n (int, optional): The number of children node to keep for each node in
                           the search tree.

    Returns:
        list: list of words describing a corrected sentence
    """
    observations = observations.split()
    tree = SearchTree()

    for level, o in enumerate(observations):
        for node in tree.level(level):
            # keep track of the best n words to expand the tree
            best_probs = [0 for _ in range(n)]
            best_words = [0 for _ in range(n)]

            for word, state_prob in bigrams[node.word].options():
                obsv_prob = observation_prob(o, vocab[word])
                prob = obsv_prob * state_prob * node.prob
                if prob > min(best_probs):
                    index = best_probs.index(min(best_probs))
                    best_probs[index] = prob
                    best_words[index] = word

            # push the best nodes onto their parent
            for w, p in zip(best_words, best_probs):
                if w == 0:
                    continue
                tree.push(node, w, p)

    leaf_level = len(observations)
    # initialize best leaf with a dummy node with probability 0
    best_leaf = Node(0, 0, None, 0)

    # find best leaf
    for node in tree.level(leaf_level):
        if node.prob > best_leaf.prob:
            best_leaf = node

    sentence = [vocab[w] for w in tree.path(best_leaf)]
    return sentence


def print_tree(tree, observations, max_depth=4):
    """Pretty print search tree

    Args:
        tree (SearchTree): tree to print
        observations (list): list of observed words
        max_depth (int, optional): depth to which to print the tree
    """
    for i in range(1, max_depth):
        for node in tree.level(i):
            print("level:", i)
            print("parent:", vocab[node.parent.word])
            print("word:", vocab[node.word])
            ldist = levenshtein(observations[i - 1], vocab[node.word])
            print("Levenshtein Distance:", ldist)
            bi_prob = bigrams[node.parent.word].word_prob(node.word)
            obsv_prob = observation_prob(observations[i - 1], vocab[node.word])
            interp_prob = bi_prob * obsv_prob
            print("Interpretation Prob:", "{:.3}".format(interp_prob))
            print("Cumulative Prob:", "{:.3}".format(node.prob))
            print()


def observation_prob(obsv, hidden, lam=0.01):
    """Calculate observation probability given a hidden word

    Args:
        obsv (str): observed word
        hidden (str): possible hidden word
        lam (float, optional): lambda parameter describing the expected
                               number of mistakes made per word

    Returns:
        float: probability of observation given hidden state
    """
    k = levenshtein(obsv, hidden)
    return lam ** k * exp(-lam) / factorial(k)


def print_sentence(sentence):
    """Pretty prints generated sentences

    Args:
        sentence (list): list of words representing the sentence
    """
    text = ""

    for word in sentence:
        text += " "
        text += word
    print(text)

if __name__ == "__main__":
    test_sentences = ["I think hat twelve thousand pounds",
                      "she haf heard them",
                      "She was ulreedy quit live",
                      "John Knightly wasn't hard at work",
                      "he said nit word by"]

    for test_sentence in test_sentences:
        print(test_sentence + " -->")
        corrected_sentence = " ".join(correct_sentence(test_sentence))
        print(corrected_sentence)
        ldist = levenshtein(test_sentence, corrected_sentence)
        print("Levenshtein Distance:", ldist)
        print()
