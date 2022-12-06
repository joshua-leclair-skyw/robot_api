import json
from flask import Blueprint, jsonify, request
from web_app.model import Robot
from web_app.utils import Logger, RobotData
import ast

logger = Logger(__name__)

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.route("/metrics")
def metrics():
    pass