import cx_Oracle
import warnings
from web_app.utils.logger import Logger


# Ignore warnings because we are professionals
warnings.filterwarnings('ignore')

class Oracle_DB():
    """
    Connection to Oracle database.

    Functions
    ---------
    select(sql, params=None):
        Attempts to select data from the robot database with the given SQL query, returns exception if error.
        
    """
    logger = Logger(__name__)
    
    def __init__(self, user:str, password:str, dsn:str) -> None:
        """ 
        Constructs necessary atributes for Oracle_DB object.
        """
        self.conn = self.__oracle_connection(user, password, dsn)
 
    def __oracle_connection(self, user:str, password:str, dsn:str) -> cx_Oracle.Connection:
        """
        (Private) Returns connection to the  Oracle database or exception if error.
        """
        try:
            connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            self.logger.info("Successful Oracle connection.")
            
            return connection

        except Exception as x:
            error = "Unable to connect to Oracle database: " + str(x)
            self.logger.error(error)
            return Exception(error)
        
    def select(self, sql: str, params: dict=None) -> "list[tuple]":
        """
        Attempts to select data from Oracle database with the given SQL query,
        returns exception if error.

        Args:
            sql (str): SQL select query.
            params (dict, optional): Any parameters needed for the SQL query. Defaults to None.

        Returns:
            list[tuple]: List of tuples with selected data.
        """
        # Attempts to query db
        try:
            self.logger.info("Selecting from Oracle database.")
            self.logger.debug("SQL: " + sql)
            self.logger.debug("Parameters: " + str(params))
            
            with self.conn.cursor() as cursor: 
                cursor.execute(sql)
                result = cursor.fetchall()
                
            return result
        
        # Returns exception if fail
        except Exception as x:
            error = "Unable to select: " + str(x)
            self.logger.error(error)
            return Exception(error)
        
