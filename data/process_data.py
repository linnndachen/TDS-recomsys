from nltk.corpus import stopwords
import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

import re
from nltk.corpus import stopwords


def load_data(data_filepath):
    df = pd.read_csv("EA_CSV.csv", engine="python", encoding="UTF-8")
    return df


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


def clean_df(df):
    # combine the description
    df['description'] = df['Expertise'].fillna(
        '') + " " + df['Title'].fillna('')
    # clean that column
    df['description'] = df['description'].apply(clean_text)
    return df


def save_data(df, database_filename):
    engine = create_engine(
        'sqlite:///' + database_filename, pool_pre_ping=True)
    df.to_sql('EAdescription', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 3:

        data_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    DATA: {}\n'
              .format(data_filepath))
        df = load_data(data_filepath)

        print('Cleaning data...')
        df = clean_df(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the EA csv file '
              'and the filepath of the database to save the cleaned data '
              'to as the second argument. \n\nExample: python process_data.py '
              'EA_CSV.csv '
              'EAdescription.db')


if __name__ == '__main__':
    main()


"""
python3 process_data.py EA_CSV.csv EAdescription.db
"""
