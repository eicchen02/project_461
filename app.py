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
@app.route('/package', methods=["POST"])
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

@app.route('/package/byName/{name}', methods=["DELETE"])
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

@app.route('/package/byName/{name}', methods=["GET"])
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
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This uses the search function that we have created
@app.route('/package/byRegEx', methods=["POST"])
def PackageByRegExGet():
    # Loads and checks the data from the request.
    #! Assuming currently that this is saved in the json under the 'regex' key. May not be in actuality
    regex = json.loads(request.data)["regex"]
    if regex == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be a regular expression that can be used in the body.'}), 400, {'content_type': 'application/json'}
    
    # Otherwise, perform search function through SQL database
    #! Need to implement SQL functionality to search correctly for a RegEx expression through READMEs and names
    
    # If the package is not found, return 404 error
    #! Need to implement SQL functionality before checking.
    
    # Otherwise, return a list of all packages that match
    #! Need to implement SQL functionality beforehand. Returns should be of type PackageMetadata, which includes ID, packageName, and version
    
    # Temp return for now
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

@app.route('/package/{id}', methods=["DELETE"])
def PackageDelete(id=None):
    # First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400', 
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    # Then, check if package is within SQL database by ID
    #! Need to implement SQL functionality beforehand to search through database. Return 404 if not in database
    
    # Finally, return 200 if deleted
    return jsonify({'status_code': '200',
                    'message': 'Package is deleted'}), 200, {'content_type': 'application/json'}

@app.route('/package/{id}', methods=["GET"])
def PackageRetrieve(id=None):
    # First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    # Then, check if package exists in the SQL database
    #! Need to implement SQL functionality beforehand to search through database. Return 404 if not in database
    
    # Then, convert package into base64/obtain base64 package for PackageData type field
    #! Need to implement SQL functionality beforehand to obtain the URL/Base64 package uploaded.
    
    # Finally, return Package to user. Should follow the 'Package' Schema, which involves 'PackageData' and 'PackageMetadata'
    #! Need to implement SQL first to get data
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This will replace the current ID with a new package version (update), as long as ID, version, and name match
@app.route('/package/{id}', methods=["PUT"])
def PackageUpdate(id=None):
    # First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    # Next, obtain data from response.
    #! Assuming that the data is found in 'data'. Might be wrong and need to change
    data = json.loads(request.data)
    
    # Then, check that there is an ID, name, and version provided
    if not data["id"]:
        return jsonify({'status_code': '400',
                        'message': 'There are missing field(s) in the request body. There must be an \'id\', \'name\', and \'version\'.'}), 400, {'content_type': 'application/json'}
    elif not data["name"]:
        return jsonify({'status_code': '400',
                        'message': 'There are missing field(s) in the request body. There must be an \'id\', \'name\', and \'version\'.'}), 400, {'content_type': 'application/json'}
    elif not data["version"]:
        return jsonify({'status_code': '400',
                        'message': 'There are missing field(s) in the request body. There must be an \'id\', \'name\', and \'version\'.'}), 400, {'content_type': 'application/json'}
    
    # Then, check if id/name/version match in database. Start with id, then check name and version associated with that id
    #! Need to implement SQL functionality beforehand to search through database. Return error code 404 if it does not match

    # Update the values for the id
    #! Need to implement SQL functionality beforehand. Then, do the same as for PackageCreate does.
    
    # Finally, return 200 status code

    return jsonify({'status_code': '200',
                    'message': 'Version is updated'}), 200, {'content_type': 'application/json'}

#? This is the rating function for a package's id value
@app.route('/package/{id}/rate', methods=["GET"])
def PackageRate(id=None):
    # First, check if id is None
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be a valid ID in order to rate packages'}), 400, {'content_type': 'application/json'}
    
    # Then, obtain the scores from the SQL database
    #! Need to implement SQL functionality to obtain store values. If the package ID does not exist, return 404. If a score is -1 or failed, return 500.
    
    # Then, need to format scores according to the PackageRating definition in the YAML.
    #! Need SQL scores to do this
    
    # Finally, return 200 and PackageRating if successful
    return jsonify({'status_code': '200',
                    'message': 'Rating was successful. View the scores for the package in the \'rate\' section.',
                    'rate': 'This is a test, put values here when completed'}), 200, {'content_type': 'application/json'}

#? This is the fetch command. Need to understand it more
#! No idea how to do this currently, must examine later
@app.route('/packages', methods=["POST"])
def PackagesList():
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This is the SQL reset
#! Need a working SQL database in order to complete this
@app.route('/reset', methods=["DELETE"])
def RegistryReset():
    return jsonify({'status_code': '200',
                    'message': 'Registry is reset'}), 200, {'content_type': 'application/json'}


# Main function call to start backend/frontend
if __name__ == "__main__":
    # app.run(host='localhost', port=8080)
    application.add_api('api-spec.yaml')
    app.static_folder = ('templates/static')
    app.template_folder = ('templates')
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))