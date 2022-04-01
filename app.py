from flask import Flask, render_template, request, json
from urllib.request import urlopen

# https://data.police.uk/api/forces

# paginate, filter and sort

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