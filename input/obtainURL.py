E=print
A=open
import base64 as C,zipfile as I,sys,json,os
from urllib.parse import urlparse as D
def B():
	M='repository';L='url';K='temp.zip';H='r';input=sys.argv[1]
	try:
		B=A(input,H).read()
		if C.b64encode(C.b64decode(B)):
			with A(K,'wb')as N:N.write(C.b64decode(B))
			F=I.ZipFile('./temp.zip',H);F.extractall('local_cloning/cloned_repos/');F.close();O,=I.Path(F).iterdir();os.remove(K);P=A(f"local_cloning/cloned_repos/{O.name}/package.json");J=json.load(P)
			if L in J[M]:G=J[M][L];Q=D(G).scheme+'://'+D(G).netloc;R=D(G).path;E(Q+os.path.splitext(R)[0])
			else:E('-1')
	except:
		with A(input,H)as B:E(B.read())
if __name__=='__main__':B()