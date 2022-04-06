from flask import Flask, render_template, request, json
from urllib.request import Request, urlopen
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
update_users = []

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
        users = json.load(f)
    return render_template('json_local.html', users=users)

@app.route("/json/remote")
def json_remote():
    url = "https://api.github.com"
    response = urlopen(url)
    github_urls = json.loads(response.read()) 
    return render_template('json_remote.html', urls=github_urls)

@app.route('/json/add', methods=['POST'])
def json_add():

    global update_users

    if len(update_users) == 0:
        with open('data/users.json') as f:
            update_users = json.load(f)
    
    update_users.append({"name": request.form.get('name')})
    return render_template('json_add.html', users=update_users)

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