from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import subprocess
import os
from json import load
from time import sleep
from os import remove
import connexion
from sys import stderr

id_counter = 0
application = connexion.FlaskApp(__name__, specification_dir='Rest_API_File/')
app = application.app
app.secret_key = os.urandom(24)

#* Frontend Page navigation

#* These routes are used for navigation from one frontend page to another.
#* The operations (rate/upload/update/download) also have a page with
#* a form, which performs the operations on the inputted value and returns
#* another Frontend Completion Page

#? This is the homepage for the website.
@app.route('/')
def home():
    return render_template('Home.html')

#? This is the page which lists all database 
#? commands.
@app.route('/database/')
def database():
    return render_template('Database.html')

#? This is the list of packages.
#! May choose to not do this. Currently have no way of displaying all packages, so may want to ignore this
@app.route('/database/packages/')
def packageList():
    return render_template('PackageList.html')

#? This is the upload frontend page. Takes a
#? package URL and uploads to the SQL database.
@app.route('/database/upload', methods=["GET", "POST"])
def upload():
    #* If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        #* Sets the default status to be an error
        session['upload_status'] = "Error with Uploading"
        
        #* Obtaines the global id_counter var for identification
        global id_counter
        
        #* Grabs the package URL from the upload form
        package_url = request.form["upload_input"]
        print("Input package_url: "+ package_url, file = stderr)
        
        #* Checks to make sure that the input is a GitHub or NPM link
        if("github.com" not in package_url and "npmjs.com" not in package_url):
            session['upload_status_details'] = "Package is not uploaded due to an invalid URL link"
            return redirect(url_for('uploadComplete'))
        
        #* Check if the current URL already is uploaded
        #! Need SQL interaction. Return error if already in database
        
        #* Open the temp_file for writing the data to
        f = open("temp_file.txt", "w+")
        f.write(package_url)
        f.close()

        #* Runs the upload function from ./run, which calculates scoring
        subprocess.run(["./run", "upload", "temp_file.txt"])
        sleep(2)

        #* Grabs the URL and scores from the output json
        output = load(open("output/output.json"))[0]
        netScore = output["NET_SCORE"]
        rampup = output["RAMP_UP_SCORE"]
        updatedCode = output["UPDATED_CODE_SCORE"]
        pinningPractice = output["PINNING_PRACTICE_SCORE"]
        correctness = output["CORRECTNESS_SCORE"]
        busFactor = output["BUS_FACTOR_SCORE"]
        responsiveness = output["RESPONSIVE_MAINTAINER_SCORE"]
        license = output["LICENSE_SCORE"]

        #* Increment id_counter
        id_counter += 1

        #* Performs Ingestion on the package
        if (netScore < 0.5 or rampup < 0.5 or updatedCode < 0.5
            or pinningPractice < 0.5 or correctness < 0.5
            or busFactor < 0.5 or responsiveness < 0.5
            or license < 0.5):
            session['upload_status_details'] = "Package is not uploaded due to a disqualified rating.\nEvery metric must score greater than 0.5"
            return redirect(url_for('uploadComplete'))

        #* Remove unneeded files
        remove("output/output.json")
        remove("temp_file.txt")
        
        #! Then, upload to SQL database
        
        #* Return success page
        session['upload_status'] = "Package has been Uploaded"
        session['upload_status_details'] = "The given package has been uploaded to our database!"
        return redirect(url_for('uploadComplete'))
    else:
        #* Otherwise, just return the Upload page (A "GET" Operation)
        return render_template('interactions/Upload.html')

#? This is the update frontend page. Takes a URL and 
#? updates the current entry in the SQL database with 
#? most recent values.
@app.route('/database/update/', methods=["GET", "POST"])
def update():
    #* If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        #* Sets default status message to be an error
        session['update_status'] = "Error with Updating"
        
        #* Grabs the package URL from the update form
        package_url = request.form["update_input"]
        
        #* Checks to make sure that the input is a GitHub or NPM link
        if("github.com" not in package_url and "npmjs.com" not in package_url):
            session['update_status_details'] = "Package is not updated due to an invalid URL link"
            return redirect(url_for('updateComplete'))
        
        #* Search through the SQL database in order to find the corresponding URL exists already
        #! Need SQL interaction. Return error page if failed
        
        #* Open the temp_file for writing the data to
        f = open("temp_file.txt", "w+")
        f.write(package_url)
        f.close()

        #* Runs the upload function from ./run, which calculates scoring
        subprocess.run(["./run", "upload", "temp_file.txt"])
        sleep(2)

        #* Grabs the URL and scores from the output json
        output = load(open("output/output.json"))[0]
        netScore = output["NET_SCORE"]
        rampup = output["RAMP_UP_SCORE"]
        updatedCode = output["UPDATED_CODE_SCORE"]
        pinningPractice = output["PINNING_PRACTICE_SCORE"]
        correctness = output["CORRECTNESS_SCORE"]
        busFactor = output["BUS_FACTOR_SCORE"]
        responsiveness = output["RESPONSIVE_MAINTAINER_SCORE"]
        license = output["LICENSE_SCORE"]

        #* Remove unneeded files
        remove("output/output.json")
        remove("temp_file.txt")
        
        #* Update SQL database with new values
        #! Need SQL interaction. Return error page on failure
        
        #* Show success page on success
        session['update_status'] = "Package has been Updated"
        session['update_status_details'] = "The given package has been updated in our database!"
        return redirect(url_for('updateComplete'))
    else:
        #* Otherwise, just return the Update page (A "GET" Operation)
        return render_template('/interactions/Update.html')

