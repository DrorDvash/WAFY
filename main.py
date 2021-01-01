from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import A1_Injection
#import A2_Broken_Authentication
import A3_Cross_Site_Scripting_XSS
#import A7_Missing_Functional_Level_Access_Control
import textwrap
import attack_csrf
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"

def main():
    main_menu = '''
    [1]  Run 'A1 Injections'
    [2]  Run 'A2 Broken Authentication'
    [3]  Run 'A3 Cross Site Scripting (XSS)'
    [7]  Run 'A7 Missing Functional Level Access Control'
    [9]  Run All
    [Q]  Quit
    '''

    while True:
        # Print menu
        print(textwrap.dedent(main_menu))
        user_choice_main_menu = input("Choose Option --> ")

        # Execute OS Injection Attacks
        if user_choice_main_menu == '1':
            driver, target_url = init()  # Create driver and login to website
            A1_Injection.execute(driver, target_url)
            driver.quit()

        # Execute Broken Authentication Attacks
        elif user_choice_main_menu == '2':
            pass
        # Execute XSS Attacks
        elif user_choice_main_menu == '3':
            driver, target_url = init()  # Create driver and login to website
            A3_Cross_Site_Scripting_XSS.execute(driver, target_url)
            driver.quit()

        # Execute Missing Functional Level Access Control
        elif user_choice_main_menu == '7':
            pass

        # Execute All Together
        elif user_choice_main_menu == '9':
            driver, target_url = init()  # Create driver and login to website
            A1_Injection.execute(driver, target_url)
            #..
            A3_Cross_Site_Scripting_XSS.execute(driver, target_url)
            #..
            #..
            driver.quit()

        elif user_choice_main_menu.lower() == 'q':
            print("Bye bye...")
            break
        else:
            print('Invalid option! try again')


def init():
    print("[+] Initializing")
    options = webdriver.ChromeOptions()
    # options.add_argument('no-sandbox')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--window-size=200,200')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=PATH, options=options)

    #driver = webdriver.Chrome(executable_path=PATH)

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


if __name__ == '__main__':
    main()

