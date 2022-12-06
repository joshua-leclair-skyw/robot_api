from typing import Any
import pandas
from datetime import datetime, timedelta
from web_app.utils import Logger, RobotData


class Metrics():
    def __init__(self, start: datetime, end: datetime) -> None:
        self.logger = Logger(__name__)
        
        db = RobotData()
        self.data = db.metrics(start=start, end=end)

    