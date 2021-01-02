import time
import socket
from urllib.parse import urlsplit
from selenium.common.exceptions import NoSuchElementException

""""

Utility File for global Functions

"""


def get_cookie_from_driver(driver):
    time.sleep(5)  # Wait Cookies To load
    driver_cookies = driver.get_cookies()
    return {c['name']: c['value'] for c in driver_cookies}


def calculate_file_lines(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        nonempty_lines = [line.strip("\n") for line in file if line != "\n"]

    return len(nonempty_lines)


def get_ip_addres_of_host(domainName):
    try:
        return socket.gethostbyname(domainName)
    except:
        return urlsplit(domainName).netloc

def check_if_element_exists(driver, find_by, value, get_att=False, att_value=""):
    try:
        if find_by == "id":
            driver.find_element_by_id(value).get_attribute(att_value) if get_att else driver.find_element_by_id(value)
        elif find_by == "name":
            driver.find_element_by_name(value).get_attribute(att_value) if get_att != "" else driver.find_element_by_name(value)
        elif find_by == "tag_name":
            driver.find_element_by_tag_name(value).get_attribute(att_value) if get_att != "" else driver.find_element_by_tag_name(value)
        elif find_by == "xpath":
            driver.find_element_by_xpath(value).get_attribute(att_value) if get_att != "" else driver.find_element_by_xpath(value)
        else:
            print("Unknown element name")
            return False
        return True
    except NoSuchElementException:
        return False

def write_to_log(attack, payload) -> None:
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write(f'[+] {attack} Payload passed: ', payload)