from sql_header import*
import json,re
from os import listdir
from sqlalchemy.orm import sessionmaker
import sys
from datetime import datetime
def upload():
	K='LICENSE_SCORE';J='RESPONSIVE_MAINTAINER_SCORE';I='BUS_FACTOR_SCORE';H='CORRECTNESS_SCORE';G='PINNING_PRACTICE_SCORE';F='UPDATED_CODE_SCORE';E='RAMP_UP_SCORE';D='NET_SCORE';C='Error getting version';B='version';A='URL';f=open('output/output.json');data=json.load(f)[0];f.close();repo_url=data[A];repo_name=re.search('.+\\/(.+)$',repo_url)
	if repo_name is None:raise'No valid name found from link'
	PackageName=repo_name[1];readme_dir='local_cloning/cloned_repos/{}'.format(repo_name[1]);dir_list=listdir(readme_dir);readme_regex=re.compile('readme.',flags=re.IGNORECASE)
	for item in dir_list:
		if readme_regex.search(item):readme_file=item
	try:
		with open(readme_dir+'/'+readme_file)as f3:
			readme_content=str()
			for(count,line)in enumerate(f3):
				if count<200:readme_content=readme_content+line
				else:break
	except:raise'Error reading readme'
	try:
		package=open(f"local_cloning/cloned_repos/{PackageName}/package.json");jsonData=json.load(package)
		if B in jsonData:version=jsonData[B]
		else:raise C
	except:raise C
	exist=exists(table.c.PackageLink,data[A])
	if exist is False:print("It doesn't exist! Uploading",file=sys.stderr);query=table.insert().values(PackageLink=data[A],NetScore=data[D],RampUp=data[E],UpdatedCode=data[F],Pinning=data[G],Correctness=data[H],BusFactor=data[I],Responsiveness=data[J],Licensing=data[K],PackageName=PackageName,Readme=readme_content,LastModified=datetime.now(),Version=version)
	else:print('It does exist! Updating',file=sys.stderr);query=table.update().where(table.c.PackageLink==data[A]).values(PackageLink=data[A],NetScore=data[D],RampUp=data[E],UpdatedCode=data[F],Pinning=data[G],Correctness=data[H],BusFactor=data[I],Responsiveness=data[J],Licensing=data[K],PackageName=PackageName,Readme=readme_content,LastModified=datetime.now(),Version=version)
	result=connection.execute(query);connection.commit();print('Upload/Update Complete!',file=sys.stderr)
if __name__=='__main__':upload()