# Python Examples

Simple Python code examples using Python, Flask and Bootstrap.

The site is viewable here, <a href="https://flask-bootstrap.azurewebsites.net/">https://flask-bootstrap.azurewebsites.net</a>.

## Flask Quickstart

Here is a quickstart guide for installing Python Flask on Microsoft Windows. The full documentation is here, <a href="https://flask.palletsprojects.com/en/2.1.x/installation/#install-flask">https://flask.palletsprojects.com/en/2.1.x/installation/#install-flask</a>.

```
mkdir myproject
cd myproject
py -3 -m venv venv

venv\Scripts\activate

pip install Flask

$env:FLASK_APP = "app"
$env:FLASK_DEBUG = 1
python -m flask run
```

### Generate a list of packages
The command below is useful if you plan to connect your code repository to a Microsoft Azure App Service.

```
pip freeze --local > requirements.txt
```

## Public APIs
* https://github.com/public-apis/public-apis

### Random Duck API
* https://random-d.uk/api