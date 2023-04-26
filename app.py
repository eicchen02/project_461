from flask import Flask,render_template,request, redirect, url_for, session
import subprocess
import os
from json import load
from time import sleep
from os import remove
 
app = Flask(__name__, template_folder='templates', static_folder='templates/static')

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/database/')
def database():
    return render_template('Database.html')

@app.route('/packages/')
def packages():
    return render_template('PackageList.html')

@app.route('/database/upload')
def upload():
    return render_template('interactions/Upload.html')

@app.route('/database/update/')
def update():
    return render_template('/interactions/Update.html')

@app.route('/database/rate/')
def rate():
    return render_template('interactions/Rate.html')

@app.route('/database/download/')
def download():
    return render_template('/interactions/Download.html')

if __name__ == "__main__": 
    # app.run(host='localhost', port=8080)
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))