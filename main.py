# main.py
# Description: TBD
# Author: Marcin Kaminski

import mysql.connector # Importing the mysql.connector module to establish a connection to the MySQL database
import dbconfig as cfg # Importing the dbconfig module to access the database configuration parameters defined in dbconfig.py
from neo4j import GraphDatabase # Importing the GraphDatabase class from the neo4j module to establish a connection to the Neo4j database


# DATABASE CONNECTIONS

db = mysql.connector.connect(**cfg.mysql) # Unpacking the mysql dictionary from dbconfig.py to create a connection

driver = GraphDatabase.driver(
    cfg.NEO4J_URI,
    auth=(cfg.NEO4J_USER, cfg.NEO4J_PASSWORD)
) # Creating a driver instance to connect to the Neo4j database using the URI and authentication credentials from dbconfig.py


 





if __name__ == "__main__": # Checking if the script is being run directly (as the main program) rather than imported as a module
    print("To be continued...")