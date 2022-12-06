from typing import Any

import pandas
from pandas import DataFrame
from web_app.utils.logger import Logger
from web_app.core import MySQL_DB
from datetime import datetime
import warnings


# Ignore warnings because we are professionals
warnings.filterwarnings('ignore')

class RobotData():
    """
    Returns connection to work with data from live_data in the robot database.
    """
    logger = Logger(__name__)
    
    known_types = {
        "int": int,
        "varchar": str,
        "float": float,
        "datetime": datetime,
        "tinyint": bool
    }
    
    def __init__(self) -> None:
        """ 
        Constructs necessary atributes for Robot_DB object.
        """
        self.db = MySQL_DB(host="localhost", 
                           user="omron", 
                           password="Auto_Team123!", 
                           database="robots")
        
    def robot_list(self) -> list:
        """
        Returns data from the robot_list table, returns exception if error

        Returns:
            list: Names of all robots
        """
        return DataFrame(self.db.select("SELECT * FROM robot_list"))['name'].to_list()
        
    def live_data(self, name: str=None, column: str="*") -> pandas.DataFrame:
        """
        Returns data from the live_data table, can specify by bot name and column,
        returns exception if error.

        Args:
            name (str, optional): Name of bot. Defaults to None.
            column (str, optional): Name of desired column, Defaults to None.

        Returns:
            pandas.DataFrame: Representation of data from live_data
        """
        sql = f"SELECT {column} FROM live_data"
        params = {"name": name}
        
        if name: 
            sql += " WHERE name = %(name)s"
            
        result = self.db.select(sql, params)
        if isinstance(result, Exception):
            return result
                
        return DataFrame(result)
    
    def live_data_update(self, name: str, data: dict) -> None:
        """
        Updates column data in the live_data table, returns exception if error

        Args:
            name (str): Name of bot.
            value (dict): New value(s)
        """
        for key, value in data.items():
            try:
                # FIXME type validation
                # assert valid.live_data_column(key), "Invalid column."
                sql = f"""UPDATE live_data 
                          SET {key} = %(value)s 
                          WHERE name = %(name)s;"""
                error = self.db.update(sql, {"value": value, "name": name})
                assert not error, error
                
            except Exception as x:
                error = "Unable to update live_data: " + str(x)
                self.logger.error(error)
                return Exception(error)
            
    def live_data_columns(self) -> list:
        """Returns list of column names from the live_data table
        
        Returns:
            list: Column names as strings
        """
        # TODO - convert column names to robot class friendly names
        # return self.select("SHOW COLUMNS FROM live_data")['Field'].to_list()
        return ["disabled", "offline", "stuck", "current_location", "displaying", 
                "next_location", "updated_at", "low_battery", "lot_list", "distance",
                "y_coord", "x_coord", "button_pressed", "status", "battery"]
    
    def live_data_column_types(self, column: str=None) -> dict:
        """Returns a dict of columns and their data types

        Args:
            column (str): Optional. Specify column to get data type of

        Returns:
            dict: Keys are column names, values are data types
        """
        sql = """SELECT COLUMN_NAME, DATA_TYPE 
                 FROM INFORMATION_SCHEMA.COLUMNS 
                 WHERE table_schema = 'robots' 
                 AND table_name = 'live_data'"""
        params = {"column": column}
        
        if column is not None:
            sql = sql + "AND COLUMN_NAME = %(column)s"
        
        df = DataFrame(self.db.select(sql, params))
        
        data = {}
        for row in df.iterrows():
            data[row[1][0]] = self.known_types[row[1][1]]
            
        return data
    
    def metrics(self, start: datetime=datetime(2022,6,1), end: datetime=datetime.now()) -> pandas.DataFrame:
        """
        Returns a dataframe of all metric data or data between dates if specified

        Args:
            start (datetime, optional): Start date parameter, inclusive. Defaults to start of collection.
            end (datetime, optional): End data parameter, inclusive. Defaults to now.

        Returns:
            pandas.DataFrame: Dataframe with selected data.
        """
        sql = """SELECT * FROM metrics
                 WHERE fromTime BETWEEN %(start)s AND %(end)s"""
                 
        df = DataFrame(self.db.select(sql, params={"start": start, "end": end}))
        return df