from utils.data_parser import load_data

vocab, unigrams, bigrams, trigrams = load_data()


def gen_sentence():
    """Creates a randomly generated sentence according to some word distribution

    Returns:
        list: list of words representing the sentence
    """
    start = 153
    end = 152

    sentence = [start]
    sentence.append(bigrams[start].guess())

    while sentence[-1] != end:
        guess = trigrams[tuple(sentence[-2:])].guess()

        if guess == 0:
            print('a')
            guess = bigrams[sentence[-1]].guess()

        if guess == 0:
            print('b')
            guess = unigrams.guess()

        sentence.append(guess)

    word_sentence = [vocab[i] for i in sentence]
    return word_sentence


def print_sentence(sentence):
    """Pretty print sentence list

    Args:
        sentence (list): list of words to print
    """
    text = sentence[1]
    punctuation = ['.', ',', ';', ':', '!', '?']

    for word in sentence[2:-1]:
        if word not in punctuation:
            text += " "
        text += word
    print(text)

if __name__ == "__main__":
    sentence = gen_sentence()
    print_sentence(sentence)
