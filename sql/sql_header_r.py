G='Packages'
from google.cloud.sql.connector import Connector,IPTypes
import pymysql,sqlalchemy as A,os
def F():B='10.65.176.3';C=os.environ['SQL_USER'];D=os.environ['SQL_PASSWORD'];E=os.environ['SQL_DB'];F=3306;G=A.create_engine(A.engine.url.URL.create(drivername='mysql+pymysql',username=C,password=D,host=B,port=F,database=E));return G
B=F()
D=B.connect()
E=A.MetaData()
C=A.Table(G,E,autoload_with=B)
def J(search_in,search_for):B=A.select(C).where(search_in==search_for);E=D.execute(B);D.commit();F=bool(E.fetchone());return F
if __name__=='__main__':B=F();D=B.connect();E=A.MetaData();C=A.Table(G,E,autoload_with=B);H=A.select(C).where(C.c.ID==9);I=D.execute(H);K=I.fetchone();print(C.columns.keys())