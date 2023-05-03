from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import connexion
import json
import subprocess
import os
from input.toEncodedPackage import createEncodedFile
from sql.search import *
from json import load
from time import sleep
from os import remove
from sys import stderr
from sql.sql_header import *

application = connexion.FlaskApp(__name__, specification_dir='Rest_API_File/')
app = application.app
app.secret_key = os.urandom(24)

# Frontend Page navigation

# These routes are used for navigation from one frontend page to another.
# The operations (rate/upload/update/download) also have a page with
# a form, which performs the operations on the inputted value and returns
# another Frontend Completion Page

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
    # If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        
        # Sets the default status to be an error
        session['upload_status'] = "Error with Uploading"
        
        # Grabs the package URL from the upload form
        package_url = request.form["upload_input"]
        print("Input package_url: "+ package_url, file = stderr)
        
        # Checks to make sure that the input is a GitHub or NPM link
        if("github.com" not in package_url and "npmjs.com" not in package_url):
            session['upload_status_details'] = "Package is not uploaded due to an invalid URL link"
            return redirect(url_for('uploadComplete'))
        
        # Check if the current URL already is uploaded
        # Return error if already in database
        exist = exists(table.c.PackageLink, package_url)
        if exist is True:
            session['upload_status_details'] = "Package is already uploaded, try updating instead!"
            return redirect(url_for('uploadComplete'))
            
        # Open the temp_link for writing the data to
        f = open("temp_link.txt", "w+")
        f.write(package_url)
        f.close()

        # Runs the upload function from ./run, which calculates scoring
        subprocess.run(["./run", "upload", "temp_link.txt"])
        sleep(0.1)

        # Grabs the URL and scores from the output json
        output = load(open("output/output.json"))[0]

        # Performs Ingestion on the package (enabled)
        for score in output.values():
            if type(score) == float and score < 0.5:
                session['upload_status_details'] = "Package is not uploaded due to a disqualified rating.\nEvery metric must score greater than 0.5"
                return redirect(url_for('uploadComplete'))

        # Upload to SQL database
        subprocess.run(["python3", "sql/upload.py"])

        # Then, remove unneeded files
        remove("output/output.json")
        remove("temp_link.txt")
        
        # Return success page
        session['upload_status'] = "Package has been Uploaded"
        session['upload_status_details'] = "The given package has been uploaded to our database!"
        return redirect(url_for('uploadComplete'))
    else:
        # Otherwise, just return the Upload page (A "GET" Operation)
        return render_template('interactions/Upload.html')

#? This is the update frontend page. Takes a URL and 
#? updates the current entry in the SQL database with 
#? most recent values.
@app.route('/database/update/', methods=["GET", "POST"])
def update():
    # If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        
        # Sets default status message to be an error
        session['update_status'] = "Error with Updating"
        
        # Grabs the package URL from the update form
        package_url = request.form["update_input"]
        
        # Checks to make sure that the input is a GitHub or NPM link
        if("github.com" not in package_url and "npmjs.com" not in package_url):
            session['update_status_details'] = "Package is not updated due to an invalid URL link"
            return redirect(url_for('updateComplete'))
        
        # Search through the SQL database in order to find the corresponding URL exists already
        # Return error page if failed
        exist = exists(table.c.PackageLink, package_url)

        if exist is False:
            session['update_status_details'] = "Package doesn't exist, try uploading instead!"
            return redirect(url_for('updateComplete'))
        
        # Open the temp_link for writing the data to
        f = open("temp_link.txt", "w+")
        f.write(package_url)
        f.close()

        # Runs the upload function from ./run, which calculates scoring
        subprocess.run(["./run", "upload", "temp_link.txt"])
        sleep(0.1)

        # Grabs the URL and scores from the output json
        output = load(open("output/output.json"))[0]
        
        # Update SQL database with new values
        subprocess.run(["python3", "sql/upload.py"])

        # Remove unneeded files
        remove("output/output.json")
        remove("temp_link.txt")
        
        # Show success page on success
        session['update_status'] = "Package has been Updated"
        session['update_status_details'] = "The given package has been updated in our database!"
        return redirect(url_for('updateComplete'))
    else:
        # Otherwise, just return the Update page (A "GET" Operation)
        return render_template('/interactions/Update.html')

