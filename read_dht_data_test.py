#!/usr/bin/env python3

import database_driver

dbname = 'sensorsData.db'
db = database_driver.database(dbname)

def getData(sensor):
	rows = db.select('SELECT * FROM DHT_data WHERE sensor=sensor ORDER BY timestamp DESC LIMIT 1')
	print(rows)
	for row in rows:
		print(row)
		time = str(row[0])
		temperature = row[2]
		humidity = row[3]
	return time, temperature, humidity

if __name__ == '__main__':
	getData(1)
	getData(2)