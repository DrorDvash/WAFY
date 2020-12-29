from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import attack_xss
import attack_csrf
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"

def main():

    driver, target_url = init()

    #search = driver.find_element_by_id("bug")
    #print(search.text)

    time.sleep(5)
    driver.quit()

def init():
    print("[+] Initializing")
    driver = webdriver.Chrome(PATH)

    # Import data about the target (url, username, password)
    with open("secret.txt") as file:
        target_url, username, password = file.read().splitlines()

    # Make a login
    driver.get(target_url)
    element = driver.find_element_by_id("login")
    element.clear()
    element.send_keys(username)
    element = driver.find_element_by_id("password")
    element.clear()
    element.send_keys(password, Keys.RETURN)

    return driver, target_url

def xss_attacks(driver, target_url):
    driver.get(target_url)


if __name__ == '__main__':
    main()
