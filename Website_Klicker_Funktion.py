from undetected_chromedriver import ChromeOptions, Chrome
#	#	#	#	#	#	#	#	#	#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchFrameException
from selenium.common.exceptions import MoveTargetOutOfBoundsException #NUR FUR ACTION CHAIN ERRORS
import time, random
from selenium.webdriver.common.action_chains import ActionChains
import requests
### Zusätzlich Website Täuschungsoptionen um natürlicher zu wirken
from selenium_stealth import stealth
### Um (private) Proxies mit undetectable Chromedriver zu nutzen (Code in extra Datei)
from proxies_settings import proxy_settings
### Um Haupt-Url aus Link zu extrahieren
from urllib.parse import urlsplit
### Selenium Wire für header interceptor
from seleniumwire import webdriver
### Um aktuellen Pfad zu bekommen
import os
#   #   #   #   #   #

#pfad_des_ordners = "C:/Users/Noah/Downloads/Website_Klicker"
if __name__ == "__main__":
    pfad_des_ordners = os.path.dirname(os.path.abspath(__file__))

def main(pfad_des_ordners):

    def close_opened_window(second_tit):
        time.sleep(1)
        first_tit = len(driver.window_handles)
        if first_tit > second_tit:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)

    def DriverClose(driver):
        try:
            driver.close()
        except NoSuchWindowException:
            print("NoSuchWindowException in driver.close()")
            return False
        return True

    def NewTab(driver, Link, default_page=0, custom=0):
        window_count = len(driver.window_handles)
        driver.execute_script('''window.open("'''+Link+'''","_blank");''')
        while len(driver.window_handles) != window_count+1:
            time.sleep(0.5)
        if custom == 0:
            driver.switch_to.window(driver.window_handles[-1])
        if custom != 0:
            driver.switch_to.window(driver.window_handles[custom])    
        time.sleep(2)
        if driver.current_url == Link:
            current_window = driver.current_window_handle
            return current_window
        if driver.current_url == "about:blank":
            time.sleep(2)
            DriverClose()
            driver.switch_to.window(driver.window_handles[default_page])
            print("current window was about:blank we closed it, trying again in 10s")
            time.sleep(10)
            NewTab(driver, Link, default_page, custom)
        if driver.current_url != Link:
            pass

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def time_sleep(inttime):
        times_sleepes = int(inttime)
        times_int_1 = [0.1,0.2,0.3,0.4,0.5,0.6,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.61,0.62,0.63,0.64,0.65,0.66]
        times_int_2 = [0.7,0.8,0.9,0.67,0.68,0.69,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.91,0.92,0.92,0.93,0.94,0.95,0.96,0.96,0.97,0.98,0.99]
        times_fir = [times_sleepes, times_sleepes-1]
        times_int_fir_index = random.choice([0,1])
        times_int_fir = times_fir[times_int_fir_index]
        if times_int_fir_index == 0:
            timeint = times_int_fir+random.choice(times_int_1)
        elif times_int_fir_index == 1:
            timeint = times_int_fir+random.choice(times_int_2)
        else:
            timeint = inttime
        timeintet = abs(timeint)
        time.sleep(timeintet)


    #UserAgents importieren und zufällig einen auswählen
    with open(pfad_des_ordners + "/useragents.txt", "r") as useragents_list:
        useragents_list_gelesen = useragents_list.readlines()
        random_useragent_array = random.choice(useragents_list_gelesen)

    print(random_useragent_array)


    # create webdriver object
    chrome_options = ChromeOptions()

    #  #  #  #  #
    # Proxy Options (+die anderen Extensions)
    chrome_options.add_argument(f"--load-extension={proxy_settings(pfad_des_ordners)},{pfad_des_ordners}/extension/WebRTC-Control,{pfad_des_ordners}/extension/Canvas-Fingerprint-Defender")
    #  #  #  #  #

    #chrome_options.add_argument("--kiosk")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-css-rendering')
    chrome_options.add_argument(f'--user-agent={random_useragent_array}')

    # ------- # ------- #
    # Bilder auf der Website blockieren (spart viel Bandwidth, aber könnte auffällig sein und blockiert werden)
    if random.choices([1,2], weights = (70,30)) == 2:
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        print("images disabled")
    # ------- # ------- #

    #  #  #  #  #
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #  #  #  #  #
    # Disable downloads
    prefs = {
        "profile.default_content_settings.popups": 1,
        "download.default_directory": "/dev/null",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "download_restrictions": 3,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # Allow pop-ups and notifications
    #chrome_options.add_argument("--disable-popup-blocking")
    #chrome_options.add_argument("--disable-notifications")
    #chrome_options.add_argument("--enable-javascript")
    #  #  #  #  #
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument("--disable-popup-blocking")

    #SEHR WICHTIG UM BANDWIDTH USAGE DRASTISCH ZU REDUZIEREN! Verhindert Background Downloads / -Updates in Chrome, welche sehr viel Bandwidth verbrauchen
    chrome_options.add_argument("--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints")

    #creating (web-)driver resource
    driver = Chrome(options=chrome_options)

    #Stealth Options
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    #Zeitzone korrigieren je nach Proxy Location
    with open (pfad_des_ordners+"/proxy_settings.txt", "r") as read_proxy_settings:
            lines_of_proxy_settings_txt = read_proxy_settings.readlines()
            proxy_settings_eingelesen = lines_of_proxy_settings_txt[1].split(":")
            proxy = "http://"+proxy_settings_eingelesen[2]+":"+proxy_settings_eingelesen[3]+"@"+proxy_settings_eingelesen[0]+":"+proxy_settings_eingelesen[1]
            
    proxies = { 
        'http': proxy, 
        'https': proxy
    }

    def get_public_ip():
        try:
            response = requests.get("http://api.ipify.org", proxies=proxies, verify=False)
            print(response.text.strip())
            return response.text.strip()
        except requests.exceptions.RequestException as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

    def get_timezone(ip):
        try:
            response = requests.get(f"https://timeapi.io/api/timezone/ip?ipAddress={ip}")
            data = response.json()
            response.raise_for_status()
            print(data['timeZone'])
            return data['timeZone']
        except requests.exceptions.RequestException as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
    
    timezone = get_timezone(get_public_ip())
    chrome_options.add_argument(f"--timezone={timezone}")

    #define the request interceptor to configure custom headers
    def interceptor(request):

        #add the missing headers
        request.headers["Accept-Language"] = "en-US,en;q=0.9"
        request.headers["Referer"] = random.choice(["https://www.google.com/","https://www.youtube.com/","https://www.facebook.com/","https://www.yahoo.com/","https://www.t.co/","https://www.instagram.com/","https://www.taobao.com/","https://www.pinterest.com/","https://www.sohu.com/","https://www.google.de/""https://www.google.it/","https://www.google.es/","https://www.google.nl/","https://www.google.co.in/","https://www.google.co.kr/","https://www.whatsapp.com/","https://www.blogspot.com/","https://www.tumblr.com/"])

        # delete the existing misconfigured default headers values
        del request.headers["User-Agent"]
        del request.headers["Sec-Ch-Ua"]
        del request.headers["Sec-Fetch-Site"]
        del request.headers["Accept-Encoding"]

        #replace the deleted headers with edited values
        request.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        request.headers["Sec-Ch-Ua"] = "\"Chromium\";v=\"131\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"131\""
        request.headers["Sec-Fetch-Site"] = "cross-site"
        request.headers["Accept-Encoding"] = "gzip, deflate, br, zstd"

    #add the interceptor
    driver.request_interceptor = interceptor


    #Wenn nach 180 Sekunden (3 Minuten) die Website nicht fertig geladen ist, dann wird sie geschlossen

    driver.set_page_load_timeout(180)

    #Hier die Funktion dazu
    def driver_get(link):
        try:
            driver.get(link)
        except(TimeoutError,TimeoutException):
            driver.delete_all_cookies()
            time.sleep(0.25)
            i = 0
            tabs_anzahl = len(driver.window_handles)
            while i < (tabs_anzahl-1):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                time.sleep(0.125)
                i += 1
            time.sleep(0.25)
            driver.switch_to.window(driver.window_handles[0])
            driver.delete_all_cookies()
            try:
                driver.get(link)
            except(TimeoutError,TimeoutException):
                return
                

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.maximize_window()
        driver.delete_all_cookies()

    #Website aufrufen
    #Noch unterschiedliche Unterlinks (z.B. zu den Posts in eine Liste machen und dann random einen davon auswählen, damit nicht immer nur bugame.xyz aufgerufen wird)
    with open (f"{pfad_des_ordners}/Link.txt") as Link_Pools:
        Link_Pool = Link_Pools.readlines()
        Haupt_Link = Link_Pool[0]
    Link_Choice = random.choice([Haupt_Link,Link_Pool])
    if Link_Choice == Link_Pool:
        Link = random.choice(Link_Pool)
    else:
        Link = Haupt_Link

    print(Link)
    #--------------------------Hauptteil des Links extrahieren---------------
    split_url = urlsplit(Link)
    Link_Base = split_url.netloc
    #------------------------------------------------------------------------
    #driver.get("https://proxy.incolumitas.com/proxy_detect.html")
    driver.get(Link)
    driver.maximize_window()

    #Zeitzone zur Sicherheit nochmal richtig einstellen
    driver.execute_script(f"Intl.DateTimeFormat().resolvedOptions().timeZone = '{timezone}';")

    time.sleep(1)

    driver.execute_script('document.getElementsByTagName("html")[0].style.scrollBehavior = "auto"')

    #Define Action Chain
    actions = ActionChains(driver)

    def action_coordinates(x,y):
        actions.reset_actions()
        try:
            actions.move_by_offset(x,y).perform()
            actions.click(on_element=None).perform()
        except(MoveTargetOutOfBoundsException,TimeoutException):
            pass

    def action_element(click_banner):
        actions.reset_actions()
        # Move the mouse to the desired location
        actions.move_to_element(click_banner).perform()
        # Click on the specific location
        actions.click(on_element=click_banner).perform()

    #------------------------------------------------------------------------------------------
    #Funktionen für die Seite
    #####################################################################
    #Ein paar Interaktions Funktionen, die nichts machen, außer Nutzeraktivität zu simulieren

    def scroll_half_page():
        time_sleep(2)
        driver.execute_script("window.scrollTo(0, (0.5*document.body.scrollHeight))")

    def scroll_full_page():
        time_sleep(2)
        html_page = driver.find_element(By.TAG_NAME, 'html')
        html_page.send_keys(Keys.PAGE_DOWN)

    def click_random_article_on_site():
        time_sleep(3)
        article_number = random.choice([1,2,3,4,5,6,7,8,9,10])
        articles_xpaths = ["/html/body/div[1]/div/div/div/main/div/article["+article_number+"]/div/div/div[1]/div/a/img","/html/body/div[1]/div/div/div/main/div/article["+article_number+"]/div/div/h2/a"]
        click_article_element = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, random.choice(articles_xpaths))))
        click_article_element.click()

    def second_page_navigator_bottom():
        time_sleep(3)
        zwei_unten_auf_der_seite_bottom = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/div/div/nav/div/a[1]")))
        zwei_unten_auf_der_seite_bottom.click()

    def dreizehn_page_navigator_bottom():
        time_sleep(3)
        dreizehn_unten_auf_der_seite_bottom = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/div/div/nav/div/a[1]")))
        dreizehn_unten_auf_der_seite_bottom.click()

    def navigate_next_or_previous_page():
        time_sleep(3)
        navigatoren_next_or_previous_page = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/div/div/nav/div/a[4]")))
        navigatoren_next_or_previous_page.click()

    def klick_auf_header_element():
        time_sleep(3)
        random_header_element_fuer_klick = "/html/body/div[1]/header/div[1]/div/div/div/div/div[2]/div/div/div/nav/div/ul/li["+random.choice([1,2,3,4,5])+"]/a"
        random_header_element_fuer_klick.click()

    def stantseiten_icon_oben_links():
        time_sleep(3)
        stantseiten_icon = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/header/div[1]/div/div/div/div/div[1]/div/div/div/span/a")))
        stantseiten_icon.click()
    #####################################################################
    def random_funktion_von_den_oberen():
        liste_der_oberen_funktionen = [scroll_half_page,scroll_full_page,click_random_article_on_site,click_random_article_on_site,second_page_navigator_bottom,dreizehn_page_navigator_bottom,navigate_next_or_previous_page,klick_auf_header_element,stantseiten_icon_oben_links]
        auszufuerende_der_funktionen = random.choice(liste_der_oberen_funktionen)
        auszufuerende_der_funktionen
    #####################################################################
    def get_random_Koordinaten():
        koordinaten = [(280,475),(800,522),(1204,461),(501,504),(209,874),(828,899),(1744,838),(1332,484),(1882,474),(723,445),(797,647),(378,827),(1047,767),(1086,404),(939,538),(1076,797),(188,719),(1610,447),(988,398),(415,232),(456,392),(203,341),(1329,443),(1319,831),(411,815),(932,637),(1017,451),(1026,759),(543,872),(868,981)]
        random_koordinate = random.choice(koordinaten)
        randomizing_the_cords = [0,1,2,3,4,5,6,7,8,9,-1,-2,-3,-4,-5,-6,-7,-8,-9]
        neue_random_koords = (random_koordinate[0]+random.choice(randomizing_the_cords),random_koordinate[1]+random.choice(randomizing_the_cords))
        
        return neue_random_koords[0],neue_random_koords[1]
    #####################################################################
    def close_new_tab(actual_tabs_anzahl):
        #	-	-	-	-	-	#
        i = 0 ; hubertus_tab_existiert = False
        while i < actual_tabs_anzahl:
            try:
                driver.switch_to.window(driver.window_handles[i])
                if (Link_Base) in driver.current_url:
                    hubertus_tab_existiert = True
                    i = actual_tabs_anzahl
                else:
                    hubertus_tab_existiert = False
                    i += 1
            except(NoSuchWindowException):
                i += 1
        #	-	-	-	-	-	#
        if hubertus_tab_existiert == True:
            if actual_tabs_anzahl > 1:
                driver.switch_to.window(driver.window_handles[0])
                if (Link_Base) not in driver.current_url:
                    driver.close()
                else:
                    driver.switch_to.window(driver.window_handles[0])
                    if (Link_Base) not in driver.current_url:
                        driver.close()
                    else:
                        i = 0
                        tabs_anzahl = len(driver.window_handles)
                        while i < (tabs_anzahl-1):
                            driver.switch_to.window(driver.window_handles[-1])
                            driver.close()
                            time.sleep(0.125)
                            i += 1
                        driver.switch_to.window(driver.window_handles[0])
                        driver_get(Link)
                        time_sleep(3)
                time.sleep(0.5)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(0.5)
            else:
                time.sleep(0.5)
                driver.switch_to.window(driver.window_handles[-1])
        else:
            #		-		-		-		#
            i = 0
            tabs_anzahl = len(driver.window_handles)
            while i < (tabs_anzahl-1):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                print(i)
                time.sleep(0.125)
                i += 1

            time_sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            #		-		-		-		#
    #			#			#			#			#
    #------------------------------------------------------------------------------------------
    #Ausführen der Funktionen für die Seite

    #                   #                   #                       
    random_page_scrolling = [0,1,2,3,4,5,6]
    random_scrolling_number = random.choice(random_page_scrolling)
    if random_scrolling_number == 0:
        scroll_half_page()
    elif random_scrolling_number == 2:
        scroll_half_page()
    else:
        pass
    #                   #                   #

    time_sleep(2)
    action_coordinates(get_random_Koordinaten()[0],get_random_Koordinaten()[1])
    time_sleep(3)
    close_new_tab(len(driver.window_handles))


    for h in range(random.choice([1,2,3])):
        
        for g in range(random.choice([1,2,3,4])):

            #   #   #   #   #
            if len(driver.window_handles) == 1:
                aktuelle_url = driver.current_url
                split_aktuelle_url = urlsplit(aktuelle_url)
                aktuelle_Link_Base = split_aktuelle_url.netloc
                if not Link_Base == aktuelle_Link_Base:
                    driver.execute_script("window.history.go(-1)")
                    time.sleep(0.5)
            #   #   #   #   #

            try:

                random_scrolling_number = random.choice(random_page_scrolling)

                if random_scrolling_number in [1]:
                    action_coordinates(get_random_Koordinaten()[0],get_random_Koordinaten()[1])
                    random.choice([time_sleep(2),time_sleep(5),time_sleep(8),time_sleep(9),time_sleep(3)])
                    close_new_tab(len(driver.window_handles))

                if random_scrolling_number in [1,2,3,4]:
                    random_funktion_von_den_oberen()
                    random.choice([time_sleep(3),time_sleep(4),time_sleep(6),time_sleep(7),time_sleep(2)])
                    close_new_tab(len(driver.window_handles))

        
                if random.choice([1,2,3,4,5]) == 1:
                    scroll_half_page()
                    time_sleep(1)

            except(TimeoutException,NoSuchWindowException,NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException):
                pass

    time_sleep(3)
    driver.close()
    driver.quit()
    print("Driver Quit")

    #------------------------------------------------------------------------------------------
    #time_sleep(100000)