import re,os as A
from pathlib import Path
G=[re.compile('(?i)README.md'),re.compile('(?i)README.txt')]
O=re.compile('(?i)license')
C=0
D='local_cloning/cloned_repos/'
with open('output/license_out.txt','w')as B:
	for H in A.listdir(D):
		E=A.path.join(D,H)
		if A.path.isdir(E):
			C=0
			for(I,P,J)in A.walk(E):
				for F in J:
					for K in G:
						if K.match(F)and C==0:
							L=A.path.join(I,F)
							with open(L,'r')as M:
								N=M.read()
								if'license'or'LICENSE'or'License'in N:B.write(str(1.));B.write('\n')
								else:B.write(str(.0));B.write('\n')
								C=1