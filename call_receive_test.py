import os
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

receive_btn_xpath = "/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[1]/div/div"
download_btn_xpath1 = "/html/body/p/details/summary"
download_btn_xpath2 = "/html/body/p/details/div/div[1]/a/button"
caller_icon_xpath = "/html/body/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[1]/div/img"
end_call_btn_xpath = "/html/body/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/div/div[2]/div[5]/span/div/div/div"
recall_btn_xpath = "/html/body/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/button"


def main():
    # check if password_caller.txt exists. if exists, read username and password from it
    if os.path.exists("password_receiver.txt"):
        with open("password_receiver.txt", "r") as f:
            myusername = f.readline()
            mypassword = f.readline()
        if len(myusername) == 0 or len(mypassword) == 0:
            print("Error: password_receiver.txt is not in the correct format.")
            return
    # if not, ask user to input username and password and save them to password_caller.txt
    else:
        myusername = input("Enter username: ")
        mypassword = input("Enter password: ")
        with open("password_receiver.txt", "w") as f:
            f.write(myusername + "\n")
            f.write(mypassword + "\n")

    # see https://stackoverflow.com/questions/43734797/page-load-strategy-for-chrome-driver-updated-till-selenium-v3-12-0
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager' # for faster loading

    # see https://stackoverflow.com/questions/38832776/how-do-i-allow-chrome-to-use-my-microphone-programmatically
    # and https://stackoverflow.com/questions/39381088/selenium-python-chrome-open-with-def-options
    options.add_argument("use-fake-device-for-media-stream")
    options.add_argument("use-fake-ui-for-media-stream")

    # see https://www.lambdatest.com/blog/download-file-using-selenium-python/
    download_directory = "C:\\Users\\Sam\\Desktop\\WebRTC_Testbench\\downloads"
    prefs = {"download.default_directory": download_directory}
    options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(options=options)

    # see https://stackoverflow.com/questions/61308799/unable-to-locate-elements-in-selenium-python
    browser.get("https://www.messenger.com/login/")

    # see https://stackoverflow.com/questions/44119081/how-do-you-fix-the-element-not-interactable-exception
    browser.implicitly_wait(1)

    browser.find_element(By.ID, "email").send_keys(myusername)
    browser.find_element(By.ID, "pass").send_keys(mypassword)
    browser.find_element(By.ID, "loginbutton").click()
    contacts_window = browser.current_window_handle

    # create a new tab for webrtc-internals and switch to it
    browser.switch_to.new_window('tab')
    browser.get("chrome://webrtc-internals")
    browser.implicitly_wait(1)  # wait for elements to load
    print("webrtc-internals page is loaded.")
    rtc_window = browser.current_window_handle

    browser.switch_to.window(contacts_window)
    # see https://www.testclass.cn/selenium_iframe.html
    print("Waiting for the incoming call...")
    start = time.time()
    while(not hasElement(browser, receive_btn_xpath)):
        end = time.time()
        if((end - start) > 10):
            print("The call is not received for 10 seconds.")
            browser.quit()
            return
    browser.find_element(By.XPATH, receive_btn_xpath).click()
    windows = browser.window_handles
    call_window = windows[2]

    browser.switch_to.window(call_window)
    while(not hasElement(browser, caller_icon_xpath)):  # wait for the call box to be fully loaded
        pass
    print("The call is received.")

    browser.switch_to.window(call_window)
    start = time.time()
    while(True):
        end = time.time()
        print("The call has been connected for " +
              str(end - start) + " seconds.", end="\r")
        # if q is pressed or 10 seconds have passed, quit the program
        hasRecall = hasElement(browser, recall_btn_xpath)
        if(((end - start) > 10) or hasRecall):
            if(not hasRecall):
                browser.find_element(By.XPATH, end_call_btn_xpath).click()
            print("\nThe call is ended.")
            browser.switch_to.window(rtc_window)
            browser.find_element(By.XPATH, download_btn_xpath1).click()
            browser.find_element(By.XPATH, download_btn_xpath2).click()
            sleep(3)  # wait for download to finish
            print("The dump file is downloaded.")
            break

    # clear()
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