G=Exception
import base64 as N,sys,os as A
from git import Repo as E
import urllib.request as O,re,zipfile as F
def B(url):
	M='./local_cloning/cloned_repos/';L='./local_cloning/encoded_repos';B=url
	if not A.path.exists(L):A.makedirs(L)
	H=f"./local_cloning/cloned_repos/{A.path.basename(B)}/"
	if not A.path.exists(H):
		if'github'in B:E.clone_from(B,M+A.path.basename(B)+'/')
		else:
			I=O.urlopen(B)
			if I.getcode()==200:
				P=I.read().decode('utf-8');Q='<span id="repository-link">(.*?)<\\/span>'
				try:R=re.search(Q,P);J='https://'+R.group(1)
				except:raise G('Valid GitHub link not found.\n')
			else:raise G('npm url not able to connect.\n')
			E.clone_from(J,M+A.path.basename(J)+'/')
	C=F.ZipFile(f"./local_cloning/encoded_repos/{A.path.basename(B)}.zip",'w',F.ZIP_DEFLATED)
	for(D,Y,S)in A.walk(H):
		C.write(D)
		for K in S:C.write(A.path.join(A.path.relpath(D),K),arcname=A.path.join(D.replace(f"local_cloning/cloned_repos/{A.path.basename(B)}",''),K))
	C.close()
	with open(f"./local_cloning/encoded_repos/{A.path.basename(B)}.zip",'rb')as T,open(f"./local_cloning/encoded_repos/{A.path.basename(B)}_base64",'wb')as U:V=N.b64encode(T.read());U.write(V)
	W=f"./local_cloning/encoded_repos/{A.path.basename(B)}.zip";X=f"./local_cloning/encoded_repos/{A.path.basename(B)}_base64";return W,X