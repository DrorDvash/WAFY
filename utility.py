""""

Utility File for global Functions

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def get_captcha(driver, element, path):
import pytesseract
import sys
import argparse
# try:
#     import Image
# except ImportError:
#     from PIL import Image
from subprocess import check_output
import urllib.request
import time
# from PIL import Image, ImageEnhance, ImageFilter
# import pytesseract
# import cv2
import os
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


# def resolve(path):
#     print("Resampling the Image")
#     check_output(['convert', path, '-resample', '600', path])
#     return pytesseract.image_to_string(Image.open(path))

# def get_captcha(driver):
#     print('Getting Captha')
#     wait = WebDriverWait(driver, 100)
#     # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
#     #     (By.XPATH, "//iframe[starts-with(@src, 'captcha_box.php')]")))
#
#     # img = driver.find_element_by_xpath("//iframe[starts-with(@src, 'captcha_box.php')]")
#     iframes = driver.find_elements_by_tag_name("iframe")[0]
#     src = iframes.get_attribute('src')
#     print(src)
#     urllib.request.urlretrieve(src)
#
#     # download the image
#     # urllib.urlretrieve(src, "captcha.png")
#     # print(iframes)
#     # driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
#     # print(img)
#     # driver.get("http://sistemas.cvm.gov.br/?fundosreg")
#     # img = driver.find_element_by_xpath("//img[@src='captcha.php']")
#     # print(img)
#     # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'Main')))
#     # img = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Table1 img')))
#     # src = img.get_attribute('src')
#     # urllib.request.urlretrieve(src, "captcha.jpeg")


# def get_captcha(driver, element, path):
#     location = element.location
#     size = element.size
#     driver.save_screenshot(path)
#     image = Image.open(path)
#     left = location['x']
#     top = location['y']
#     right = location['x'] + size['width']
#     bottom = location['y'] + size['height']
#     image = image.crop((left, top, right, bottom))
#     image.save(path, 'png')
#     time.sleep(3)
#     get_text_from_pic()

    # im = Image.open('captcha.png')  # the second one
    # # im = im.filter(ImageFilter.MedianFilter())
    # enhancer = ImageEnhance.Contrast(im)
    # im = enhancer.enhance(2)
    # # im = im.convert('1')
    # im.save('captch_test.png')
    # text = pytesseract.image_to_string(im, lang='eng')
    # print(text)
    # # os.remove('captcha.png')



def get_text_from_pic():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread('captcha.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    print(data)

    cv2.imshow('thresh', thresh)
    cv2.imshow('opening', opening)
    cv2.imshow('invert', invert)
    cv2.waitKey()