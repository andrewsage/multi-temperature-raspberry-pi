# Multiple Temperature Sensors

This simple project was put together to observe the temperature difference between the floor and desk level in my home office.

It reads the temperature and humidity sensors every 10 seconds and logs the readings to a file called `temp_log.csv`.

# Hardware

The system this software is written for is as follows:

* Raspberry Pi 3 running Raspbian 10.3 (buster)
* I2C 16x2 LCD - https://wiki.52pi.com/index.php?title=1602_Serial_LCD_Module_Display_SKU:Z-0234
* 2 x DHT 11 Temperature / Humidity sensors

# Software requirements

The software is written in Python3.

## DHT (Temperature / Humidity) sensor drivers

The DHT uses adafruit drivers and can be installed using the following:

```
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2
```

# Running 

To start it running (and be able to close the terminal and leave it running):

```
nohup ./multi_temp.py &
```

To stop it running in the background:

```
ps ax | grep multi_temp.py
kill PID
```

# Graphing the readings

![sample graph showing both sensors](images/sample_graph.png)


Running

```
python3 graph.py
```

will generate a set of graphs and save them as a file called `temp.png`.

## Graph requirements

In order for the graphing to work the following needs to be installed:

```
sudo pip3 install pandas
sudo pip3 install matplotlib
sudo apt-get install libatlas3-base
sudo pip3 install seaborn
```
