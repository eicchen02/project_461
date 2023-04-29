from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy as db
import os

ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

connector = Connector(ip_type)

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        os.environ.get("SQL_LINK", "No SQL_LINK"),
        "pymysql",
        user=os.environ.get("SQL_USER", "No SQL_USER"),
        password=os.environ.get("SQL_PASSWORD", "No SQL_Password"),
        db=os.environ.get("SQL_DB", "No SQL_DB")
    )
    return conn

# create connection pool
pool = db.create_engine(
    "mysql+pymysql://",
    creator=getconn,
    # echo=True
)

if __name__ == "__main__":
    connection = pool.connect()
    metadata = db.MetaData()
    test = db.Table('Packages', metadata, autoload_with=pool)
    query = db.select(test) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    print(test.columns)
    print(ResultSet)


