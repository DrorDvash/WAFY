from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

def init():
    print("[+] Initializing")
    driver = webdriver.Chrome(PATH)

    # Import data about the target (url, username, password)
    with open("secret.txt") as file:
        target_url, username, password = file.read().splitlines()

    # Login to website
    driver.get(target_url)
    element = driver.find_element_by_id("login")
    element.clear()
    element.send_keys(username)
    element = driver.find_element_by_id("password")
    element.clear()
    element.send_keys(password, Keys.RETURN)
    return driver, target_url

def execute():
    driver, target_url = init() #to delete

    read_all_attacks(driver)

def read_all_attacks(driver):
    attack_type = "Cross-Site Scripting - "
    attacks = {}
    urls = []
    elements = driver.find_elements_by_xpath("//form/select[@name='bug']/option")
    for item in elements:
        if attack_type in item.text:
            # Insert any result into dict {Attack Name:Value}
            attacks[item.text] = item.get_attribute(("value"))

            item.click()
            driver.find_element_by_xpath("//form/button[@type='submit']").click()
            time.sleep(10)
    #print(attacks)
    return attacks

if __name__ == '__main__':
    execute()
