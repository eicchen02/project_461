from flask import Flask,render_template,request, redirect, url_for, session
import subprocess
import os
from json import load
from time import sleep
from os import remove
 
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        link_local = request.form["link_input"]

        if(link_local.find("github") and link_local.find("npm") == 0):
            return redirect(url_for("error_link"))
        
        f = open("temp_link.txt", "w+")
        f.write(link_local)
        f.close()

        subprocess.run(["./run", "showscore", "temp_link.txt"])
        subprocess.run(["python3", "sql/upload.py"])
        
        return redirect(url_for("done"))
    else:
	    return render_template("form.html")
     

@app.route("/done")
def done():
    try:
        test_text = load(open("output/output.json"))
        # remove("output/output.json")
        return render_template("test.html", variable = test_text)

    except:
       return redirect(url_for("error_output"))

    

@app.route("/error")
def error():
    return f'<h1> Whoops, Error! <h1>'

@app.route("/error_link")
def error_link():
    return f'<h2> Your input was invald, please use a valid Github/npm link <h2>'

@app.route("/error_output")
def error_output():
    return f'<h2> Output could not be read/errored <h2>'

 
if __name__ == "__main__": 
    # app.run(host='localhost', port=8080)
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))