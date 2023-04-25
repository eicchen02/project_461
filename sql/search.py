"""
Name: Elijah Klein
    Date of Last Edit: 4/20/2023

    Purpose: Back End for Search Function in web api
    Details: checkTitle searches the repo title via native re regex package
        checkRM searches the according readMe for the given name
"""
import re
import sys

import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector
from sql_header import *


def checkInput(input_term, search_term):
    if re.search(
        search_term.lower(), input_term.lower()
    ):  # Check the Repo Name contains the name via re regex package
        return 1
    return 0


def main():
    search_term = sys.argv[1]

    foundNames = []
    # interact with Cloud SQL database using connection pool
    with pool.connect() as db_conn:
        # query database
        t = sqlalchemy.text("SELECT * FROM Packages")
        result = db_conn.execute(t)
        # Do something with the results
        for row in result:
            if checkInput(row[0],  search_term) or checkInput(row[1],  search_term) or checkInput(row[9], search_term):
                foundNames.append(1)
            else:
                foundNames.append(0)

    print(foundNames)
    return foundNames

main()
