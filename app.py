# venv\scripts\activate
# $env:FLASK_APP = "app" 
# $env:FLASK_DEBUG = 1 
# python -m flask run
#
# http://flask-bootstrap.azurewebsites.net/

import datetime

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.dates import DayLocator, DateFormatter
from io import BytesIO

import random

from flask import Flask, render_template, Response, request, redirect, url_for, json
from urllib.request import Request, urlopen
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
users = []

@app.route("/")
def home():
    return render_template('jumbotron.html')

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/email', methods=['POST'])
def email():
    return render_template('email.html', email=request.form.get('email_address'))

@app.route("/json/local")
def json_local():
    with open('data/users.json') as f:
        local_users = json.load(f)
    return render_template('json_local.html', users=local_users)

@app.route("/json/remote")
def json_remote():
    url = "https://api.github.com"
    response = urlopen(url)
    github_urls = json.loads(response.read()) 
    return render_template('json_remote.html', urls=github_urls)

@app.route('/json/users', methods=['GET'])
def json_users():

    global users

    if len(users) == 0:
        with open('data/users.json') as f:
            users = json.load(f)

    return render_template('json_users.html', users=users)

@app.route('/json/users/add', methods=['POST'])
def json_add():

    global users

    users.append({"name": request.form.get('name')})
    return redirect(url_for('json_users')) 

# Random Duck API

duck_url = "https://random-d.uk/api/v2/"

# paginate, filter and sort

@app.route("/duck")
def duck():
    
    global duck_url
 
    query = duck_url + "random"
    req = Request(query, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req)
    duck_json = json.loads(res.read()) 

    return render_template('duck/duck.html', duck=duck_json)

@app.route("/ducks")
def ducks():
    
    global duck_url
    # "image_count": 282,
    # "images": []

    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
 
    query = duck_url + "list"
    req = Request(query, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req)
    ducks_json = json.loads(res.read())

    pagination = Pagination(page=page, total=ducks_json['image_count'], search=search, record_name='ducks') 
    
    return render_template('duck/ducks.html', ducks=ducks_json['images'], url=duck_url, pagination=pagination)

# FHRS API

fhrs_url = "http://api.ratings.food.gov.uk"

@app.route("/countries")
def countries():
    
    global fhrs_url
 
    # page = 1
    # page_size = 10
    
    # Create the URL string to query the FHRS API
    # In this case, http://api.ratings.food.gov.uk/Countries/basic
    # I found the API query failed without adding, headers = {'x-api-version': 2}
    # You may want to limit the number of results you bring back from the API
    # For example, query = fhrs_url + '/Countries/basic/{}/{}'.format(page, page_size)  

    query = fhrs_url + '/Countries/basic'
    headers = {'x-api-version': 2}

    req = Request(query, headers=headers)
    res = urlopen(req)
    fhrs_json = json.loads(res.read()) 

    return render_template('countries.html', data=fhrs_json)

# Graph

@app.route("/graph")
def graph():
    str_date = datetime.datetime.now()
    return render_template('graph.html', date=str_date)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():

    dataset = "./data/NY-City-Central-Park-Historical-Temperature-Data.csv"
    # dataframe
    df = pd.read_csv(dataset)
    # Convert the date column, 18690101, to a Python datetime
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    # Locate a range of dates
    start_date = '07-01-2020'
    end_date = '08-01-2020'
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[mask]
    # Convert the min, max columns from Fahredheit to Celsius
    # (32°F − 32) × 5/9 = 0°C
    df['min'] = (df['min']-32) * 5/9
    df['max'] = (df['max']-32) * 5/9
    # Create the Figure    
    fig = Figure()
    ax = fig.subplots()
    ax.plot(df['date'], df['max'])
    #defines the tick location 
    ax.xaxis.set_major_locator(DayLocator())
    #defines the label format
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m"))
    ax.tick_params(axis="x", labelrotation= 90)

    return fig
    