#? This is the rate frontend page. Takes a URL and 
#? displays the ratings for such page.
@app.route('/database/rate/', methods=["GET", "POST"])
def rate():
    # If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):
        
        # Sets the default status to be an error
        session['rate_status'] = "Error with Rating"
        
        # Grabs the package URL from the rate form
        package_url = request.form["rate_input"]
        
        # Search through the SQL database in order to find the corresponding URL
        exist = exists(table.c.PackageLink, package_url)

        if exist is False:
            session['rate_status'] = "No such package exists!"
            return redirect(url_for('rateComplete'))
        
        # Grab all scores from the SQL database
        columns =  ["PackageName", "PackageLink", "Responsiveness", "UpdatedCode", "Correctness", "BusFactor", "RampUp", "Licensing", "Pinning", "NetScore"]
        query = db.select(table).where(table.c.PackageLink == package_url)
        result = connection.execute(query).fetchall()
        print(table.columns.keys())
        # Return rating page that shows all scores according to the data gathered
        session['rate_status'] = f'Results for {result[0][0]}:'
        session['rate_status_details'] = f'Net Score: {result[0][8]}, Bus Factor: {result[0][5]}, Ramp Up: {result[0][6]},\n Pinning Practice: {result[0][10]}, Responsiveness: {result[0][2]}, Pull Requests: {result[0][3]}\n, Correctness: {result[0][4]}, Licensing: {result[0][7]}'
        return redirect(url_for('rateComplete'))
    else:
        # Otherwise, just return the Rate page (A "GET" Operation)
        return render_template('interactions/Rate.html')

#? This is the download frontend page. Takes a URL 
#? and downloads a local copy for the user.
@app.route('/database/download/', methods=["GET", "POST"])
def download():
    # If the submit button is pressed (A "POST" Operation)
    if (request.method == "POST"):

        # Sets the default status to be an error
        session['download_status'] = "Error with Downloading"
        
        # Grabs the package URL from the download form
        package_url = request.form["download_input"]
        
        # Search through the SQL database in order to find the corresponding URL
        exist = exists(table.c.PackageLink, package_url)
        if exist is False:
            session['download_status_details'] = "No such package exists!"
            return redirect(url_for('downloadComplete'))
        
        # Create the Base64 package, and return the package. Can be changed to be .zip instead if needed
        zipPackage, encodedPackage = createEncodedFile(package_url)
        return send_file(f'{zipPackage}', as_attachment=True)
    else:
        # First, delete all previous .zip and Base64 files
        if os.path.exists('local_cloning/encoded_repos'):
            for f in os.listdir('local_cloning/encoded_repos'):
                os.remove(os.path.join('local_cloning/encoded_repos', f))
        
        # Otherwise, just return the Download page (A "GET" Operation)
        return render_template('/interactions/Download.html')

# Frontend Completion Pages:

# These Pages are used to show results or to inform the user of a success/fail for
# all operations through the frontend website.

#? The page for displaying completion/errors for uploads.
@app.route('/database/upload/complete', methods=["GET"])
def uploadComplete():
    # Returns the upload completion page, for both errors and success
    return render_template('interactions/complete/UploadComplete.html',
                           status_message=session['upload_status'],
                           status_message_details=session['upload_status_details'])

#? The page for displaying completion/errors for updates.
@app.route('/database/update/complete', methods=["GET"])
def updateComplete():
    # Returns the update completion page, for both errors and success
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


# Backend Paths and Operations:

# These routes are used to handle all REST API calls and operations.
# Some of these routes are similar to the Frontend Page Operations,
# but most operate differently and return JSON responses back to the
# user.

#? We have no authentication, should return 501
@app.route('/authenticate', methods=["PUT"])
def CreateAuthToken():
    return jsonify({'status_code': '501',
                    'message': 'This system does not support authentication'}), 501, {'content_type': 'application/json'}

