import sys
import os
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def load_data(database_filepath):
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('EAdescription', engine)
    return df


def glove_model(file_path='glove.twitter.27B.200d.txt'):
    """
    input: the access to the file which contains the pre-trained glove model
    ouput: a trained model using glove
    """

    model = {}
    f = open(file_path, encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        model[word] = coefs
    f.close()
    return model


def glove2vec(df, model):
    # Creating a list for storing the vectors (description into vectors)
    global word_embeddings
    word_embeddings = []

    avgword2vec = None
    count = 0
    for text in df['description']:
        for word in text.split():
            if word in model:
                count += 1
                if avgword2vec is None:
                    avgword2vec = model[word]
                else:
                    avgword2vec = avgword2vec + model[word]

        if avgword2vec is not None:
            avgword2vec = avgword2vec / count

        word_embeddings.append(avgword2vec)

    # drop an EA if that EA has "None" vector
    df['vectors'] = word_embeddings
    for i, n in enumerate(df['vectors']):
        if n[0] is None:
            df = df.drop([i+1], axis=0)

    return df


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, "wb"))

def save_data(df, database_filename):
    engine = create_engine(
        'sqlite:///' + database_filename, pool_pre_ping=True)
    df.to_sql('EAvectors', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '
              'as the first argument and the filepath of the pickle file to '
              'save the model to as the second argument. \n\nExample: python '
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
