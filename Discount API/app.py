from ast import Param
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from urllib import response
import requests
import csv
import cgi

BASE = "http://allanchuang1.pythonanywhere.com/"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'meow'

class SearchForm(FlaskForm):
    entry = StringField('Entry', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/magnific-popup/<path:path>')
def send_magnific(path):
    return send_from_directory('static/magnific-popup', path)

@app.route('/slick/<path:path>')
def send_slick(path):
    return send_from_directory('static/slick', path)


@app.route("/", methods = ['GET', 'POST'])
def index():
    form = request.form.to_dict(flat = False)
    results = []
    if request.method == 'POST':
        code = form['searchform'][0]
        response = requests.get(BASE + 'course/' + code).json()
        print(response)
        results.append(response)
    

    return render_template("index.html", title="Search", form=form, results=results)


if __name__ == "__main__":
    app.run(debug=True)