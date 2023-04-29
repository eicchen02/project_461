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
    return jsonify({'status_code': '501',
                    'message': 'This system does not support authentication'}), 501, {'content_type': 'application/json'}

#? /package path uploads a new package
def PackageCreate():
    # Grabs the global id_counter for adding packages
    global id_counter
    
    # Loads and checks the data from the request
    data = json.loads(request.data)
    if "URL" in data:
        file = data["URL"]
    elif "Content" in data:
        file = data["Content"]
    else:
        return jsonify({'status_code': '400',
                        'message': 'There is missing field(s) in the PackageData or it is formed inproperly'}), 400, {'content_type': 'application/json'}
    
    # Open the temp_file for writing the data to
    f = open("temp_file.txt", "w+")
    f.write(file)
    f.close()

    # Runs the upload function from ./run, which calculates scoring
    subprocess.run(["./run", "upload", "temp_file.txt"])
    sleep(2)
    
    # Grabs the URL and scores from the output json
    output = load(open("output/output.json"))[0]
    obtainedURL = output["URL"]
    netScore = output["NET_SCORE"]
    rampup = output["RAMP_UP_SCORE"]
    updatedCode = output["UPDATED_CODE_SCORE"]
    pinningPractice = output["PINNING_PRACTICE_SCORE"]
    correctness = output["CORRECTNESS_SCORE"]
    busFactor = output["BUS_FACTOR_SCORE"]
    responsiveness = output["RESPONSIVE_MAINTAINER_SCORE"]
    license = output["LICENSE_SCORE"]
    
    # Performs Ingestion on the package
    if (netScore < 0.5 or rampup < 0.5 or updatedCode < 0.5
        or pinningPractice < 0.5 or correctness < 0.5
        or busFactor < 0.5 or responsiveness < 0.5
        or license < 0.5):
        return jsonify({'status_code': '424',
                        'message': 'Package is not uploaded due to the disqualified rating.'}), 424, {'content_type': 'application/json'}
    
    # Remove unneeded files
    remove("output/output.json")
    remove("temp_file.txt")

    #! Still needs to check if already in database and return error code 409 if it already exists
    #! Still needs to upload to database after previous checks
    
    # Grab version number from package
    version = load(open(f'local_cloning/cloned_repos/{os.path.basename(obtainedURL)}/package.json'))["version"]

    # Form metadata return json
    metadata = {'ID': f'{id_counter}',
                'Name': f'{os.path.basename(obtainedURL)}',
                'Version': f'{version}'}
    
    # Increment id_counter
    id_counter += 1
    
    # Form data return json
    packageData = {'URL': f'{obtainedURL}'}

    # Return success
    return jsonify({'status_code': '201',
                    'message': 'Success. Check the ID in the returned metadata for the official ID.',
                    'data': f'{packageData}',
                    'metadata': f'{metadata}'}), 201, {'content_type': 'application/json'}


def PackageByNameDelete(name=None):
    # Check if a name is actually passed, and return error if not
    if name == None:
        return jsonify({'status_code': '400',
                        'message': 'Package name cannot be \'None\'.'}), 400, {'content_type': 'application/json'}
    
    # First, check if package name is in our SQL database. Return 404 if not in database
    #! Need to implement searching by name for SQL database

    # Then, use SQL commands to delete package
    #! Need to implement SQL connection to delete package
    
    # Finally, return 200 if everything is successful
    return jsonify({'status_code': '200',
                    'message': 'Package is deleted'}), 200, {'content_type': 'application/json'}

def PackageByNameGet(name=None):
    # Check if a name is actually passed, and return error if not
    if name == None:
        return jsonify({'status_code': '400',
                        'message': 'Package name cannot be \'None\'.'}), 400, {'content_type': 'application/json'}
    
    # First, check if the package name is in our SQL database. Return 404 if not in database
    #! Need to implement searching by name for SQL database
    
    # Then, use SQL commands to obtain when the package was entered into the SQL database
    #! Need to implement SQL functionality, as well as potentially uploading time of upload into table
    
    # Finally, return 200 with correct message
    #! Need to implement SQL functionality to return correct format. Almost correct format is described here:
    ''' return jsonify({'status_code': '200',
                        'message' : 'Obtained the history of the given package. Check in the \'history\' field for the data.',
                        'history' : f'{HISTORY_DATE (Example: 2023-03-23T23:11:15.000Z)}'}), 200, {'content_type': 'application/json'}
    '''
    
    # Temp return for now
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'})

def PackageByRegExGet():
    # Loads and checks the data from the request
    data = json.loads(request.data)
    

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