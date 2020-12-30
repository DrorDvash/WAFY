from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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


def execute():
    driver, target_url = init()  # to delete

    # Get all relevant results
    relevant_attacks = read_all_attacks(driver)

    # Start to attack
    implement_attack(driver, relevant_attacks)

    driver.quit()


def read_all_attacks(driver):
    print("[+] Collecting Attacks")
    attack_type = "Cross-Site Scripting - "
    relevant_attacks = []
    elements = driver.find_elements_by_xpath("//form/select[@name='bug']/option")
    for item in elements:
        if attack_type in item.text:
            # Insert any result into list of lists eg: [ [obj, name, index], [obj, name, index] ]
            relevant_attacks.append([item, item.text, item.get_attribute("value")])
    return relevant_attacks


def implement_attack(driver, relevant_attacks):
    print(relevant_attacks)
    print("[+] Start Attacking")
    for attack in relevant_attacks:
        elements = driver.find_element_by_xpath(f"//form/select[@name='bug']/option[{attack[2]}]")
        elements.click()
        el = driver.find_element_by_xpath("//form/button[@type='submit']").click()

        time.sleep(2)
        print("Trying Payload: ", attack[1])
        # Send payloads
        # ...
        time.sleep(2)

        # Move to next attack type
        el = driver.back()
        time.sleep(2)


if __name__ == '__main__':
    execute()
