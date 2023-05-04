I='finished cloning url #'
H=Exception
E='local_cloning/cloned_repos/'
from git import Repo as F
import sys,os as A,re,urllib.request as J
from subprocess import DEVNULL
B=sys.argv[1]
A.mkdir(E)
C=open('log/logv1.txt','w')
K=open('log/logv2.txt','w')
if'github'in B:F.clone_from(B,E+A.path.basename(B)+'/');C.write(I+str(A.path.basename(B))+'\n')
else:
	G=J.urlopen(B)
	if G.getcode()==200:
		L=G.read().decode('utf-8');M='<span id="repository-link">(.*?)<\\/span>'
		try:N=re.search(M,L);D='https://'+N.group(1)
		except:raise H('Valid GitHub link not found.\n')
	else:raise H('npm url not able to connect.\n')
	F.clone_from(D,E+A.path.basename(D)+'/');C.write(I+A.path.basename(D)+'\n')
C.close()
K.close()
exit(0)