#? This is the rate frontend page. Takes a URL and 
#? displays the ratings for such page.
@app.route('/database/rate/', methods=["GET", "POST"])
def rate():
    #* If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        #* Sets the default status to be an error
        session['rate_status'] = "Error with Rating"
        
        #* Grabs the package URL from the rate form
        package_url = request.form["rate_input"]
        
        #* Search through the SQL database in order to find the corresponding URL
        #! Need SQL interaction. Return error page if failed
        
        #* Grab all scores from the SQL database
        #! Need SQL interaction. Return error page if failed
        
        #* Return rating page that shows all scores according to the data gathered
        #TODO Change the session 'status_details' to be the values obtained from SQL database
        session['rate_status'] = "Package has been Rated"
        session['rate_status_details'] = "Here are the values for the given package!"
        return redirect(url_for('rateComplete'))
    else:
        #* Otherwise, just return the Rate page (A "GET" Operation)
        return render_template('interactions/Rate.html')

#? This is the download frontend page. Takes a URL 
#? and downloads a local copy for the user.
@app.route('/database/download/', methods=["GET", "POST"])
def download():
    #* If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        #* Sets the default status to be an error
        session['download_status'] = "Error with Downloading"
        
        #* Grabs the package URL from the download form
        package_url = request.form["download_input"]
        
        #* Search through the SQL database in order to find the corresponding URL
        #! Need SQL interaction. Return error page if failed
        
        #* Grab the base64 package associated from the SQL database
        #! Need SQL interaction. Return error page if failed
        
        #* Use this format to send the file back -> return send_file(io.BytesIO(FILE_DATA))
        #! Need SQL interaction. Return error page if failed
        
        #* Show success page on success
        session['download_status'] = "Package has been Downloaded"
        session['download_status_details'] = "The given package has been downloaded from our database!"
        return redirect(url_for('downloadComplete'))
    else:
        #* Otherwise, just return the Download page (A "GET" Operation)
        return render_template('/interactions/Download.html')

#* Frontend Completion Pages:

#* These Pages are used to show results or to inform the user of a success/fail for
#* all operations through the frontend website.

#? The page for displaying completion/errors for uploads.
@app.route('/database/upload/complete', methods=["GET"])
def uploadComplete():
    #* Returns the upload completion page, for both errors and success
    return render_template('interactions/complete/UploadComplete.html',
                           status_message=session['upload_status'],
                           status_message_details=session['upload_status_details'])

#? The page for displaying completion/errors for updates.
@app.route('/database/update/complete', methods=["GET"])
def updateComplete():
    #* Returns the update completion page, for both errors and success
    return render_template('interactions/complete/UpdateComplete.html', 
                           status_message=session['update_status'],
                           status_message_details=session['update_status_details'])

#? The page for displaying completion/errors for ratings.
@app.route('/database/rate/complete', methods=["GET"])
def rateComplete():
    return render_template('interactions/complete/RateComplete.html',
                           status_message=session['rate_status'],
                           status_message_details=session['rate_status_details'])

#? The page for displaying completion/errors for downloads.
@app.route('/database/download/complete', methods=["GET"])
def downloadComplete():
    return render_template('interactions/complete/DownloadComplete.html',
                           status_message=session['download_status'],
                           status_message_details=session['download_status_details'])


#* Backend Paths and Operations:

#* These routes are used to handle all REST API calls and operations.
#* Some of these routes are similar to the Frontend Page Operations,
#* but most operate differently and return JSON responses back to the
#* user.

#? We have no authentication, should return 501
#TODO May have to include tokens anyways? Maybe not users, but potentially tokens for operations. May not be baseline though.
@app.route('/authenticate', methods=["PUT"])
def CreateAuthToken():
    return jsonify({'status_code': '501',
                    'message': 'This system does not support authentication'}), 501, {'content_type': 'application/json'}

