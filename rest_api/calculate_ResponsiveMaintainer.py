O='https://github.com/'
B='\n'
I=str
F=open
E=int
import requests as Q
from pprint import pprint
import sys,json,datetime as L,os
M=1000
N=1.1
def C(githubRepoURL):
	J=githubRepoURL;R=J.split(O)[1];S='https://api.github.com/repos/'+R;T=os.getenv('GITHUB_TOKEN');B=F('log/logv1.txt','a+');A=F('log/logv2.txt','a+');B.write('\n\n>>> beginning respmaintainer metric with REST api\n');A.write('\n\n------------------\n');A.write('current analysis of responsive maintainer metric will be done with github REST api\n');A.write('beginning retrieval of information from repository %s\n'%J);A.write('------------------\n');U={'Authorization':f"token {T}"};G=Q.get(url=S,headers=U)
	if G.status_code==200:
		B.write('able to receive response from github\n');A.write('able to receive response code %d from github\n'%G.status_code)
		try:K=G.json();Y=K['has_issues'];P=E(K['open_issues_count']);D=K['updated_at'];D=D.split('-');V=E(D[0]);W=E(D[1]);X=E(D[2].split('T')[0]);D=L.date(V,W,X);B.write('proper repo format - data retrieval successful\n');A.write('proper repo format - retrieved %s from the api\n'%D)
		except:B.write('improper repo format');A.write('improper repo format- investigate repo at %s \n'%J);return-1
		H=0
		if P>25:B.write('number of open issues exceeded threshold\n');A.write('number of open issues exceeded threshold of 25\n');H+=min(.2,.2*((M-P)/M))
		C=I(L.date.today()-D)
		if C=='0:00:00':B.write('repo was updated today\n');A.write('repo was updated today, i.e. day difference was %s\n'%C);C=0
		else:
			C=E(C.split(' ')[0]);B.write('repo was not updated today\n');A.write('repo was not updated today, it was updated %d days ago\n'%C)
			if C<0:C=0
		H+=.75*N**(-1*C);A.write('responsive maintainer score was calculated to be %f with decay factor %f\n'%(H,N));B.close();A.close();return H
	else:B.write('failed to resolve repository\n');A.write('failed to resolve repository with response code %d from github\n'%G.status_code);B.close();A.close();return-1
def D(repo):
	G='github.com/';C='/';D=[];A=repo.partition(G)[2]
	if not A:
		H=os.path.basename(repo.strip(B))
		with F(f"local_cloning/cloned_repos/{H}/package.json")as J:K=json.load(J);A=K['repository']
		if not isinstance(A,I):A=list(A.values())[1];A=A.partition(G)[2].replace('.git','')
	D.append((A.partition(C)[0],A.partition(C)[2].replace(B,'')))
	for E in D:L=O+E[0]+C+E[1];M=L
	return M
def A():
	E=sys.argv[1];G=D(E)
	with F('output/resp_maintain_out.txt','w')as A:H=C(G);A.write(I(H));A.write(B)
if __name__=='__main__':A()