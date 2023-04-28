from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import subprocess
import os
from json import load
from time import sleep
from os import remove
import connexion

id_counter = 0 
application = connexion.FlaskApp(__name__, specification_dir='Rest_API_File/')
app = application.app

#! Implement RESTful API here, but first update the app.routes to be in accordance with SWAGGER

#Frontend Page navigation
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/database/')
def database():
    return render_template('Database.html')

@app.route('/database/packages/')
def packageList():
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

# Backend paths and operations

#? We have no authentication, should return 501
@app.route('/authenticate', methods=["PUT"])
def CreateAuthToken():
    return '', 501

#? /package path uploads a new package
def PackageCreate():
    data = json.loads(request.data)
    if "URL" in data:
        file = data["URL"]
    elif "Content" in data:
        file = data["Content"]
    else:
        return jsonify({'code': '400',
                        'message': 'There is missing field(s) in the PackageData or it is formed inproperly'})
    
    f = open("temp_file.txt", "w+")
    f.write(file)
    f.close()

    subprocess.run(["./run", "upload", "temp_file.txt"])
    sleep(2)
    obtainedURL = load(open("output/output.json"))[0]["URL"]
    remove("output/output.json")

    #! Still needs to check if already in database and return error code 409 if it already exists
    #! Still needs ingestion, and return error code 424 if failed
    #! Still needs to upload to database after previous checks
    
    metadata = jsonify({'ID': f'{id_counter}',
                        'Name': f'{os.path.basename(obtainedURL)}',
                        'Version': f'{load(f"local_cloning/cloned_repos/{os.path.basename(obtainedURL)}/package.json")["version"]}'})
    id_counter += 1
    
    packageData = jsonify({'URL': f'{obtainedURL}'})
    
    packageInfo = jsonify({'data': f'{packageData}',
                       'metadata': f'{metadata}'})
    return jsonify({'code': '201',
                   'message': f'{packageInfo}'})


def PackageByNameDelete():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageByNameGet():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageByRegExGet():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageDelete():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageRetrieve():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageUpdate():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageRate():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackagesList():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def RegistryReset():
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

if __name__ == "__main__": 
    # app.run(host='localhost', port=8080)
    application.add_api('api-spec.yaml')
    app.static_folder = ('templates/static')
    app.template_folder = ('templates')
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))