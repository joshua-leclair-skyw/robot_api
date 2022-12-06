import pandas
from datetime import datetime
from web_app.utils import RobotData
db = RobotData()

# data = pandas.read_sql("""SELECT column_name, data_type 
#                           FROM information_schema.columns 
#                           WHERE table_schema = 'robots' 
#                           AND table_name = 'live_data';""", 
#                           db.conn)

# print(db.live_data_column_types())

# print(db.live_data_column_types("disabled"))

# data = db.live_data("asd")
# assert not isinstance(data, Exception), data
# cur = db.conn.cursor()
# cur.execute("ALTER TABLE live_data MODIFY buttonPressed TINYINT")
# db.conn.commit()

# print(isinstance(db.live_data_column_types("status")["status"], str))
# print(db.live_data_column_types("status")["status"])

# df = pandas.read_sql("SELECT * FROM metrics", db.conn)
# df = pandas.read_sql("SELECT SUM(waitAvg) FROM metrics WHERE updateType = 'monthly'", db.conn)
# totalTrips, lotsMoved
print(db.live_data_column_types())