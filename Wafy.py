"""
Project was created by Dror Dvash & Ronen Zubkov - White-Hat LTD
Wafy - Testing BeWApp Waf with common attack
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable
import time
import Utility
import Injections
import Cross_Site_Scripting_XSS
import Unauthorized_Access_Control

PATH = r"""chromedriver.exe"""


def main():
    # Get Credentials
    creds = Utility.add_slash(Utility.get_credentials())
    while len(creds) > 3:
        creds()


    while True:
        # Print menu
        print_menu()
        user_choice_main_menu = input("Choose Option --> ")

        # Execute OS Injection Attacks
        if user_choice_main_menu == '1':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website

            t1 = time.perf_counter()  # Start timer
            Injections.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer

            print(f"Finish within {round(t2 - t1, 4)} seconds.")
            driver.quit()

        # Execute XSS Attacks
        elif user_choice_main_menu == '2':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website

            t1 = time.perf_counter()  # Start timer
            Cross_Site_Scripting_XSS.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer

            print(f"Finish within {round(t2 - t1, 4)} seconds.")
            driver.quit()

        # Execute Unauthorized Access Control
        elif user_choice_main_menu == '3':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website

            t1 = time.perf_counter()  # Start timer
            Unauthorized_Access_Control.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer

            print(f"Finish within {round((t2 - t1)/60, 2)} seconds.")
            driver.quit()

        # Execute All Together
        elif user_choice_main_menu == '9':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website

            t1 = time.perf_counter()  # Start timer
            Injections.execute(driver, target_url)
            Cross_Site_Scripting_XSS.execute(driver, target_url)
            Unauthorized_Access_Control.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer

            print(f"Finish within {round((t2 - t1)/60, 2)} minutes.")
            driver.quit()

        elif user_choice_main_menu.lower() == 'q':
            print("Bye bye...")
            break
        else:
            print('Invalid option! try again')


def init(username, password, target_url):
    print("[+] Initializing")

    # Clean Log File
    Utility.clean_log()

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    # driver = webdriver.Chrome(executable_path=PATH, options=options)
    driver = webdriver.Chrome(options=options)

    # Login to website
    driver.get(target_url)
    element = driver.find_element_by_id("login")
    element.clear()
    element.send_keys(username)
    element = driver.find_element_by_id("password")
    element.clear()
    element.send_keys(password, Keys.RETURN)

    return driver, target_url


def print_menu():
    x = PrettyTable()
    x.field_names = ["No.", "Name", "Attacks"]
    x.add_row(["[1]", "Injections", "OS, HTML, iFrame"])
    x.add_row(["[2]", "Cross-Site Scripting", "XSS"])
    x.add_row(["[3]", "Unauthorized Access Control", "LFI/RFI, SSRF, XXE"])
    x.add_row(["[9]", "*Run All*", ""])
    x.add_row(["[Q]", "Quit", ""])
    x.align["Name"] = "l"
    x.align["Attacks"] = "l"
    print("\n")
    print(x)


if __name__ == '__main__':
    main()
