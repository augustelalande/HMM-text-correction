from utils.data_parser import load_data

vocab, unigrams, bigrams, trigrams = load_data()


def gen_sentence():
    sentence = [153]
    sentence.append(bigrams[153].guess())

    while sentence[-1] != 152:
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
    text = sentence[1]
    punctuation = ['.', ',', ';', ':', '!', '?']

    for word in sentence[2:-1]:
        if word not in punctuation:
            text += " "
        text += word
    print(text)

sentence = gen_sentence()
print_sentence(sentence)