#? Uploads a new package to our database. This operates similarly to
#? the "Upload" Frontend Page Operation.
@app.route('/package', methods=["POST"])
def PackageCreate():
    #* Grabs the global id_counter for adding packages
    global id_counter
    
    #* Loads and checks the data from the request
    data = json.loads(request.data)
    if "URL" in data:
        file = data["URL"]
    elif "Content" in data:
        file = data["Content"]
    else:
        return jsonify({'status_code': '400',
                        'message': 'There is missing field(s) in the PackageData or it is formed inproperly'}), 400, {'content_type': 'application/json'}
    
    #* Open the temp_file for writing the data to
    f = open("temp_file.txt", "w+")
    f.write(file)
    f.close()

    #* Runs the upload function from ./run, which calculates scoring
    subprocess.run(["./run", "upload", "temp_file.txt"])
    sleep(2)
    
    #* Grabs the URL and scores from the output json
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
    
    #* Increment id_counter
    id_counter += 1
    
    #* Performs Ingestion on the package
    if (netScore < 0.5 or rampup < 0.5 or updatedCode < 0.5
        or pinningPractice < 0.5 or correctness < 0.5
        or busFactor < 0.5 or responsiveness < 0.5
        or license < 0.5):
        return jsonify({'status_code': '424',
                        'message': 'Package is not uploaded due to the disqualified rating.'}), 424, {'content_type': 'application/json'}
    
    #* Remove unneeded files
    remove("output/output.json")
    remove("temp_file.txt")

    #! Still needs to check if already in database and return error code 409 if it already exists (DO THIS HERE)
    #! Still needs to upload to database after previous checks (DO THIS HERE)
    
    #* Grab version number from package
    version = load(open(f'local_cloning/cloned_repos/{os.path.basename(obtainedURL)}/package.json'))["version"]

    #* Form metadata return json
    metadata = {'ID': f'{id_counter}',
                'Name': f'{os.path.basename(obtainedURL)}',
                'Version': f'{version}'}
    
    #* Form data return json
    #TODO Should return base64 package, instead of URL
    packageData = {'URL': f'{obtainedURL}'}

    #* Return success
    return jsonify({'status_code': '201',
                    'message': 'Success. Check the ID in the returned metadata for the official ID.',
                    'data': f'{packageData}',
                    'metadata': f'{metadata}'}), 201, {'content_type': 'application/json'}


#? This will delete packages from SQL database 
#? by the name provided.
#! Needs SQL interaction
@app.route('/package/byName/{name}', methods=["DELETE"])
def PackageByNameDelete(name=None):
    #* Check if a name is actually passed, and return error if not
    if name == None:
        return jsonify({'status_code': '400',
                        'message': 'Package name cannot be \'None\'.'}), 400, {'content_type': 'application/json'}
    
    #* First, check if package name is in our SQL database. Return 404 if not in database
    #! Need to implement searching by name for SQL database

    #* Then, use SQL commands to delete package
    #! Need to implement SQL connection to delete package
    
    #* Finally, return 200 if everything is successful
    return jsonify({'status_code': '200',
                    'message': 'Package is deleted'}), 200, {'content_type': 'application/json'}

#? This will obtain the most recent change to the 
#? package (date of last modification).
#! Needs SQL interaction, as well as additional table entry for 'time last modified'
@app.route('/package/byName/{name}', methods=["GET"])
def PackageByNameGet(name=None):
    #* Check if a name is actually passed, and return error if not
    if name == None:
        return jsonify({'status_code': '400',
                        'message': 'Package name cannot be \'None\'.'}), 400, {'content_type': 'application/json'}
    
    #* First, check if the package name is in our SQL database. Return 404 if not in database
    #! Need to implement searching by name for SQL database
    
    #* Then, use SQL commands to obtain when the package was entered into the SQL database
    #! Need to implement SQL functionality, as well as potentially uploading time of upload into table
    
    #* Finally, return 200 with correct message
    #! Need to implement SQL functionality to return correct format. Almost correct format is described here:
    ''' return jsonify({'status_code': '200',
                        'message' : 'Obtained the history of the given package. Check in the \'history\' field for the data.',
                        'history' : f'{HISTORY_DATE (Example: 2023-03-23T23:11:15.000Z)}'}), 200, {'content_type': 'application/json'}
    '''
    
    #* Temp return for now
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This uses the search function that we have created to search
#? for a list of Package types.
#! Needs SQL interaction
@app.route('/package/byRegEx', methods=["POST"])
def PackageByRegExGet():
    #* Loads and checks the data from the request.
    #TODO Assuming currently that this is saved in the json under the 'regex' key. May not be in actuality
    regex = json.loads(request.data)["regex"]
    if regex == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be a regular expression that can be used in the body.'}), 400, {'content_type': 'application/json'}
    
    #* Otherwise, perform search function through SQL database
    #! Need to implement SQL functionality to search correctly for a RegEx expression through READMEs and names
    
    #* If the package is not found, return 404 error
    #! Need to implement SQL functionality before checking.
    
    #* Otherwise, return a list of all packages that match
    #! Need to implement SQL functionality beforehand. Returns should be of type PackageMetadata, which includes ID, packageName, and version
    
    #* Temp return for now
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This deletes packages based on the id provided.
#! Needs SQL interaction
@app.route('/package/{id}', methods=["DELETE"])
def PackageDelete(id=None):
    #* First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400', 
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    #* Then, check if package is within SQL database by ID
    #! Need to implement SQL functionality beforehand to search through database. Return 404 if not in database
    
    #* Then, delete package from SQL database
    #! Need to implement SQL functionality beforehand to interact with database.
    
    #* Finally, return 200 if deleted
    return jsonify({'status_code': '200',
                    'message': 'Package is deleted'}), 200, {'content_type': 'application/json'}