#? Uploads a new package to our database. This operates similarly to
#? the "Upload" Frontend Page Operation.
@app.route('/package', methods=["POST"])
def PackageCreate():   
    
    # Loads and checks the data from the request
    #!logs input
    data = json.loads(request.data)
    print("Autograder input: {}".format(data), file = stderr)

    if "URL" in data and data["URL"] != None:
        file = data["URL"]
    elif "Content" in data and data["Content"] != None:
        file = data["Content"]
    else:
        return jsonify({'status_code': '400',
                        'message': 'There is missing field(s) in the PackageData or it is formed inproperly'}), 400, {'content_type': 'application/json'}
    
    # Open the temp_link for writing the data to
    f = open("temp_link.txt", "w+")
    f.write(file)
    f.close()

    # Runs the upload function from ./run, which calculates scoring
    subprocess.run(["./run", "upload", "temp_link.txt"])
    sleep(0.1)
    
    # Grabs the URL and scores from the output json
    output = load(open("output/output.json"))[0]
    obtainedURL = output["URL"]

    # Checks if the url is already in the SQL database
    exist = exists(table.c.PackageLink, obtainedURL)
    if exist is True:
       return jsonify({'status_code': '409',
                        'message': 'Package exists already.'}), 409, {'content_type': 'application/json'}
            
    # Performs Ingestion on the package (enabled)
    for score in output.values():
        if type(score) == float and score < 0.5:
            session['upload_status_details'] = "Package is not uploaded due to a disqualified rating.\nEvery metric must score greater than 0.5"
            return jsonify({'status_code': '424','message': 'Package is not uploaded due to the disqualified rating.'}), 424, {'content_type': 'application/json'}

    # Upload to SQL database
    subprocess.run(["python3", "sql/upload.py"])

    # Then, remove unneeded files from local directories
    remove("output/output.json")
    remove("temp_link.txt")

    # Grab version number from package.json. Returns error 404 if it does not exist
    try:
        version = load(open(f'local_cloning/cloned_repos/{os.path.basename(obtainedURL)}/package.json'))["version"]
    except:
        return jsonify({'status_code': '404',
                        'message': 'The provided package does not have a valid \'package.json\''}), 404, {'content_type': 'application/json'}

    #Get ID from SQL database
    query = db.select(table.c.ID).where(table.c.PackageLink == obtainedURL)
    return_id = connection.execute(query).scalar()
    
    # Form the metadata return field
    metadata = {'ID': f'{return_id}',
                'Name': f'{os.path.basename(obtainedURL)}',
                'Version': f'{version}'}
    
    # Form the data return field. Contains the Base64 package and URL
    zipPackageName, base64PackageName = createEncodedFile(obtainedURL)
    with open(base64PackageName, 'rb') as encodedPackage:
        packageData = {'Content': f'{encodedPackage.read()}',
                       'URL': f'{obtainedURL}'}

    # Return success
    return jsonify({'status_code': '201',
                    'message': 'Success. Check the ID in the returned metadata for the official ID.',
                    'data': packageData,
                    'metadata': metadata}), 201, {'content_type': 'application/json'}

#? This uses the search function that we have created to search
#? for a list of Package types.
@app.route('/package/byRegEx', methods=["GET"])
def PackageByRegExGet():

    #!logs input
    data = json.loads(request.data)
    print("Autograder input: {}".format(data), file = stderr)
    
    # Loads and checks the data from the request.
    #TODO Assuming currently that this is saved in the json under the 'regex' key. May not be in actuality
    regex = data["regex"]
    if regex == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be a regular expression that can be used in the body.'}), 400, {'content_type': 'application/json'}
    
    # Otherwise, perform search function through SQL database
    packageMatches = []
    t = sqlalchemy.text("SELECT * FROM Packages")
    result = connection.execute(t)
    
    # Do something with the results
    for row in result:
        if checkInput(row[0],  regex) or checkInput(row[1],  regex) or checkInput(row[9], regex):
            packageMatches.append({'Name': row[0], 'ID': row[11], 'Version': row[13]})
            
    # If the package is not found, return 404 error
    if not packageMatches:
        return jsonify({'status_code': '404',
                        'message': 'No package found under this regex'}), 404, {'content_type': 'application/json'}
    
    # Otherwise, return a list of all packages that match
    return jsonify({'status_code': '200',
                    'message': 'Attached is the list of packages. Check the \'data\' field for the list',
                    'data': packageMatches}), 200, {'content_type': 'application/json'}


