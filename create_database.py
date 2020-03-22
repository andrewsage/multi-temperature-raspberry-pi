import database_driver

dbname = 'sensorsData.db'
db = database_driver.database(dbname)
 
if __name__ == '__main__':

    sql_create_dht_table = "CREATE TABLE IF NOT EXISTS DHT_data (timestamp DATETIME, sensor NUMERIC, temperature NUMERIC, humidity NUMERIC);"

    try:
        db.create_table(sql_create_dht_table)
    except Error as e:
        print(e)