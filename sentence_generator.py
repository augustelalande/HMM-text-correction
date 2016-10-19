from utils.data_parser import load_data

vocab, unigrams, bigrams, trigrams = load_data()


def gen_sentence():
    """Creates a randomly generated sentence according to some word distribution

    Returns:
        list: list of words representing the sentence
    """
    start = 153
    end = 152

    # initialize the sentence with the start word
    sentence = [start]
    # append a word using the bigram of the start character
    sentence.append(bigrams[start].guess())

    while sentence[-1] != end:
        # try to guess a word using the trigram of the previous two characters
        guess = trigrams[tuple(sentence[-2:])].guess()

        if guess == 0:
            # if no word was found try using the bigram
            guess = bigrams[sentence[-1]].guess()

        if guess == 0:
            # if still no word was found use the unigram
            guess = unigrams.guess()

        sentence.append(guess)

    # substitute the word indices with the real words
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
