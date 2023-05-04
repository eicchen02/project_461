B=print
import requests as C,base64,zipfile
from sys import argv
def D(link):
	L='Test';K='cloudinary_npm';I='data';H='Content';G='/package/';D=link;J=K;id='18';E={'X-Authorization':L};A=C.delete(D+'/reset',headers=E)
	if A.status_code==200:B(f"Database Reset Test: {A.json()}\n")
	else:B(f"The database could not be reset, due to an error code {A.status_code}\n")
	A=C.put(D+'/authenticate',json={'Secret':{'password':'TestTest'},'User':{'isAdmin':True,'name':L}});B(f"Authentication Test: {A.json()}\n");A=C.post(D+'/package',headers=E,json={H:None,'URL':'https://github.com/cloudinary/cloudinary_npm','JSProgram':"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n"})
	if A.status_code==201:M=A.json()[I];F=A.json()['metadata'];B(f"Package Create Test, Grabbing metadata: {F}\n");J=F['Name'];id=F['ID'];N=F['Version']
	else:B(f"The package was not uploaded, due to an error code {A.status_code}\n")
	A=C.get(D+'/package/byName/'+J,headers=E)
	if A.status_code==200:B(f"Package By Name History Test: {A.json()}\n")
	else:B(f"The package history could not be obtained by name, due to an error code {A.status_code}\n")
	A=C.get(D+'/package/byRegEx',headers=E,json={'regex':K})
	if A.status_code==200:B(f"Package By RegEx Search Test: {A.json()}\n")
	else:B(f"The package could not be searched by RegEx, due to an error code {A.status_code}\n")
	A=C.get(D+G+id,headers=E)
	if A.status_code==200:
		if A.json()[I][H]!=None:B(f"Package By ID Retrieve Test: Content field set {A.json()[I][H]}\n")
		else:B("Package By ID Retrieve Test: Obtained 200, but not 'Content' field\n")
	else:B(f"The package could not be retrieved by ID, due to an error code {A.status_code}\n")
	A=C.get(D+G+id,headers=E)
	if A.status_code==200:B(f"Package By ID Update Test: Success\n")
	else:B(f"The package could not be retrieved by ID, due to an error code {A.status_code}\n")
	A=C.get(D+G+id+'/rate',headers=E)
	if A.status_code==200:B(f"Package By ID Rate Test: {A.json()}\n")
	else:B(f"The package could not be rated by ID, due to an error code {A.status_code}\n")
	A=C.post(D+'/packages',headers=E,json={'PackageNames':['*'],'SemverRange':'1.36.4'})
	if A.status_code==200:B(f"Packages Fetch Test: {A.json()}\n")
	else:B(f"The packages could not be fetched, due to an error code {A.status_code}\n")
	A=C.delete(D+G+id,headers=E)
	if A.status_code==200:B(f"Package By ID Delete Test: {A.json()}\n")
	else:B(f"The package could not be deleted by ID, due to an error code {A.status_code}\n")
if __name__=='__main__':
	if argv[1]=='-l':A='http://127.0.0.1:8080'
	else:A='https://project-461-xm2e3izt6a-uc.a.run.app'
	B(A);D(A)