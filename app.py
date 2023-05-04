_A0='/package/byName/<name>'
_z='Package is deleted'
_y="Package name cannot be 'None'."
_x='SELECT * FROM Packages'
_w='metadata'
_v='download_status_details'
_u='download_status'
_t='rate_status_details'
_s='Pinning'
_r='Licensing'
_q='UpdatedCode'
_p='Responsiveness'
_o='PackageLink'
_n='No such package exists!'
_m='Package is not uploaded due to a disqualified rating.\nEvery metric must score greater than 0.5'
_l='npmjs.com'
_k='github.com'
_j='/package/<id>'
_i='There must be an ID value in order to delete packages'
_h='DELETE'
_g='data'
_f='NetScore'
_e='RampUp'
_d='BusFactor'
_c='Correctness'
_b='update_status'
_a='upload'
_Z='./run'
_Y='upload_status'
_X='Autograder input: {}'
_W='PackageName'
_V='rate_status'
_U='update_status_details'
_T='sql/upload.py'
_S='python3'
_R="Package doesn't exist."
_Q='upload_status_details'
_P='output/output.json'
_O='200'
_N='Name'
_M=False
_L='temp_link.txt'
_K='ID'
_J='POST'
_I='Version'
_H='404'
_G='GET'
_F='400'
_E=None
_D='content_type'
_C='message'
_B='status_code'
_A='application/json'
from flask import Flask,render_template,request,redirect,url_for,session,jsonify,send_file,Response
import connexion,json,subprocess,os
from input.toEncodedPackage import createEncodedFile
from sql.search import*
from json import load
from time import sleep
from os import remove
from sys import stderr
from sql.sql_header import*
application=connexion.FlaskApp(__name__,specification_dir='Rest_API_File/')
app=application.app
app.secret_key=os.urandom(24)
@app.route('/')
def home():return render_template('Home.html')
@app.route('/database/')
def database():return render_template('Database.html')
@app.route('/database/packages/')
def packageList():return render_template('PackageList.html')
@app.route('/database/upload',methods=[_G,_J])
def upload():
	A='uploadComplete'
	if request.method==_J:
		session[_Y]='Error with Uploading';package_url=request.form['upload_input'];print('Input package_url: '+package_url,file=stderr)
		if _k not in package_url and _l not in package_url:session[_Q]='Package is not uploaded due to an invalid URL link';return redirect(url_for(A))
		exist=exists(table.c.PackageLink,package_url);f=open(_L,'w+');f.write(package_url);f.close();subprocess.run([_Z,_a,_L]);sleep(.1);output=load(open(_P))[0]
		for score in output.values():
			if type(score)==float and score<.5:session[_Q]=_m;return redirect(url_for(A))
		subprocess.run([_S,_T]);remove(_P);remove(_L);session[_Y]='Package has been Uploaded';session[_Q]='The given package has been uploaded to our database!';return redirect(url_for(A))
	else:return render_template('interactions/Upload.html')
@app.route('/database/update/',methods=[_G,_J])
def update():
	A='updateComplete'
	if request.method==_J:
		session[_b]='Error with Updating';package_url=request.form['update_input']
		if _k not in package_url and _l not in package_url:session[_U]='Package is not updated due to an invalid URL link';return redirect(url_for(A))
		exist=exists(table.c.PackageLink,package_url)
		if exist is _M:session[_U]="Package doesn't exist, try uploading instead!";return redirect(url_for(A))
		f=open(_L,'w+');f.write(package_url);f.close();subprocess.run([_Z,_a,_L]);sleep(.1);output=load(open(_P))[0];subprocess.run([_S,_T]);remove(_P);remove(_L);session[_b]='Package has been Updated';session[_U]='The given package has been updated in our database!';return redirect(url_for(A))
	else:return render_template('/interactions/Update.html')
