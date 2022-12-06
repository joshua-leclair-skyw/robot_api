import json
from flask import Blueprint, jsonify, request
from web_app.model import Robot
from web_app.utils import Logger, RobotData
import ast

logger = Logger(__name__)

logs_bp = Blueprint("logs", __name__)

