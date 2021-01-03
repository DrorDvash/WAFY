""""
Utility File for global functions
"""

import argparse
import time
import socket
from urllib.parse import urlsplit
from selenium.common.exceptions import NoSuchElementException


def get_cookie_from_driver(driver) -> dict:
    time.sleep(5)  # Wait Cookies To load
    driver_cookies = driver.get_cookies()
    return {c['name']: c['value'] for c in driver_cookies}


def calculate_file_lines(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
    return len(nonempty_lines)


def get_ip_address_of_host(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except:
        return urlsplit(domain_name).netloc


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
    with open('successful_attacks.log', 'a', encoding='utf-8') as log:
        log.write(f'[+] [{attack}] || Payload Passed: {payload}')


def clean_log():
    with open('successful_attacks.log', "w"):
        pass


def add_slash(creds_dict):
    if creds_dict['target_url'][-1] != '/':
        creds_dict['target_url'] = creds_dict['target_url'] + '/'
    return creds_dict


def get_credentials():
    # Get Credentials and target url
    parser = argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('-u', dest='username', type=str, required=True)
    parser.add_argument('-p', dest='password', type=str, required=True)
    parser.add_argument('-target', dest='target_url', type=str, required=True)
    return vars(parser.parse_args())
