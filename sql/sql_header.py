from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy as db
import os

#? Use top block for local testing, Use bottom block for deploying to Cloud Run 
#
#? Works with Whitelisted IP (local)

def connect_tcp_socket() -> db.engine.base.Engine:
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
    return pool

#? Works with Cloud Run

# def connect_tcp_socket() -> db.engine.base.Engine:
#     db_host = '10.65.176.3'  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
#     db_user = os.environ["SQL_USER"]  # e.g. 'my-db-user'
#     db_pass = os.environ["SQL_PASSWORD"]  # e.g. 'my-db-password'
#     db_name = os.environ["SQL_DB"]  # e.g. 'my-database'
#     db_port = 3306  # e.g. 3306

#     pool = db.create_engine(
#         # Equivalent URL:
#         # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
#         db.engine.url.URL.create(
#             drivername="mysql+pymysql",
#             username=db_user,
#             password=db_pass,
#             host=db_host,
#             port=db_port,
#             database=db_name,
#         ),
#         # ...
#     )
#     return pool

pool = connect_tcp_socket()
connection = pool.connect()
metadata = db.MetaData()
table = db.Table('Packages', metadata, autoload_with=pool)

def exists(search_in, search_for):
    #Check if url exists already
    #Return 1 if exists, 0 if not
    query = db.select(table).where(search_in == search_for)
    result = connection.execute(query)
    connection.commit()
    exists = bool(result.fetchone())
    return exists

if __name__ == "__main__":
    pool = connect_tcp_socket()
    connection = pool.connect()
    metadata = db.MetaData()
    table = db.Table('Packages', metadata, autoload_with=pool)
    # query = db.select(table.c.PackageName)
    # query = db.select(table.c["ID", "PackageName", "Version"]).where(table.c.ID == 9)
    # query = db.select(table.c.LastModified).where(table.c.PackageName == "cloudinary_npm")
    query = db.select(table).where(table.c.ID == 9)
    result_row = connection.execute(query)
    result = result_row.fetchone()
    print(table.columns.keys())



