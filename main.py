from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import attack_xss
import attack_csrf
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"

def main():

    # Create driver and login to page.
    driver, target_url = init()

    # Execute XSS Attacks
    attack_xss.execute(driver, target_url)

    # Execute CSRF Attacks
    # ...

    driver.quit()

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

if __name__ == '__main__':
    main()

