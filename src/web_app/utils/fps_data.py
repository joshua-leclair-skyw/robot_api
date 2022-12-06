from web_app.core import Oracle_DB
from web_app.utils.logger import Logger
import pandas


class FPS_Data():
    """
    Interface to work with data from the FPS database.
    """
    logger = Logger(__name__)
    
    def __init__(self) -> None:
        """ 
        Returns connection object to Oracle FPS DB for interaction.
        """
        try:
            self.db = Oracle_DB(user="FPSADMIN",
                                password="F%$321fps321",
                                dsn="skyw-oracle02.skywatertechnology.com/FPSP2.SKYWATERTECHNOLOGY.COM")
            assert not isinstance(self.db.conn, Exception), str(self.db)
            
            self.logger.info("Connected to FPS Production 2.")
            
        except Exception as x:
            self.logger.info("Unable to connect to Prod 2: " + str(x))
            
            self.db = Oracle_DB(user="FPSADMIN",
                                password="F%$321fps321",
                                dsn="skyw-oracle01.skywatertechnology.com/FPSP1.SKYWATERTECHNOLOGY.COM")
            assert not isinstance(self.db.conn, Exception), "FPS connection failed: " + str(self.db)
            
            self.logger.info("Connected to FPS Production 1.")
    
    def current_shift(self) -> list:
        """Retrieves time span and letter of current shift from CAL_SHIFTS
        
        Returns:
            list: [pandas.Timestamp: Start time,
                   pandas.Timestamp: End time,
                   str: Shift letter]
        """
        df = self.db.select("""SELECT START_SHIFT, END_SHIFT, WORK_GROUP 
                            FROM CAL_SHIFTS 
                            WHERE SYSDATE BETWEEN START_SHIFT AND END_SHIFT
                            ORDER BY START_SHIFT Desc""")
        
        return df
        
