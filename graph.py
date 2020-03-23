#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mpl_dates
import seaborn as sns
import database_driver

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

dbname = 'sensorsData.db'
db = database_driver.database(dbname)

sns.set()

con = db.create_connection()
dfFloor = pd.read_sql_query('SELECT timestamp, temperature, humidity FROM DHT_data WHERE sensor=1 ORDER BY timestamp', con, parse_dates=['timestamp'], index_col=['timestamp'])
dfDesk = pd.read_sql_query('SELECT timestamp, temperature, humidity FROM DHT_data WHERE sensor=2 ORDER BY timestamp', con, parse_dates=['timestamp'], index_col=['timestamp'])
con.close()

resampledFloor = dfFloor.resample('1T').mean()
resampledDesk = dfDesk.resample('1T').mean()

print(dfFloor.info())
print(dfFloor)

print(dfDesk.info())
print(dfDesk)

print(resampledFloor.info())
print(resampledFloor)

print(resampledDesk.info())
print(resampledDesk)

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

ax1.plot(resampledFloor.index.values, resampledFloor['temperature'], label="floor")
ax1.plot(resampledDesk.index.values, resampledDesk['temperature'], label="desk")
date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(date_format)
ax1.legend()

ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature ($^\circ$C)')
ax1.set_title('Temperature at floor vs. desk')

ax2.plot(resampledFloor.index.values, resampledFloor['humidity'], label="floor")
ax2.plot(resampledDesk.index.values, resampledDesk['humidity'], label="desk")
ax2.xaxis_date()
ax2.xaxis.set_major_formatter(date_format)

ax2.set_xlabel('Time')
ax2.set_ylabel('Humidity (%)')
ax2.set_title('Humidity at floor vs. desk')
ax2.legend()

ax3.plot(resampledFloor.index.values, resampledDesk['temperature'] - resampledFloor['temperature'], label="Difference")
date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
ax3.xaxis_date()
ax3.xaxis.set_major_formatter(date_format)
ax3.legend()

ax3.set_xlabel('Time')
ax3.set_ylabel('Delta ($^\circ$C)')
ax3.set_title('Temperature Difference')

fig.autofmt_xdate()
fig.tight_layout()
fig.savefig('temp.png')