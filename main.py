from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import attack_xss
import attack_csrf
import time
from attack_csrf import csrf_attack

PATH = "C:\Program Files (x86)\chromedriver.exe"

def main():
    blacklisted_values = [0, 1, 33, 46, 67, 72, 91, 102, 114, 119, 132, 136, 137, 149]
    driver, target_url = init()

    #search = driver.find_element_by_id("bug")
    #print(search.text)
    time.sleep(1)

    selector = Select(driver.find_element_by_id('select_portal'))
    options = selector.options

    for index in range(0, len(options) - 1):
        if index not in blacklisted_values:
            selector.select_by_index(index)
            driver.find_element_by_xpath("//button[@name='form']").click()

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


if __name__ == '__main__':
    main()
