A=Exception
C=print
import requests as M,urllib.request as D,re,sys,os
def N(repo):
	B=D.urlopen(repo)
	if B.getcode()==200:
		C=B.read().decode('utf-8');E='<span id="repository-link">(.*?)<\\/span>'
		try:F=re.search(E,C);G='https://'+F.group(1)
		except:raise A('Valid GitHub link not found.\n')
	else:raise A('npm url not able to connect.\n')
	return G
def B():
	L='additions';K='nodes';J='repository';I='data';F='0.0';D=sys.argv[1]
	if D=='':C(F);return
	if'npmjs.com/'in D:G=N(D)
	else:G=D
	O=os.environ.get('GITHUB_TOKEN');H=G.split('github.com/',1)[1].split('/');P={'Authorization':f"Bearer {O}"};Q='\n    {\n      repository(owner: "%s", name: "%s") {\n        pullRequests(states: MERGED, last: 100) {\n          nodes {\n            additions\n          }\n        }\n        commitComments(last: 100) {\n          nodes {\n            commit {\n              additions\n            }\n          }\n        }\n      }\n    }\n    '%(H[0],H[1]);R={'query':Q};E=M.post(url='https://api.github.com/graphql',json=R,headers=P)
	if E.status_code==200:
		try:
			A=0;B=0
			for S in E.json()[I][J]['pullRequests'][K]:
				try:A+=S[L]
				except:A+=0
			for T in E.json()[I][J]['commitComments'][K]:
				try:B+=T['commit'][L]
				except:B+=0
		except:A=0;B=1
		if A==0 and B==0:C(F)
		else:C(f"{round(A/(A+B),2)}")
	else:C(F)
if __name__=='__main__':B()