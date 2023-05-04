Q='data'
P='github.com/'
K='repository'
J='\n'
I='w'
H=open
import requests as R,sys,json,os
S=os.getenv('GITHUB_TOKEN')
E=sys.argv[1]
C=H('log/logv1.txt',I)
A=H('log/logv2.txt',I)
L=[]
C.write(f"\n\n>>> Extracting information for url {E}\n")
B=E.partition(P)[2]
if not B:
	E=os.path.basename(E.strip(J))
	with H(f"local_cloning/cloned_repos/{E}/package.json")as T:U=json.load(T)
	B=U[K]
	if not isinstance(B,str):B=list(B.values())[1];B=B.partition(P)[2].replace('.git','')
L.append((B.partition('/')[0],B.partition('/')[2].replace(J,'')))
V={'Authorization':f"Bearer {S}"}
with H('output/correctness_out.txt',I)as M:
	for D in L:
		C.write('\n\n>>> beginning correctness metric with GraphQL api\n');A.write('\n\n------------------\n');A.write('current analysis of correctness will be done with github GraphQL api\n');A.write('beginning retrieval of information from repository %s %s\n'%(D[0],D[1]));A.write('------------------\n');W=f'{{repository(owner: "{D[0]}", name: "{D[1]}") {{stargazerCount openIssues: issues(states: OPEN) {{totalCount}}}}}}';F=R.post('https://api.github.com/graphql',json={'query':W},headers=V)
		if F.status_code==200:
			C.write('successful graphql api retrieval\n');A.write('successful graphQL api retrieval with code %d\n'%F.status_code)
			try:G=F.json()[Q][K]['stargazerCount'];N=F.json()[Q][K]['openIssues']['totalCount'];O=G/(G+N*10);C.write('proper repo format\n');A.write('proper repo format - data retrieval successful\n');A.write('Number of stars: %i\n'%G);A.write('Number of open issues: %i\n'%N);C.write('Repo had %d stars\n'%G);A.write('Correctness score for repo %s owned by %s: %f \n'%(D[1],D[0],O))
			except:C.write('improper repo format\n');A.write('improper repo format - error with repo\n')
			M.write(str(O));M.write(J)
		else:C.write('Failed to retrieve response');A.write('Failed to retrieve response with code %d\n'%F.status_code)
C.close()
A.close()