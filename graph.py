import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mpl_dates
import seaborn as sns

# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

sns.set()

df = pd.read_csv('temp_log.csv', parse_dates=['Time'], index_col=['Time'], na_values=['999.99'])
resampled = df.resample('1T').mean()

print(df.info())
print(df)

print(resampled.info())
print(resampled)

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

ax1.plot(resampled.index.values, resampled['Temp Floor'], label="floor")
ax1.plot(resampled.index.values, resampled['Temp Desk'], label="desk")
date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(date_format)
ax1.legend()

ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature ($^\circ$C)')
ax1.set_title('Temperature at floor vs. desk')

ax2.plot(resampled.index.values, resampled['Humidity Floor'], label="floor")
ax2.plot(resampled.index.values, resampled['Humidity Desk'], label="desk")
ax2.xaxis_date()
ax2.xaxis.set_major_formatter(date_format)

ax2.set_xlabel('Time')
ax2.set_ylabel('Humidity (%)')
ax2.set_title('Humidity at floor vs. desk')
ax2.legend()

ax3.plot(resampled.index.values, resampled['Temp Desk'] - resampled['Temp Floor'], label="Difference")
date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
ax3.xaxis_date()
ax3.xaxis.set_major_formatter(date_format)
ax3.legend()

ax3.set_xlabel('Time')
ax3.set_ylabel('Delta ($^\circ$C)')
ax3.set_title('Temperature Difference')

fig.autofmt_xdate()
fig.savefig('temp.png')