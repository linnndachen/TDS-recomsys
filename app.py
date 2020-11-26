import os
import json
import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

from models.glove_model import glove2vec

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, abort, jsonify
from sqlalchemy import exc, create_engine
import sqlite3
import joblib

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


def recomm_engine(input, df, model):
    # vectorize the input
    vector_input = glove2vec(input, model)

    # finding cosine similarity for the vectors
    similarity = []
    for n in df['vectors']:
        scores = cosine_similarity(vector_input, n)[0][0]
        similarity.append(scores)

    df['similarity'] = similarity

    # sort and find the recommended movie
    df = df.sort_values(by=['similarity'], ascending=False)
    #res_df = df.iloc[:m]

    return df['Names']


con = sqlite3.connect("data/EAdescription.db")
df = pd.read_sql_query("SELECT * FROM EAdescription", con)

# load model
model = joblib.load("models/glove_model.pkl")


@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


# web page that handles user query and displays model results
@app.route('/reuslt')
def go():
    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file.
    return render_template(
        '/result.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
