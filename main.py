from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import time
from devicesDB import DevicesDB
from IPdevice import IPDevice

class wifiDeviceAnalyzer:


    #constructor
    def __init__(self):
        self.db_name = 'wifi_devices.db'
        self.table_name = 'DEVICES'

        with open('secrets.json') as f:
            data = json.load(f)

        url = data['ziggo_ip']
        username = data['username']
        pw = data['password']

        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("window-size=1920,1080") 
        driver = webdriver.Firefox(options = opts)
        driver.get('http://' + url)
        time.sleep(2)

        html_user = driver.find_element_by_id('Userbane')
        html_pw = driver.find_element_by_id('Password')
        html_continue_button = driver.find_element_by_class_name('button_main')

        html_user.send_keys(username)
        html_pw.send_keys(pw)
        html_continue_button.click()

        driver.get('http://' + url + '/LandConnectedDevices.asp')
        time.sleep(2)

        html_devices_container = driver.find_element_by_class_name('data-tables')
        html_devices = html_devices_container.find_elements_by_tag_name('tr')

        db_connection = DevicesDB(db_name=self.db_name, table_name=self.table_name)
        db_connection.create_devices_table()


        for html_device in html_devices[1::]: #Skipping table header
            # print(html_device.text)
            device_name, device_mac, device_ip = html_device.text.split(' ')[0:3]
            device = IPDevice(device_name, device_mac, device_ip)
            active_check = device.is_active()
            print(f'insert device {html_device.text} into db')
            db_connection.insert_device(device)
            if active_check:
                print(f'device {device.name} with ip {device.ip} is active')
            else:
                print('.')

        time.sleep(5)
        driver.close()


if __name__ == '__main__':
    while True:
        wifiDeviceAnalyzer()
        time.sleep(900)
