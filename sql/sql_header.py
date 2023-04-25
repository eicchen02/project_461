from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy as db


# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "ece461-team25:us-central1:project461-database",
        "pymysql",
        user="root",
        password="SweetCaroline",
        db="test"
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
    test = db.Table('TestData', metadata, autoload_with=pool)
    query = db.select(test) 
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    # print(test.columns.keys())
    print(ResultSet)




