from selenium import webdriver
from selenium.webdriver.common.by import By
import os

base_dir = os.path.dirname(os.path.abspath(
    __file__))  # get the current directory
download_dir = base_dir + "\\data"

options = webdriver.FirefoxOptions()
options.page_load_strategy = 'eager'  # "eager" for faster loading
options.set_preference("media.navigator.streams.fake", True)
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", download_dir)
options.set_preference(
    "browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
# prefs = {"download.default_directory": download_dir}
# options.add_experimental_option("prefs", prefs)
browser = webdriver.Firefox(options=options)
browser.get("https://www.messenger.com/login/")