@app.route('/database/rate/',methods=[_G,_J])
def rate():
	A='rateComplete'
	if request.method==_J:
		session[_V]='Error with Rating';package_url=request.form['rate_input'];exist=exists(table.c.PackageLink,package_url)
		if exist is _M:session[_V]=_n;return redirect(url_for(A))
		columns=[_W,_o,_p,_q,_c,_d,_e,_r,_s,_f];query=db.select(table).where(table.c.PackageLink==package_url);result=connection.execute(query).fetchall();print(table.columns.keys());session[_V]=f"Results for {result[0][0]}:";session[_t]=f"Net Score: {result[0][8]}, Bus Factor: {result[0][5]}, Ramp Up: {result[0][6]},\n Pinning Practice: {result[0][10]}, Responsiveness: {result[0][2]}, Pull Requests: {result[0][3]}\n, Correctness: {result[0][4]}, Licensing: {result[0][7]}";return redirect(url_for(A))
	else:return render_template('interactions/Rate.html')
@app.route('/database/download/',methods=[_G,_J])
def download():
	A='local_cloning/encoded_repos'
	if request.method==_J:
		session[_u]='Error with Downloading';package_url=request.form['download_input'];exist=exists(table.c.PackageLink,package_url)
		if exist is _M:session[_v]=_n;return redirect(url_for('downloadComplete'))
		zipPackage,encodedPackage=createEncodedFile(package_url);return send_file(f"{zipPackage}",as_attachment=True)
	else:
		if os.path.exists(A):
			for f in os.listdir(A):os.remove(os.path.join(A,f))
		return render_template('/interactions/Download.html')
@app.route('/database/upload/complete',methods=[_G])
def uploadComplete():return render_template('interactions/complete/UploadComplete.html',status_message=session[_Y],status_message_details=session[_Q])
@app.route('/database/update/complete',methods=[_G])
def updateComplete():return render_template('interactions/complete/UpdateComplete.html',status_message=session[_b],status_message_details=session[_U])
@app.route('/database/rate/complete',methods=[_G])
def rateComplete():return render_template('interactions/complete/RateComplete.html',status_message=session[_V],status_message_details=session[_t])
@app.route('/database/download/complete',methods=[_G])
def downloadComplete():return render_template('interactions/complete/DownloadComplete.html',status_message=session[_u],status_message_details=session[_v])
@app.route('/authenticate',methods=['PUT'])
def CreateAuthToken():return jsonify({_B:'501',_C:'This system does not support authentication'}),501,{_D:_A}
@app.route('/package',methods=[_J])
def PackageCreate():
	B='Content';A='URL';data=json.loads(request.data);print(_X.format(data),file=stderr)
	if A in data and data[A]!=_E:file=data[A]
	elif B in data and data[B]!=_E:file=data[B]
	else:return jsonify({_B:_F,_C:'There is missing field(s) in the PackageData or it is formed inproperly'}),400,{_D:_A}
	f=open(_L,'w+');f.write(file);f.close();subprocess.run([_Z,_a,_L]);sleep(.1);output=load(open(_P))[0];obtainedURL=output[A];exist=exists(table.c.PackageLink,obtainedURL)
	for score in output.values():
		if type(score)==float and score<.5:session[_Q]=_m;return jsonify({_B:'424',_C:'Package is not uploaded due to the disqualified rating.'}),424,{_D:_A}
	subprocess.run([_S,_T]);remove(_P);remove(_L)
	try:version=load(open(f"local_cloning/cloned_repos/{os.path.basename(obtainedURL)}/package.json"))['version']
	except:return jsonify({_B:_H,_C:"The provided package does not have a valid 'package.json'"}),404,{_D:_A}
	query=db.select(table.c.ID).where(table.c.PackageLink==obtainedURL);return_id=connection.execute(query).scalar();metadata={_K:f"{return_id}",_N:f"{os.path.basename(obtainedURL)}",_I:f"{version}"};packageData={B:_E,A:f"{obtainedURL}",'JSProgram':_E};return jsonify({_B:'201',_C:'Success. Check the ID in the returned metadata for the official ID.',_g:packageData,_w:metadata}),201,{_D:_A}
@app.route('/package/byRegEx',methods=[_G])
def PackageByRegExGet():
	data=json.loads(request.data);print(_X.format(data),file=stderr);regex=data['regex']
	if regex==_E:return jsonify({_B:_F,_C:'There must be a regular expression that can be used in the body.'}),400,{_D:_A}
	packageMatches=[];t=sqlalchemy.text(_x);result=connection.execute(t)
	for row in result:
		if checkInput(row[0],regex)or checkInput(row[1],regex)or checkInput(row[9],regex):packageMatches.append({_N:row[0],_K:row[11],_I:row[13]})
	if not packageMatches:return jsonify({_B:_H,_C:'No package found under this regex'}),404,{_D:_A}
	return jsonify({_B:_O,_C:"Attached is the list of packages. Check the 'data' field for the list",_g:packageMatches}),200,{_D:_A}
