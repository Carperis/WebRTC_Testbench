import os
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import xlrd

caller_xpath = "/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/a"
call_btn_xpath = "/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[1]/span/div"


def main():
    # login studentlink class planner Fall 2022
    # myusername = input("Enter username: ")
    # mypassword = input("Enter password: ")
    myusername = "kutousam@gmail.com"
    mypassword = "QPSam15982818"

    # see https://stackoverflow.com/questions/43734797/page-load-strategy-for-chrome-driver-updated-till-selenium-v3-12-0
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'

    # see https://stackoverflow.com/questions/38832776/how-do-i-allow-chrome-to-use-my-microphone-programmatically
    # and https://stackoverflow.com/questions/39381088/selenium-python-chrome-open-with-def-options
    options.add_argument("use-fake-device-for-media-stream")
    options.add_argument("use-fake-ui-for-media-stream")

    browser = webdriver.Chrome(options=options)

    # # see https://stackoverflow.com/questions/61308799/unable-to-locate-elements-in-selenium-python
    # browser.get("https://www.messenger.com/login/")
    # browser.find_element(By.ID, "email").send_keys(myusername)
    # browser.find_element(By.ID, "pass").send_keys(mypassword)
    # browser.find_element(By.ID, "loginbutton").click()

    # # see https://www.testclass.cn/selenium_iframe.html
    # print("The caller is loading...")
    # while(not hasElement(browser, caller_xpath)):
    #     pass
    # print("The caller is loaded.")
    # browser.find_element(By.XPATH, caller_xpath).click()
    # print("Start calling...")
    # browser.find_element(By.XPATH, call_btn_xpath).click()
    # print("Waiting for the call to be answered...")

    # if q is pressed, quit
    while(True):
        if(input() == 'q'):
            break

    clear()

    browser.quit()


def clear():  # clear screen
    os.system('cls')  # for windows
    os.system('clear')  # for mac/linux


def hasElement(browser, xpath):
    try:
        browser.find_element(By.XPATH, xpath)
    except:
        return False
    return True


if __name__ == "__main__":
    # calculate run time
    start = time.time()
    main()
    end = time.time()
    print("Run time: ", end - start)
