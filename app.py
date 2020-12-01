import os
import json
import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

from models.glove_model import glove2vec
from data.process_data import clean_text

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, abort, jsonify
from sqlalchemy import exc, create_engine
import sqlite3
import joblib


def create_app(test_config=None):
    app = Flask(__name__)
    # create and configure the app
    app.secret_key = 'SECRET'
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        return response

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

    def recomm_engine(string, vec_df, model):
        # vectorize the input
        cleaned_input = clean_text(string)
        input_vector = input_vec(cleaned_input, model)

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

    vec_df = pd.read_pickle("models/vectors.pkl")
    model = joblib.load("models/glove_model.pkl")

    @app.route('/')
    @app.route('/index', methods=['GET'])
    def index():
        show_df = vec_df.loc[::, :'Title']
        return render_template('/index.html',  tables=[show_df.to_html()], titles=show_df.columns.values)

    # web page that handles user query and displays model results

    @app.route('/result', methods=['GET'])
    def go():
        # save user input in query
        query = request.args.get('query', '')

        # use model to predict classification for query
        recomm_orders = recomm_engine(query, vec_df, model)

        # This will render the go.html Please see that file.
        return render_template('/index.html',  tables=[recomm_orders.to_html()], titles=recomm_orders.columns.values)

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=3001, debug=True)
