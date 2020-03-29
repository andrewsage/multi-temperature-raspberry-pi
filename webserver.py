#!/usr/bin/env python3

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mpl_dates
import io
from flask import Flask, render_template, send_file, make_response, request
import datetime
import database_driver
import pandas as pd
import configparser, os

app = Flask(__name__)
dbname = 'sensorsData.db'
db = database_driver.database(dbname)

def getDHTData(sensor):
	rows = db.select('SELECT * FROM DHT_data WHERE sensor=:sensor ORDER BY timestamp DESC LIMIT 1', {"sensor": sensor})
	if len(rows) > 0:
		for row in rows:
			time = str(row[0])
			temperature = row[1]
			humidity = row[2]
		return time, temperature, humidity
	else:
		raise Exception("No DHT data has been logged yet")

def getHistoricalDHTData(sensor):
	rows = db.select('SELECT * FROM DHT_data WHERE sensor=:sensor ORDER BY timestamp', {"sensor": sensor})
	dates = []
	temperatures = []
	humidities = []
	for row in reversed(rows):
		dates.append(row[0])
		temperatures.append(row[1])
		humidities.append(row[2])

	return dates, temperatures, humidities

@app.route('/')
# main route
def index():
	dht_time1 = ""
	temperature1= 0
	humidity1= 0

	dht_time2 = ""
	temperature2= 0
	humidity2= 0
	try:
		dht_time1, temperature1, humidity1 = getDHTData(1)
	except Exception as e:
		print(e)

	try:
		dht_time2, temperature2, humidity2 = getDHTData(2)
	except Exception as e:
		print(e)

	templateData = {
		'dht_time1' : dht_time1,
		'temperature1' : temperature1,
		'humidity1' : humidity1,
		'dht_time2' : dht_time2,
		'temperature2' : temperature2,
		'humidity2' : humidity2
	}
	return render_template('index.html', **templateData)

@app.route('/graphs')
# main route
def graphs():
	return render_template('graphs.html')

@app.route('/plot/temperature')
def plot_temperature():
	con = db.create_connection()
	df = pd.read_sql_query('SELECT timestamp, temp FROM DHT_data ORDER BY timestamp', con, parse_dates=['timestamp'], index_col=['timestamp'])
	con.close()

	resampled = df.resample('10T').mean()

	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.plot(resampled.index.values, resampled['temp'])
	date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
	axis.xaxis_date()
	axis.xaxis.set_major_formatter(date_format)

	axis.set_xlabel('Time')
	axis.set_ylabel('Temperature ($^\circ$C)')
	axis.set_title('Temperature PGU')
	axis.grid(True)

	fig.autofmt_xdate()
	fig.tight_layout()

	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/humidity')
def plot_humidity():
	con = db.create_connection()
	df = pd.read_sql_query('SELECT timestamp, hum FROM DHT_data ORDER BY timestamp', con, parse_dates=['timestamp'], index_col=['timestamp'])
	con.close()

	resampled = df.resample('10T').mean()

	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.plot(resampled.index.values, resampled['hum'])
	date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
	axis.xaxis_date()
	axis.xaxis.set_major_formatter(date_format)

	axis.set_xlabel('Time')
	axis.set_ylabel('Humidity (%)')
	axis.set_title('Humidity PGU')
	axis.grid(True)

	fig.autofmt_xdate()
	fig.tight_layout()

	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/moisture')
def plot_moisture():
	con = db.create_connection()
	df = pd.read_sql_query('SELECT timestamp, value FROM Moisture_data ORDER BY timestamp', con, parse_dates=['timestamp'], index_col=['timestamp'])
	con.close()

	df['percentage'] = df.apply(scaleMoistureCapacitance, axis=1)

	resampled = df.resample('1T').mean()

	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.plot(resampled.index.values, resampled['percentage'])
	date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
	axis.xaxis_date()
	axis.xaxis.set_major_formatter(date_format)

	axis.set_xlabel('Time')
	axis.set_ylabel('Moisture (%)')
	axis.set_title('Moisture % PGU')
	axis.grid(True)

	fig.autofmt_xdate()
	fig.tight_layout()

	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/csv/dht')
def csv_dht():
	con = db.create_connection()
	df = pd.read_sql_query('SELECT * FROM DHT_data ORDER BY timestamp', con, parse_dates=['timestamp'], index_col=['timestamp'])
	con.close()

	response = make_response(df.to_csv())
	response.headers["Content-Disposition"] = "attachment; filename=dht.csv"
	response.headers["Content-Type"] = "text/csv"
	return response

if __name__ == '__main__':
	app.run(debug=True, port=80, host='0.0.0.0')