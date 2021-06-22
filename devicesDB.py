import sqlite3
from datetime import datetime
import os
from IPdevice import IPDevice

class DevicesDB:
    #constructor
    def __init__(self, db_name, table_name, db_folder='databases') -> None:
        self.db_folder = db_folder
        self.db_name = db_name
        self.table_name = table_name
        self.devices = []
        self.connection = None
        self.cursor = None

    def start_db_connection(self):
        self.connection = sqlite3.connect(os.path.join(self.db_folder, self.db_name))
        self.cursor = self.connection.cursor()

    def create_devices_table(self):
        self.start_db_connection() if not self.connection else 0
        qry = '''CREATE TABLE IF NOT EXISTS {}
             ([id] BIGINT PRIMARY KEY,
              [device_name] VARCHAR(30),
              [device_mac] VARCHAR(30),
              [device_ip] VARCHAR(30),
              [device_status] TINYINT,
              [date_created] DATETIME,
              [date_modified] DATETIME);'''.format(self.table_name)
        self.cursor.execute(qry)
        self.connection.commit()

    def clean_table(self):
        self.start_db_connection() if not self.connection else 0
        qry = '''DROP TABLE IF EXISTS {}'''.format(self.table_name)
        self.cursor.execute(qry)
        self.connection.commit()
        print('***Table is cleaned***')

    def insert_device(self, device):
        self.start_db_connection() if not self.connection else 0
        insert_date = datetime.now()
        device_id = str(device.ip) + str(insert_date.isocalendar()[0]) + str(insert_date.isocalendar()[1]) + str(insert_date.isocalendar()[2])
        try:
            qry = '''INSERT OR IGNORE INTO {0} (id, device_name, device_mac, device_ip, device_status, date_created, date_modified) 
            VALUES ('{1}', "{2}", "{3}", "{4}",{5}, '{6}', '{7}');'''.format(self.table_name, device_id, device.name, device.mac, device.ip, device.active, insert_date, insert_date)
            self.cursor.execute(qry)
            self.connection.commit()
        except:
            print(qry)
            raise

    def update_device(self, product):
        insert_date = datetime.now()
        qry = '''UPDATE {0} SET date_modified =  '{1}' 
        WHERE device_name = '{2}' AND device_mac = '{3}' AND device_ip = '{4}';'''.format(self.table_name, insert_date, device.name, device.mac, device.ip)
        self.cursor.execute(qry)
        self.connection.commit()

    def get_all_devices(self):
        self.start_db_connection() if not self.connection else 0
        qry = '''SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{0}';'''.format(self.table_name)
        run_query = self.cursor.execute(qry).fetchall()

        if (run_query[0][0]):
            qry = '''SELECT device_name, device_mac, device_ip FROM {} ORDER BY date_modified DESC'''.format(self.table_name)
            self.products = self.cursor.execute(qry).fetchall() 
        return self.products

    def get_all_product_ips(self):
        self.start_db_connection() if not self.connection else 0
        self.get_all_devices()
        product_ids = [pid[2] for pid in self.products]
        return product_ids

if __name__== "__main__":
    db = ProductsDB('test.db', 'test_table')