from typing import Any
import pandas
from web_app.utils import Logger, RobotData, valid


class Robot():
    """
    Class representation of a robots live data

    Attributes
    ----------
    name : str
        Name of robot
        
    battery : float 
        Battery percentage of robot
        
    status : str 
        Mode status of the robot
        
    button_pressed : bool 
        Whether the send button has been pressed
        
    x_coord : float 
        X coordinate of the bots location in mobile planner
        
    y_coord : float 
        Y coordinate of the bots location in mobile planner
        
    distance : float 
        Distance in mm from the robots goal
        
    lot_list : list 
        List of lots on the robot
        
    low_battery : float 
        Percentage at which the robot enters low battery mode
        
    updated_at : pandas.Timestamp 
        Time of the last data update
        
    next_location : str 
        Robots calculated next location
        
    displaying : str 
        What is currently being displayed on the robots screen
        
    current_location : str 
        Robots current location in the fab
        
    stuck : bool 
        Whether the robot is stuck
        
    offline : bool 
        Whether the robot is offline or disconnected from internet
        
    disabled : bool 
        Whether the robot has been disabled
            
    Functions
    ---------
    refresh():
        Refreshes old robot data with live data
    
    """
    def __init__(self, name: str) -> None:
        """
        Constructs all necessary attributes for the Robot object.

        Args:
            name (str): Name of the robot, used when querying MySQL
        """
        # Validate name
        assert valid.name(name), "Invalid robot name: " + name
        self.name = name.capitalize()
        
        # Instance Variables
        self.__logger = Logger(__name__)
        # TODO - logging
        self.__db = RobotData()
        
    @property
    def battery(self) -> float:
        return self.__get_db_value("battery")
    
    @battery.setter
    def battery(self, value):
        self.__set_db_value("battery", value)
        
    @property
    def status(self) -> str:
        return self.__get_db_value("status")
    
    @status.setter
    def status(self, value):
        self.__set_db_value("status", value)

    @property
    def button_pressed(self) -> bool:
        return bool(self.__get_db_value("buttonPressed"))
    
    @button_pressed.setter
    def button_pressed(self, value) -> None:
        self.__set_db_value("buttonPressed", value)

    @property
    def x_coord(self) -> float:
        return self.__get_db_value("xCoord")
    
    @x_coord.setter
    def x_coord(self, value) -> None:
        self.__set_db_value("xCoord", value)

    @property
    def y_coord(self) -> float:
        return self.__get_db_value("yCoord")
    
    @y_coord.setter
    def y_coord(self, value) -> None:
        self.__set_db_value("yCoord", value)

    @property
    def distance(self) -> float:
        return self.__get_db_value("distance")
    
    @distance.setter
    def distance(self, value) -> None:
        self.__set_db_value("distance", value)

    @property
    def lot_list(self) -> list:
        return self.__get_db_value("lotList")
    
    @lot_list.setter
    def lot_list(self, value) -> None:
        self.__set_db_value("lotList", value)

    @property
    def low_battery(self) -> float:
        return self.__get_db_value("lowBatteryThreshold")
    
    @low_battery.setter
    def low_battery(self, value) -> None:
        self.__set_db_value("lowBatteryThreshold", value)

    @property
    def updated_at(self) -> pandas.Timestamp:
        return self.__get_db_value("updatedAt")
    
    @updated_at.setter
    def updated_at(self, value) -> None:
        self.__set_db_value("updatedAt", value)

    @property
    def next_location(self) -> str:
        return self.__get_db_value("nextLocation")
    
    @next_location.setter
    def next_location(self, value):
        self.__set_db_value("nextLocation", value) 
    
    @property
    def displaying(self) -> str:
        return self.__get_db_value("displaying")
    
    @displaying.setter
    def displaying(self, value):
        self.__set_db_value("displaying", value) 
    
    @property
    def current_location(self) -> str:
        return self.__get_db_value("currentLocation")
    
    @current_location.setter
    def current_location(self, value):
        self.__set_db_value("currentLocation", value) 
    
    @property
    def stuck(self) -> bool:
        return bool(self.__get_db_value("stuck"))
    
    @stuck.setter
    def stuck(self, value):
        self.__set_db_value("stuck", value) 
    
    @property
    def offline(self) -> bool:
        return bool(self.__get_db_value("offline"))
    
    @offline.setter
    def offline(self, value):
        self.__set_db_value("offline", value)    
    
    @property
    def disabled(self) -> bool:
        return bool(self.__get_db_value("disabled"))
    
    @disabled.setter
    def disabled(self, value):
        self.__set_db_value("disabled", value)
    
    def __get_db_value(self, column: str) -> Any:
        """
        (Private) Gets value of column from live_data.

        Args:
            column (str): Live_data column name.

        Returns:
            Any: Whatever the value is in the database.
        """
        # Attempt to get column data from live_data
        self.__logger.info(f"Getting {column} data...")
        data = self.__db.live_data(self.name, column).loc[0][column]
        self.__logger.info(f"Recieved: {data}")
        assert not isinstance(data, Exception), "Failed to get value: " + str(data) 
        
        # Return value
        return data
    
    def __set_db_value(self, column: str, value: Any) -> None:
        """
        (Private) Sets value of column in live_data.

        Args:
            column (str): Live_data column name.
            value (Any): New value of column.
        """
        # Validate new value
        self.__logger.info(f"Validating new {column} value: '{value}'")
        assert valid.live_data_column_value(column, value), f"Invalid {column} typing: {type(value)}"
        
        # Attempt to set column data in live_data
        self.__logger.info(f"Setting new value for {column}...")
        error = self.__db.live_data_update(self.name, {column: value})
        self.__logger.info(f"Error?: {error}")
        assert not error, "Failed to set value: " + str(error)
        