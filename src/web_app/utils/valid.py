from typing import Any
from web_app.utils import RobotData


def name(name: str) -> bool:
    """
    Validates name of robot.

    Args:
        name (str): Name of bot

    Returns:
        bool: True if valid, false if invalid
    """
    # Get robot list from database
    db = RobotData()
    robots = db.robot_list()

    # Return true if passed name exists in list
    if name in robots:
        return True

    # Otherwise return False
    return False

def live_data_column(column: str) -> bool:
    """
    Validates live_data column name.

    Args:
        column (str): Name of column

    Returns:
        bool: True if valid, false if invalid
    """
    # Get column list from database
    db = RobotData()
    columns = db.live_data_columns()
    
    # Return true if passed name exists in list
    if column in columns:
        return True

    # Otherwise return False
    return False

def live_data_column_value(column: str, value: Any) -> bool:
    """
    Validates live_data column value.

    Args:
        column (str): Name of column
        value (Any): New value of column

    Returns:
        bool: True if valid, false if invalid
    """
    # Get column typing dictionary from database
    db = RobotData()
    column_data = db.live_data_column_types()
    
    # Return true if passed value is correct type for passed column
    if column in column_data.keys():
        # TODO - support multiple types, like bool and int
        if isinstance(value, column_data[column]):
            return True

    # Otherwise return False
    return False