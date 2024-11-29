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
### Zusätzlich Website Täuschungsoptionen um natürlicher zu wirken
from selenium_stealth import stealth
### Um (private) Proxies mit undetectable Chromedriver zu nutzen (Code in extra Datei)
from proxies_settings import proxy_settings
#   #   #   #   #   #


pfad_des_ordners = "C:/Users/Noah/Downloads/Website_Klicker/"


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
with open(pfad_des_ordners + "useragents.txt", "r") as useragents_list:
    useragents_list_gelesen = useragents_list.readlines()
    random_useragent_array = random.choice(useragents_list_gelesen)

print(random_useragent_array)


# create webdriver object
chrome_options = ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--incognito')
chrome_options.add_argument(f'--user-agent={random_useragent_array}')
#  #  #  #  #
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})
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
#  #  #  #  #

## Proxy Options
proxy_settings(chrome_options, pfad_des_ordners)

#  #  #  #  #

#creating (web-)driver resource (seleniumwire_options nur für (private) proxy)
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

#Wenn nach 6 Sekunden die Website nicht fertig geladen ist, dann wird sie neu geladen
driver.set_page_load_timeout(6)


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
driver.get("https://controller.com/")
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



#------------------------------------------------------------------------------------------
time_sleep(1000)