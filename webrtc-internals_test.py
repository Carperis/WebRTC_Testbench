import os
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)
browser.get("chrome://webrtc-internals")
# if q is pressed, quit
while(True):
    if(input() == 'q'):
        break
browser.quit()