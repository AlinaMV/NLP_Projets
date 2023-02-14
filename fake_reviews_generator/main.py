from nltk import ngrams
from collections import defaultdict
import numpy as np


def make_trigrams(file):

    """Making a list of trigrams from a text"""

    with open(file) as f:
        text = f.read().replace('.', ' .')
        trigrams = ngrams(text.split(), 3)
        return trigrams

def make_conditional_probas(text_file):

    """ Outputs a probability table (dictionary) based on naive Bayes approach.
    Takes reviews file as an argument"""

    proba_table = defaultdict()
    trigrams = make_trigrams(text_file)

    # Constructing a count table
    for i in trigrams:
        key = i[:2]
        if proba_table.get(key) == None:
            proba_table[key] = dict()
            proba_table[key][i[2]] = 1
        elif proba_table[key].get(i[2]) == None:
            proba_table[key][i[2]] = 1
        else:
            proba_table[key][i[2]] += 1

        # Turning the count table into probability table
        for k in proba_table:
            sum_up = 0
            for subkey in proba_table[k]:
                sum_up += proba_table[k][subkey]
            for subkey in proba_table[k]:
                proba_table[k][subkey] /= sum_up

    return proba_table



def sample_from_discrete_distrib(distrib):

    """Sample a value from a discrete distribution represented by a dictionary"""

    words, probas = zip(*distrib.items())
    probas = np.asarray(probas).astype('float64')/np.sum(probas)
    return np.random.choice(words, p = probas)


def generate(proba_table):

    """Generating reviews based on the probability table
    from the make_conditional_probas function """

    # Take words "BEGIN","NOW" to start the list and continue until the word "END" is reached
    words = ["BEGIN", "NOW"]
    while True:
        # Choose a word from the probability table that can follow the two previous chosen words
        words.append(sample_from_discrete_distrib(proba_table[tuple(words[-2:])]))
        # End the review when "END" is reached
        if words[-1] == "END":
            break
    # Make a complete review of the chosen words
    review = " ".join(words)
    # Replace the space-separated period and comma tokens with normal ponctuation
    return review.replace(' .', '.').replace(' ,', ',')

probas = make_conditional_probas('wine_test.txt')

print(generate(probas))