#? This will delete packages from SQL database 
#? by the name provided.
@app.route('/package/byName/<name>', methods=["DELETE"])
def PackageByNameDelete(name=None):
    # Check if a name is actually passed, and return error if not
    if name == None:
        return jsonify({'status_code': '400',
                        'message': 'Package name cannot be \'None\'.'}), 400, {'content_type': 'application/json'}
    
    # First, check if package name is in our SQL database. Return 404 if not in database
    exist = exists(table.c.PackageName, name)
    if exist is False:
       return jsonify({'status_code': '404',
                        'message': 'Package doesn\'t exist 7.'}), 404, {'content_type': 'application/json'}

    # Then, use SQL commands to delete package
    query = db.delete(table).where(table.c.PackageName == name)
    connection.execute(query)
    connection.commit()
    
    # Finally, return 200 if everything is successful
    return jsonify({'status_code': '200',
                    'message': 'Package is deleted'}), 200, {'content_type': 'application/json'}

#? This will obtain the most recent change to the 
#? package (date of last modification).
@app.route('/package/byName/<name>', methods=["GET"])
def PackageByNameGet(name=None):
    # Check if a name is actually passed, and return error if not
    if name == None:
        return jsonify({'status_code': '400',
                        'message': 'Package name cannot be \'None\'.'}), 400, {'content_type': 'application/json'}
    
    # First, check if the package name is in our SQL database. Return 404 if not in database
    exist = exists(table.c.PackageName, name)
    if exist is False:
       return jsonify({'status_code': '404',
                        'message': 'Package doesn\'t exist 8.'}), 404, {'content_type': 'application/json'}
    
    # Then, use SQL commands to obtain when the package was entered into the SQL database
    query = db.select(table.c.LastModified).where(table.c.PackageName == name)
    history_date = connection.execute(query).scalar()
    
    # Finally, return 200 with correct message
    return jsonify({'status_code': '200',
                    'message' : 'Obtained the history of the given package. Check in the \'history\' field for the data.',
                    'history' : f'{history_date}'}), 200, {'content_type': 'application/json'}


#? This deletes packages based on the id provided.
@app.route('/package/<id>', methods=["DELETE"])
def PackageDelete(id=None):
    
    # First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400', 
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    # Then, check if package is within SQL database by ID
    exist = exists(table.c.ID, id)
    if exist is False:
       return jsonify({'status_code': '404',
                        'message': 'Package doesn\'t exist 1.'}), 404, {'content_type': 'application/json'}
    
    # Then, delete package from SQL database
    query = db.delete(table).where(table.c.ID == id)
    connection.execute(query)
    connection.commit()
    
    # Finally, return 200 if deleted
    return jsonify({'status_code': '200',
                    'message': 'Package is deleted'}), 200, {'content_type': 'application/json'}

#? This retrieves a base64 package from the database. This 
#? operates similarly to the 'Download" Frontend Page Operation.
@app.route('/package/<id>', methods=["GET"])
def PackageRetrieve(id=None):
    
    # First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    # Then, check if package exists in the SQL database
    exist = exists(table.c.ID, id)
    if exist is False:
       return jsonify({'status_code': '404',
                        'message': 'Package doesn\'t exist 2.'}), 404, {'content_type': 'application/json'}
    
    # Obtain the URL from the database
    query = db.select(table.c["PackageName", "Version", "PackageLink"]).where(table.c.ID == id)
    result = connection.execute(query).fetchone()
    
    # Then, convert package into base64/obtain base64 package for PackageData type field
    zipPackagePath, base64PackagePath = createEncodedFile(result[2])
    with open(base64PackagePath, 'rb') as data:
        packageData = {'URL': f'{result[2]}',
                       'Content': f'{data.read()}'}
    packageMetadata = {'ID': f'{id}',
                       'Name': f'{result[0]}',
                       'Version': f'{result[1]}'}
    
    # Return success
    return jsonify({'status_code': '200',
                    'message': 'Success. The package has been obtained by ID.',
                    'data': packageData,
                    'metadata': packageMetadata}), 200, {'content_type': 'application/json'}