@app.route(_A0,methods=[_h])
def PackageByNameDelete(name=_E):
	if name==_E:return jsonify({_B:_F,_C:_y}),400,{_D:_A}
	exist=exists(table.c.PackageName,name)
	if exist is _M:return jsonify({_B:_H,_C:_R}),404,{_D:_A}
	query=db.delete(table).where(table.c.PackageName==name);connection.execute(query);connection.commit();return jsonify({_B:_O,_C:_z}),200,{_D:_A}
@app.route(_A0,methods=[_G])
def PackageByNameGet(name=_E):
	if name==_E:return jsonify({_B:_F,_C:_y}),400,{_D:_A}
	exist=exists(table.c.PackageName,name)
	if exist is _M:return jsonify({_B:_H,_C:_R}),404,{_D:_A}
	query=db.select(table.c.LastModified).where(table.c.PackageName==name);history_date=connection.execute(query).scalar();return jsonify({_B:_O,_C:"Obtained the history of the given package. Check in the 'history' field for the data.",'history':f"{history_date}"}),200,{_D:_A}
@app.route(_j,methods=[_h])
def PackageDelete(id=_E):
	if id==_E:return jsonify({_B:_F,_C:_i}),400,{_D:_A}
	exist=exists(table.c.ID,id)
	if exist is _M:return jsonify({_B:_H,_C:_R}),404,{_D:_A}
	query=db.delete(table).where(table.c.ID==id);connection.execute(query);connection.commit();return jsonify({_B:_O,_C:_z}),200,{_D:_A}
@app.route(_j,methods=[_G])
def PackageRetrieve(id=_E):
	if id==_E:return jsonify({_B:_F,_C:_i}),400,{_D:_A}
	exist=exists(table.c.ID,id)
	if exist is _M:return jsonify({_B:_H,_C:_R}),404,{_D:_A}
	query=db.select(table.c[_W,_I,_o]).where(table.c.ID==id);result=connection.execute(query).fetchone();zipPackagePath,base64PackagePath=createEncodedFile(result[2]);data=open(base64PackagePath,'rb');packageMetadata={_K:f"{id}",_N:f"{result[0]}",_I:f"{result[1]}"}
	def generator(packageMetadata,URL,ContentFile):
		yield'{"status_code": "200", "message": "Success. The package has been obtained by ID.", "metadata": '+json.dumps(packageMetadata)+', "data": {"URL": "'+URL+'", "Content": "'
		while True:
			data=ContentFile.read(256)
			if not data:break
			yield data
		yield'"}}'
	return Response(generator(packageMetadata,result[2],data),content_type=_A)
@app.route(_j,methods=['PUT'])
def PackageUpdate(id=_E):
	B="Package does not exist. There must be an 'id', 'name', and 'version'.";A="There are missing field(s) in the request body. There must be an 'ID', 'Name', and 'Version'."
	if id==_E:return jsonify({_B:_F,_C:_i}),400,{_D:_A}
	data=json.loads(request.data);print(_X.format(data),file=stderr)
	if not data[_K]or data[_K]==_E:return jsonify({_B:_F,_C:A}),400,{_D:_A}
	elif not data[_N]or data[_N]==_E:return jsonify({_B:_F,_C:A}),400,{_D:_A}
	elif not data[_I]or data[_I]==_E:return jsonify({_B:_F,_C:A}),400,{_D:_A}
	query=db.select(table.c[_K,_W,_I]).where(table.c.ID==id);return_list=connection.execute(query).fetchone()
	if return_list[0]!=data[_K]:return jsonify({_B:_H,_C:B}),404,{_D:_A}
	if return_list[1]!=data[_N]:return jsonify({_B:_H,_C:B}),404,{_D:_A}
	if return_list[2]!=data[_I]:return jsonify({_B:_H,_C:B}),404,{_D:_A}
	subprocess.run([_S,_T]);return jsonify({_B:_O,_C:'Version is updated'}),200,{_D:_A}
