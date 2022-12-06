import json
from flask import Blueprint, jsonify, request
from web_app.model import Robot
from web_app.utils import Logger, RobotData
import ast

logger = Logger(__name__)

data_bp = Blueprint("data", __name__)

@data_bp.route("/data", defaults={"bots": "all", "values": "all"}, methods=["GET"])
@data_bp.route("/data/<bots>", defaults={"values": "all"}, methods=["GET"])
@data_bp.route("/data/<bots>/<values>", methods=["GET", "POST"])
def data(bots: str, values: str) -> None:
    """_summary_

    Args:
        bots (str): _description_
        values (str): _description_

    Returns:
        _type_: _description_
    """
    logger.info("'/data' accessed.")
    db = RobotData()
    
    # Convert bots to a list
    if bots == "all":
        bots = db.robot_list()
    else: 
        bots = bots.split("&")
        bots = [bot.capitalize() for bot in bots]
    
    # Convert values to a list
    if values == "all":
        values = db.live_data_columns()
        # values.remove("id")
    else:
        values = values.split("&")
        
    if request.method == "GET":
        logger.info(f"GETting '{values}' for '{bots}'...")
        # Add requested values to a dictionary
        info = {}
        for bot in bots:
            robot = Robot(bot)
            
            temp = {}
            for value in values:
                temp[value] = getattr(robot, value)
                
            info[bot] = temp
        
        # Return requested data
        logger.info(f"GET returning: '{info}'")
        return info
    
    if request.method == "POST":
        logger.info(f"POSTing '{values}' for '{bots}'...")
        status = {}
        for bot in bots:
            robot = Robot(bot)
            for column in request.form.keys():
                # Convert json into correct typing when possible
                try:
                    value = ast.literal_eval(request.form[column])
                except:
                    value = request.form[column]
                
                # Attempt to update robot
                try:
                    setattr(robot, column, value)
                    status[column] = "write success"
                except Exception as x:
                    status[column] = "write failed: " + repr(x)
                    
        logger.info(f"POST Status: '{status}'")
        return json.dumps(status)
                
            
    
    
