import pandas as pd
import numpy as np
import pickle
import pprint as pp

def cosine_similarity(a, b):
    """
    Input :
    a : a numpy array representing word a as a vector
    b : a numpy array representing word b as a vector

    Output:
    cos_ab : a scalar proportional to the similarity in angles between a and b

    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def euclidean(a, b):
    """
    Input:
    a : a numpy array representing word a as a vector
    b : a numpy array representing word b as a vector

    Output:
    d: scalar representing the Euclidean distance between a and b
    """
    return np.linalg.norm(a - b)

def get_country(city1, country1, city2, embeddings):
    """
    Input:
        city1: a string (the capital city of country1)
        country1: a string (the country of capital1)
        city2: a string (the capital city of country2)
        embeddings: a dictionary where the keys are words and values are their embeddings

    Output:
        countries: a dictionary with the most likely country and its similarity score
    """

    # Store the city1, country 1, and city 2 in a set called group
    group = {city1, country1, city2}

    # Get their embeddings
    city1_emb = embeddings.get(city1)
    country1_emb = embeddings.get(country1)
    city2_emb = embeddings.get(city2)

    # Calculate the embedding of country2 using simple linear algebra
    # Remember : king - man + woman = queen
    country2_emb = country1_emb - city1_emb + city2_emb

    # Finding the closest word embedding

    # loop through all the words in the embeddings dict, checking that it isnt in the group defined above and
    # then calculate the similarity (using whichever metric you prefer).  If the similarity is higher, then write
    # over the stored best_similarity and update country, which stores a tuple (country_name, similarity_score).
    # Finally return the country tuple.

    # Initialize the similarity to -1
    best_similarity = -1

    # Initialize the country to an empty string
    country = ''

    # Loop through all words in the embeddings dictionary
    for word, emb in embeddings.items():

        # Check if the word is not in the group
        if word not in group:

            # Compute the similarity between the embedding of the word and the embedding of country2
            similarity = cosine_similarity(emb, country2_emb)

            # If the similarity is higher than the current best similarity
            if similarity > best_similarity:
                # Update the best_similarity variable
                best_similarity = similarity

                # Update the country variable with a tuple containing the country name and the similarity score
                country = (word, best_similarity)

    # Return the country tuple
    return {'country': country[0], 'similarity_score': country[1]}


def get_accuracy(word_embeddings, data):
    '''
    Input:
        word_embeddings: a dictionary where the key is a word and the value is its embedding
        data: a pandas dataframe containing all the country and capital city pairs

    Output:
        accuracy: the accuracy of the model
    '''

    # initialize num correct to zero
    num_correct = 0

    # loop through the rows of the dataframe
    for i, row in data.iterrows():

        # get city1
        city1 = row['city1']

        # get country1
        country1 = row['country1']

        # get city2
        city2 = row['city2']

        # get country2
        country2 = row['country2']

        # use get_country to find the predicted country2
        predicted_country2 = get_country(city1, country1, city2, word_embeddings)

        # if the predicted country2 is the same as the actual country2...
        if predicted_country2.get('country') == country2:
            # increment the number of correct by 1
            num_correct += 1

    # get the number of rows in the data dataframe (length of dataframe)
    m = len(data)

    # calculate the accuracy by dividing the number correct by m
    accuracy = num_correct / m

    return accuracy




# Load pre-trained embeddings
word_embeddings = pickle.load( open( "word_embeddings_subset.p", "rb" ) )

# load data file
data = pd.read_csv('capitals.txt', delimiter=' ')
# name columns
data.columns = ['city1', 'country1', 'city2', 'country2']


# Test the cosine_similarity function 
# king = word_embeddings['king']
# queen = word_embeddings['queen']
# print(cosine_similarity(king, queen))


# Test euclidean function
# print(euclidean(king, queen))


# Test get_country function
print(get_country('Paris', 'France', 'Cairo', word_embeddings))


accuracy = get_accuracy(word_embeddings, data)
print(f"Accuracy is {accuracy:.3f}")