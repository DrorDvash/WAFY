""""

Utility File for global Functions

"""

import time
import socket
from urllib.parse import urlsplit

def get_cookie_from_driver(driver):
    time.sleep(5)  # Wait Cookies To load
    driver_cookies = driver.get_cookies()
    return {c['name']: c['value'] for c in driver_cookies}

def calculate_file_lines(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        nonempty_lines = [line.strip("\n") for line in file if line != "\n"]

    return len(nonempty_lines)

def clean_file_from_duplicates():
    lines_seen = set() # holds lines already seen
    with open("Output_file.txt", "w") as output_file:
        for each_line in open("./Payloads/LFI_RFI_Injections.txt", "r", encoding='utf-8'):
            if each_line not in lines_seen: # check if line is not duplicate
                output_file.write(each_line)
                lines_seen.add(each_line)

def get_ip_addres_of_host(domainName):

    try:
        return socket.gethostbyname(domainName)
    except:
        return urlsplit(domainName).netloc
