# TDS-recomsys

## Project Description:

This project aims to optimize the process for finding the most suited editorial associates in the shortest period of time. An NLP recommendation engine was thus built. After the editor type in the keywords of an article, the web app will rank all the editorial associates by their relevancy, comparing to the keywords that the editor provided. For more details, please see [this](https://medium.com/@linnndachen/finding-a-reviewer-d0fd1a1572c2) Medium blog post.

## File Structures

```
├── auth
│   └── auth.py
├── data
│   └── process_data.py
├── models
│   └── glove_model.py
├── static
│   ├── css 
│   ├── fonts
│   ├── tds_icon.ico
│   ├── img
│   └── js
└── templates
│   ├── home.html
│   └── result.html
├── Procfile
├── README.md
├── app.py
├── nltk.txt
├── recomm_local.ipynb
├── requirements.txt
└── test.py
```

Files Highlight:

- ```data/process_data.py``` is the file to clean data.

- ```models/glove_model.py``` is the file to produce the pre-trained word vectors and to turn wrods into vectos. 


- The web frontend is located in ```templates/```, which builds static assets deployed to the web server at ```static/```.


- ```recomm_local.ipynb```is the juypter notebook to make sure all the codes work.


- ```Procfile``` and ```nltk.txt``` are files for Heroku deployment


## Getting Started

### Installing Dependencies

#### Python 3.7 and Flask

Follow instructions to install the latest version of [Python](https://docs.python.org/3/using/) and [Flask](https://flask.palletsprojects.com/en/1.0.x/installation/#install-flask) for your platform.

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Initialize and activate a virtualenv:

```
$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by

```pip install -r requirements.txt```

This will install all of the required packages we selected within the requirements.txt file.

### Get it running

1. Download files and rename columns

```
- download the most updated EA file from Google drive in CSV format.

- rename it to: EA_CSV.csv

- rename "Current Title on LinkedIn" to "Title" and "Expertise(s)" to "Expertise"
```

If the column names have completed change by the time you are using this project. Please use the Jupyter notebook ```recomm_local.ipynb``` to play with it first.

2. Process Data

```
$ cd YOUR_PROJECT_DIRECTORY_PATH/data
$ python3 process_data.py EA_CSV.csv EAdescription.db
```

3. go to https://nlp.stanford.edu/projects/glove/ and download the ```glove.twitter.27B.zip```. Upzip the file and save it to YOUR_PROJECT_DIRECTORY_PATH/models

4. Train the model

```
$ cd YOUR_PROJECT_DIRECTORY_PATH/models
$ python3 glove_model.py ../data/EAdescription.db glove_model.pkl
```

This step takes ~10 mins

5. Run the development server

```
$ export FLASK_APP=myapp
$ export FLASK_ENV=development # enables debug mode
$ python3 app.py
```

6. Navigate to Home page http://0.0.0.0:8080/

It takes ~5 min to get the web running.

## Results

Before, the editors need to go through an excel sheet like below to find the most suited EA

![](static/img/results/before.png)


Now, they can go to a web page like below and type in the keywords with space.

![](static/img/results/result_1.png)


For example, if we type in keywords "data ethics". The web page will render what we searched for and the first EA is the one that's most recommended.

![](static/img/results/result_2.png)


For more details on model performance and future improvement, please read the Medium [blog post](https://linnndachen.medium.com/finding-a-reviewer-d0fd1a1572c2). 

## Author and Acknowledgement

Linda Chen is the author of this project.

All rights reserved.
