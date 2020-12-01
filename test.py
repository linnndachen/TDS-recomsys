import os
import sys
import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

from models.glove_model import glove2vec

from sqlalchemy import exc, create_engine
import sqlite3
import joblib


def load_data(database_filepath, model_filepath):
    vec_df = pd.read_pickle(database_filepath)

    model = joblib.load(model_filepath)
    keywords = 'data collection, data ethics issues/initial assumptions'

    return vec_df, model, keywords


def clean_text(s):
    # removeNonAscii
    s = "".join(i for i in s if ord(i) < 128)

    # return all lower cases
    s = s.lower()

    # remove stop wrods
    s = s.split()
    stops = set(stopwords.words("english"))
    text = [w for w in s if not w in stops]
    text = " ".join(text)

    # remove html
    html_pattern = re.compile('<.*?>')
    text = html_pattern.sub(r'', text)

    # remove punctuation
    text = re.sub(r'[^\w\s]', " ", text)
    return text


def input_vec(input, model):
    avgword2vec = None
    count = 0
    for word in input.split():
        if word in model:
            count += 1
            if avgword2vec is None:
                avgword2vec = model[word]
            else:
                avgword2vec = avgword2vec + model[word]

    if avgword2vec is not None:
        avgword2vec = avgword2vec / count

    return avgword2vec


def recomm_engine(input_vector, vec_df, model):
    # vectorize the input
    #cleaned_input = clean_text(keywords)
    #input_vector = input_vec(cleaned_input, model)

    # finding cosine similarity for the vectors
    similarity = []
    input_vector = input_vector.reshape(1, -1)
    for n in vec_df['vectors']:
        n = n.reshape(1, -1)
        scores = cosine_similarity(input_vector, n)[0][0]
        similarity.append(scores)

    vec_df['similarity'] = similarity

    # sort and find the recommended movie
    vec_df = vec_df.sort_values(by=['similarity'], ascending=False)

    return vec_df.loc[::, :'Title']


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n')
        vec_df, model, keywords = load_data(database_filepath, model_filepath)
        print('keywords: {}'.format(keywords))
        print(vec_df['vectors'][0])

        print('Cleaning input...')
        cleaned_input = clean_text(keywords)

        print('Vectorizing the input')
        vec_input = input_vec(cleaned_input, model)
        print('Input vectorized')

        print('Finding EAs....')
        result = recomm_engine(vec_input, vec_df, model)
        print(result)

    else:
        print('Please provide the filepath of the EAdescription database '
              'as the first argument. The filepath of the pickle file to '
              'save the model the second argument and the filepath of '
              'the database to save the vectorized description as the '
              'third argument. \n\nExample: python3 glove_model.py '
              '../data/EAdescription.db glove_model.pkl '
              'vecDescription.db')


if __name__ == '__main__':
    main()

# python3 test.py models/vectors.pkl models/glove_model.pkl

#print(recomm_engine(keywords, vec_df, model))
