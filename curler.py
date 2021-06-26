#!/usr/bin/env python
from selenium import webdriver
import socket
import time
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("prefs", {
  "download.default_directory": "/tmp",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
})
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=options)
time.sleep(3)
# Can't use localhost here as the remote docker cannot see it
driver.get('http://' + get_ip() + ':8888/chart.html');