@app.route('/package/<id>/rate',methods=[_G])
def PackageRate(id=_E):
	if id==_E:return jsonify({_B:_F,_C:'There must be a valid ID in order to rate packages'}),400,{_D:_A}
	exist=exists(table.c.ID,id)
	if exist is _M:return jsonify({_B:_H,_C:_R}),404,{_D:_A}
	query=db.select(table.c[_d,_c,_s,_r,_f,_q,_e,_p]).where(table.c.ID==id);result=connection.execute(query).fetchone();packageRatings={_d:f"{result[0]}",_c:f"{result[1]}",'GoodPinningPractice':f"{result[2]}",'LicenseScore':f"{result[3]}",_f:f"{result[4]}",'PullRequest':f"{result[5]}",_e:f"{result[6]}",'ResponsiveMaintainer':f"{result[7]}"};return jsonify({_B:_O,_C:"Rating has been calculated. View the 'data' field for values",_g:packageRatings}),200,{_D:_A}
@app.route('/packages',methods=[_J])
def PackagesList():
	G='There are missing fields in the PackageQuery';F='~';E='^';D='-';C='SemverRange';B='PackageNames';A='.';data=json.loads(request.data);print(_X.format(data),file=stderr)
	if not data[C]or data[C]==_E:return jsonify({_B:_F,_C:G}),400,{_D:_A}
	if not data[B]or data[B]==_E:return jsonify({_B:_F,_C:G}),400,{_D:_A}
	packageList=[];providedRange=data[C]
	if providedRange.find(D)!=-1:lowerBound=providedRange.split(D)[0];upperBound=providedRange.split(D)[1]
	elif providedRange.find(E)!=-1:lowerBound=providedRange.split(E)[0];upperBound=providedRange.split(E)[0]
	elif providedRange.find(F)!=-1:lowerBound=providedRange.split(F)[0];upperBound=providedRange.split(F)[0]
	else:lowerBound=providedRange;upperBound=providedRange
	if data[B][0]=='*':
		t=sqlalchemy.text(_x);result=connection.execute(t)
		for row in result:
			obtainedVersion=row[13];numericValues=obtainedVersion.split(A)
			if numericValues[0]>=lowerBound.split(A)[0]and numericValues[0]<=upperBound.split(A)[0]:
				if numericValues[1]>=lowerBound.split(A)[1]and numericValues[1]<=upperBound.split(A)[1]:
					if numericValues[2]>=lowerBound.split(A)[2]and numericValues[2]<=upperBound.split(A)[2]:packageList.append({_N:row[0],_K:row[11],_I:row[13]})
	elif not data[B]:return jsonify({_B:'413',_C:'Too many packages to return. Please specify a PackageQuery.'}),413,{_D:_A}
	else:
		for package in data[B]:
			if exists(table.c.PackageName,package):
				query=db.select(table.c[_W,_K,_I]).where(table.c.PackageName==package);result=connection.execute(query).fetchone();numericValues=result[2].split(A)
				if numericValues[0]>=lowerBound.split(A)[0]and numericValues[0]<=upperBound.split(A)[0]:
					if numericValues[1]>=lowerBound.split(A)[1]and numericValues[1]<=upperBound.split(A)[1]:
						if numericValues[2]>=lowerBound.split(A)[2]and numericValues[2]<=upperBound.split(A)[2]:packageList.append({_N:result[0],_K:result[1],_I:result[2]})
	if not packageList:return jsonify({_B:_H,_C:'No packages could be obtained within the provided SemverRange.'}),404,{_D:_A}
	return jsonify({_B:_O,_C:"Obtained a list of packages. Check the 'metadata' field for the list.",_w:packageList}),200,{_D:_A}
@app.route('/reset',methods=[_h])
def RegistryReset():query=db.delete(table);connection.execute(query);connection.commit();return jsonify({_B:_O,_C:'Registry is reset'}),200,{_D:_A}
if __name__=='__main__':application.add_api('api-spec.yaml');app.static_folder='templates/static';app.template_folder='templates';app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))