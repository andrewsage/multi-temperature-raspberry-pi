#!/usr/bin/env python3

import os
import time
import board
import adafruit_dht
from time import sleep
from datetime import datetime
import I2C_LCD_driver
import database_driver

dbname = 'sensorsData.db'
db = database_driver.database(dbname)

lcd = I2C_LCD_driver.lcd()

sensorFloor = 1
sensorDesk = 2

# Initial the dht device, with data pin connected to:
dhtLowerDevice = adafruit_dht.DHT11(board.D16)
dhtUpperDevice = adafruit_dht.DHT11(board.D18)

# save the data to the database
def logData(timestamp, sensor, temperature, humidity):
    db.execute_query("INSERT INTO DHT_data values((?), (?), (?), (?))", (timestamp, sensor, temperature, humidity))

while True:
    try:
        now = datetime.now()
        # Print the values to the serial port
        temperature_lower = dhtLowerDevice.temperature
        humidity_lower = dhtLowerDevice.humidity
        temperature_upper = dhtUpperDevice.temperature
        humidity_upper = dhtUpperDevice.humidity
        logData(now, sensorFloor, temperature_lower, humidity_lower)
        logData(now, sensorDesk, temperature_upper, humidity_upper)
        lcd.lcd_display_string("F:{:.1f} D:{:.1f}".format(temperature_lower, temperature_upper), 1)
        lcd.lcd_display_string("F:{}% D:{}%".format(humidity_lower, humidity_upper), 2)
        print("Temp Floor: {:.1f} C    Temp Desk: {:.1f} C    Humidity Floor: {}%     Humidity Desk: {}% "
              .format(temperature_lower, temperature_upper, humidity_lower, humidity_upper))

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

    except OverflowError as error:
        print(error.args[0])

    time.sleep(10.0)