#? This will replace the current ID with a new package 
#? version (update), as long as ID, version, and name match.
#? aka update by ID
@app.route('/package/<id>', methods=["PUT"])
def PackageUpdate(id=None):
    
    # First, check if ID is none
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be an ID value in order to delete packages'}), 400, {'content_type': 'application/json'}
    
    # Next, obtain data from response.
    #!logs input
    data = json.loads(request.data)
    print("Autograder input: {}".format(data), file = stderr)
    
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
    
    # Then, check if id/name/version match in database. Start with id, then check name and version associated with that id, else return error 404
    query = db.select(table.c["ID", "PackageName", "Version"]).where(table.c.ID == id)
    return_list = connection.execute(query).fetchone()

    if return_list[0] != data["id"]:
        return jsonify({'status_code': '404',
                        'message': 'Package does not exist 3. There must be an \'id\', \'name\', and \'version\'.'}), 404, {'content_type': 'application/json'}
    
    if return_list[1] != data["name"]:
        return jsonify({'status_code': '404',
                        'message': 'Package does not exist 4. There must be an \'id\', \'name\', and \'version\'.'}), 404, {'content_type': 'application/json'}

    if return_list[2] != data["version"]:
        return jsonify({'status_code': '404',
                        'message': 'Package does not exist 5. There must be an \'id\', \'name\', and \'version\'.'}), 404, {'content_type': 'application/json'}
    
    # Update the values for the id
    subprocess.run(["python3", "sql/upload.py"])
    
    # Finally, return 200 status code
    return jsonify({'status_code': '200',
                    'message': 'Version is updated'}), 200, {'content_type': 'application/json'}

#? This is the rating function for a package's id value. This
#? operates similarly to the "Rate" Frontend Page Operation.
@app.route('/package/<id>/rate', methods=["GET"])
def PackageRate(id=None):
    
    # First, check if id is None
    if id == None:
        return jsonify({'status_code': '400',
                        'message': 'There must be a valid ID in order to rate packages'}), 400, {'content_type': 'application/json'}
    
    # Then, check if package is within SQL database by ID
    exist = exists(table.c.ID, id)
    if exist is False:
       return jsonify({'status_code': '404',
                        'message': 'Package doesn\'t exist 6.'}), 404, {'content_type': 'application/json'}
    
    # Then, obtain the scores from the SQL database
    query = db.select(table.c["BusFactor", "Correctness", "Pinning", "Licensing", "NetScore", "UpdatedCode", "RampUp", "Responsiveness"]).where(table.c.ID == id)
    result = connection.execute(query).fetchone()

    # Then, need to format scores according to the PackageRating definition in the YAML and return 200 and PackageRating if successful
    packageRatings = {'BusFactor': f'{result[0]}',
                  'Correctness': f'{result[1]}',
                  'GoodPinninPractice': f'{result[2]}',
                  'LicenseScore': f'{result[3]}',
                  'NetScore': f'{result[4]}',
                  'PullRequest': f'{result[5]}',
                  'RampUp': f'{result[6]}',
                  'ResponsiveMaintainer': f'{result[7]}'}
    
    return jsonify({'status_code': '200',
                    'message': 'Rating has been calculated. View the \'data\' field for values',
                    'data': packageRatings}), 200, {'content_type': 'application/json'}

#? This is the fetch command. Need to understand it more
#? before implementing it.
#! No idea how to do this currently, must examine later
@app.route('/packages', methods=["POST"])
def PackagesList():
    return jsonify({'status_code': '200',
                    'message': 'This is a test, must implement later'}), 200, {'content_type': 'application/json'}

#? This is the SQL reset. Resets the SQL database to a 
#? default state.
@app.route('/reset', methods=["DELETE"])
def RegistryReset():

    # SQL delete table
    query = db.delete(table)
    connection.execute(query)
    connection.commit()

    # Return success
    return jsonify({'status_code': '200',
                    'message': 'Registry is reset'}), 200, {'content_type': 'application/json'}


# Main function call to start backend/frontend
if __name__ == "__main__":
    application.add_api('api-spec.yaml')
    app.static_folder = ('templates/static')
    app.template_folder = ('templates')
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))