#? This retrieves a base64 package from the database. This 
#? operates similarly to the 'Download" Frontend Page Operation.
#! Needs SQL interaction
@app.route('/package/{id}', methods=["GET"])
def PackageRetrieve(id=None):
    #* First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    #* Then, check if package exists in the SQL database
    #! Need to implement SQL functionality beforehand to search through database. Return 404 if not in database
    
    #* Then, convert package into base64/obtain base64 package for PackageData type field
    #! Need to implement SQL functionality beforehand to obtain the URL/Base64 package uploaded.
    
    #* Finally, return Package to user. Should follow the 'Package' Schema, which involves 'PackageData' and 'PackageMetadata'
    #! Need to implement SQL first to get data
    
    #* Temp return for now
    return jsonify({'code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This will replace the current ID with a new package 
#? version (update), as long as ID, version, and name match.
#! Needs SQL interaction
@app.route('/package/{id}', methods=["PUT"])
def PackageUpdate(id=None):
    #* First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    #* Next, obtain data from response.
    #TODO Assuming that the data is found in 'data'. Might be wrong and need to change
    data = json.loads(request.data)
    
    #* Then, check that there is an ID, name, and version provided
    if not data["id"]:
        return jsonify({'status_code': '400',
                        'message': 'There are missing field(s) in the request body. There must be an \'id\', \'name\', and \'version\'.'}), 400, {'content_type': 'application/json'}
    elif not data["name"]:
        return jsonify({'status_code': '400',
                        'message': 'There are missing field(s) in the request body. There must be an \'id\', \'name\', and \'version\'.'}), 400, {'content_type': 'application/json'}
    elif not data["version"]:
        return jsonify({'status_code': '400',
                        'message': 'There are missing field(s) in the request body. There must be an \'id\', \'name\', and \'version\'.'}), 400, {'content_type': 'application/json'}
    
    #* Then, check if id/name/version match in database. Start with id, then check name and version associated with that id
    #! Need to implement SQL functionality beforehand to search through database. Return error code 404 if it does not match

    #* Update the values for the id
    #! Need to implement SQL functionality beforehand. Then, do the same as for PackageCreate does.
    
    #* Finally, return 200 status code

    return jsonify({'status_code': '200',
                    'message': 'Version is updated'}), 200, {'content_type': 'application/json'}

#? This is the rating function for a package's id value. This
#? operates similarly to the "Rate" Frontend Page Operation.
#! Needs SQL interaction
@app.route('/package/{id}/rate', methods=["GET"])
def PackageRate(id=None):
    #* First, check if id is None
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be a valid ID in order to rate packages'}), 400, {'content_type': 'application/json'}
    
    #* Then, obtain the scores from the SQL database
    #! Need to implement SQL functionality to obtain store values. If the package ID does not exist, return 404. If a score is -1 or failed, return 500.
    
    #* Then, need to format scores according to the PackageRating definition in the YAML.
    #! Need SQL scores to do this
    
    #* Finally, return 200 and PackageRating if successful
    return jsonify({'status_code': '200',
                    'message': 'Rating was successful. View the scores for the package in the \'rate\' section.',
                    'rate': 'This is a test, put values here when completed'}), 200, {'content_type': 'application/json'}

#? This is the fetch command. Need to understand it more
#? before implementing it.
#! No idea how to do this currently, must examine later
@app.route('/packages', methods=["POST"])
def PackagesList():
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This is the SQL reset. Resets the SQL database to a 
#? default state.
#! Need a working SQL database in order to complete this
@app.route('/reset', methods=["DELETE"])
def RegistryReset():
    return jsonify({'status_code': '200',
                    'message': 'Registry is reset'}), 200, {'content_type': 'application/json'}


#* Main function call to start backend/frontend
if __name__ == "__main__":
    application.add_api('api-spec.yaml')
    app.static_folder = ('templates/static')
    app.template_folder = ('templates')
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))

