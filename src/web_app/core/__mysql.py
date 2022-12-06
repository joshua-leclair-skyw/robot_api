import mysql.connector
from mysql.connector import MySQLConnection
from web_app.utils.logger import Logger
from datetime import datetime
import warnings


# Ignore warnings because we are professionals
warnings.filterwarnings('ignore')

class MySQL_DB():
    """
    Connection to MySQL database.
    
    Functions
    ---------
    select(sql, params=None):
        Attempts to select data from the robot database with the given SQL query, returns exception if error.
        
    update(sql):
        Attempts to update the robot data with the given sql query and commits the changes, returns exception if error.
    """
    logger = Logger(__name__)
    
    def __init__(self, host:str, user:str, password:str, database:str) -> None:
        """ 
        Constructs necessary atributes for MySQL_DB object.
        """
        self.conn:MySQLConnection = self.__mysql_connection(host, user, password, database)
            
    def __mysql_connection(self, host:str, user:str, password:str, database:str) -> MySQLConnection:
        """
        (Private) Returns connection to the robot MySQL database or exception if error.
        """
        # Attempts to create and return connection to mysql database
        try:
            self.logger.debug("Creating connection to MySQL.")
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database)
            return connection

        # Returns Exception if fails
        except Exception as x:
            error = "Unable to connect to mysql database: " + str(x)
            self.logger.error(error)
            return Exception(error)
        
    def select(self, sql: str, params: dict=None) -> "list[tuple]":
        """
        Attempts to select data from the robot database with the given SQL query,
        returns exception if error.

        Args:
            sql (str): SQL select query.
            params (dict, optional): Any parameters needed for the SQL query. Defaults to None.

        Returns:
            list[tuple]: List of tuples with selected data.
        """
        # Attempts to query db
        try:
            self.logger.info("Selecting from MySQL database.")
            self.logger.debug("SQL: " + sql)
            self.logger.debug("Parameters: " + str(params))
            
            with self.conn.cursor() as cursor: 
                cursor.execute(sql)
                result = cursor.fetchall()
            
            self.logger.debug("Results: " + str(result))
            return result
                        
        # Returns exception if fail
        except Exception as x:
            error = "Unable to select: " + str(x)
            self.logger.error(error)
            return Exception(error)
        
    def update(self, sql: str, params: dict=None) -> None:
        """
        Attempts to update the robot data with the given sql query
        and commits the changes, returns exception if error.
        
        Args:
            sql (str): SQL update/delete/insert query.
        """
        # Attempts to execute and commit sql
        try:
            self.logger.info("Updating database.")
            self.logger.debug("SQL: " + sql)
            self.logger.debug("Parameters: " + str(params))
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                self.conn.commit()
                
        
        # Returns exception if fail
        except Exception as x:
            error = "Unable to update: " + str(x)
            self.logger.error(error)
            return Exception(error)