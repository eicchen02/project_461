from flask import Flask,render_template,request, redirect, url_for, session
import subprocess
import os
from json import load
 
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        link_local = request.form["link_input"]
        f = open("log/temp_link.txt", "w+")
        f.write(link_local)
        f.close()
        
        subprocess.run(["./run", "showscore", "log/temp_link.txt"])
        # session['link'] = link_local
        return redirect(url_for("display"))
    else:
	    return render_template("form.html")
    

@app.route("/done")
def display():
    test_text = load(open("output/output.json"))
    
    if(len(test_text) ==  0):
       test_text = "ERROR: file can't be read"  

    return render_template("test.html", variable = test_text)

 
if __name__ == "__main__": 
    # app.run(host='localhost', port=8080)
    app.run(debug = True, host = '0.0.0.0', port  = int(os.environ.get('PORT', 8080)))