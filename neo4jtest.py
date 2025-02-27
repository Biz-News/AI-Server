from neo4j import GraphDatabase
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

class Neo4jHandler:
    def __init__(self):
        uri = "bolt://13.124.216.60:7687"
        username = "neo4j"
        password = "123456789"
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
    def close(self):
        self.driver.close()
    def run_query(self, query_list, parameters_list):
        with self.driver.session() as session:
            for i in range(len(query_list)):
                query = query_list[i]
                parameters = parameters_list[i]
                session.run(query, parameters)

class MySQLHandler:
    def __init__(self):
        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        name = os.getenv("DB_NAME")
        host = os.getenv("DB_HOST")
        db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": name,
        }
        self.cnx = mysql.connector.connect(**db_config)
        self.cursor = self.cnx.cursor()
    def query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return pd.DataFrame(result)
    def close(self):
        self.cursor.close()
        self.cnx.close()

if __name__ == "__main__":
    neo4j_handler = Neo4jHandler()
    mysql_handler = MySQLHandler()
    print(neo4j_handler)
    print(mysql_handler)
