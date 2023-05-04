G='r'
F=float
E=round
D=open
from pathlib import Path
from collections import Counter
from git import Repo
import sys,json
A=0
C=[]
J=[]
H=[]
K=[]
I=[]
license=[]
L=[]
M=[]
N=[]
P=sys.argv[1]
b=Path('metric_out_files/')
with D('output/rampup_out.txt',G)as Q:
	for B in Q:J.append(F(B.strip()))
with D('output/busfactor_out.txt',G)as R:
	for B in R:L.append(F(B.strip()))
with D('output/correctness_out.txt',G)as S:
	for B in S:H.append(F(B.strip()))
with D('output/resp_maintain_out.txt',G)as T:
	for B in T:K.append(F(B.strip()))
with D('output/license_out.txt',G)as U:
	for B in U:license.append(F(B.strip()))
with D('output/updatedcode_out.txt',G)as V:
	for B in V:M.append(F(B.strip()))
with D('output/pinningpractice_out.txt',G)as W:
	for B in W:N.append(F(B.strip()))
A=0
for X in H:I.append((L[A]*5.+K[A]*4.+H[A]*3.+J[A]*2.+M[A]*2.+N[A]*2.+license[A])/19.);A+=1
A=0
for X in I:C.append({});C[A].update({'URL':P});C[A].update({'NET_SCORE':E(I[A],2)});C[A].update({'RAMP_UP_SCORE':E(J[A],2)});C[A].update({'UPDATED_CODE_SCORE':E(M[A],2)});C[A].update({'PINNING_PRACTICE_SCORE':E(N[A],2)});C[A].update({'CORRECTNESS_SCORE':E(H[A],2)});C[A].update({'BUS_FACTOR_SCORE':E(L[A],2)});C[A].update({'RESPONSIVE_MAINTAINER_SCORE':E(K[A],2)});C[A].update({'LICENSE_SCORE':E(license[A],2)});A+=1
Y=list(zip(I,C))
Z=sorted(Y,reverse=True)
O=[A[1]for A in Z]
print(O)
with D('output/output.json','w+')as a:json.dump(O,a)
exit(0)