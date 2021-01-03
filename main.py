"""

    Project was created by Dror Dvash & Ronen Zubkov - White Hat LTD
    Wafy - Testing BeWApp Waf with common attack


"""

import A1_Injection
import A3_Cross_Site_Scripting_XSS
import A7_Missing_Functional_Level_Access_Control
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable
import time
import utility
import argparse

PATH = r".\chromedriver.exe"


def main():
    # Get Credentials
    creds = utility.add_slash(get_credentials())
    print(creds['target_url'])
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
            A1_Injection.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer
            print(f"Finish within {round(t2 - t1, 4)} seconds.")

            driver.quit()

        # Execute XSS Attacks
        elif user_choice_main_menu == '2':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website
            t1 = time.perf_counter()  # Start timer
            A3_Cross_Site_Scripting_XSS.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer
            print(f"Finish within {round(t2 - t1, 4)} seconds.")
            driver.quit()

        # Execute Missing Functional Level Access Control
        elif user_choice_main_menu == '3':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website
            t1 = time.perf_counter()  # Start timer
            A7_Missing_Functional_Level_Access_Control.execute(driver, target_url)
            t2 = time.perf_counter()  # Stop timer
            print(f"Finish within {round(t2 - t1, 4)} seconds.")

        # Execute All Together
        elif user_choice_main_menu == '9':
            driver, target_url = init(creds['username'], creds['password'], creds['target_url'])  # Create driver and login to website

            t1 = time.perf_counter()  # Start timer

            A1_Injection.execute(driver, target_url)
            A3_Cross_Site_Scripting_XSS.execute(driver, target_url)
            A7_Missing_Functional_Level_Access_Control.execute(driver, target_url)

            t2 = time.perf_counter()  # Stop timer
            print(f"Finish within {round(t2 - t1, 4)} seconds.")
            driver.quit()

        elif user_choice_main_menu.lower() == 'q':
            print("Bye bye...")
            break
        else:
            print('Invalid option! try again')


def init(username, password, target_url):
    print("[+] Initializing")

    # Clean Log File
    utility.clean_log()

    options = webdriver.ChromeOptions()
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
    x.add_row(["[9]", "Run All", ""])
    x.add_row(["[Q]", "Quit", ""])
    x.align["Name"] = "l"
    x.align["Attacks"] = "l"
    print(x)


def get_credentials():
    # Get Credentials
    parser = argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('-u', dest='username', type=str, required=True)
    parser.add_argument('-p', dest='password', type=str, required=True)
    parser.add_argument('-target', dest='target_url', type=str, required=True)
    return vars(parser.parse_args())


if __name__ == '__main__':
    main()
