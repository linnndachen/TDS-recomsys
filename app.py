import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
#from auth import AuthError, requires_auth
#from models import db_drop_and_create_all, setup_db, Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = 'SECRET'
    #setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        return response

    # db_drop_and_create_all()

    # Home
    @app.route('/')
    def home():
        return render_template('index.html')

    return app

APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)