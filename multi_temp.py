#!/usr/bin/python

import os
import time
import board
import adafruit_dht
from time import sleep
from datetime import datetime
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

# Initial the dht device, with data pin connected to:
dhtLowerDevice = adafruit_dht.DHT11(board.D16)
dhtUpperDevice = adafruit_dht.DHT11(board.D18)

file = open("temp_log.csv", "a")
if os.stat("temp_log.csv").st_size == 0:
    file.write("Time,Temp Floor,Temp Desk,Humidity Floor,Humidity Desk\n")

while True:
    try:
        now = datetime.now()
        # Print the values to the serial port
        temperature_lower = dhtLowerDevice.temperature
        humidity_lower = dhtLowerDevice.humidity
        temperature_upper = dhtUpperDevice.temperature
        humidity_upper = dhtUpperDevice.humidity
        mylcd.lcd_clear()
        mylcd.lcd_display_string("F:{:.1f} D:{:.1f}".format(temperature_lower, temperature_upper), 1)
        mylcd.lcd_display_string("F:{}% D:{}%".format(humidity_lower, humidity_upper), 2)
        print("Temp Floor: {:.1f} C    Temp Desk: {:.1f} C    Humidity Floor: {}%     Humidity Desk: {}% "
              .format(temperature_lower, temperature_upper, humidity_lower, humidity_upper))
        file.write("{},{:.1f},{:.1f},{},{}\n"
              .format(now,temperature_lower, temperature_upper, humidity_lower, humidity_upper))
        file.flush()

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])

    except OverflowError as error:
        print(error.args[0])

    time.sleep(2.0)

