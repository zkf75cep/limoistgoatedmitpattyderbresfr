import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions, Chrome
import os , time

options = uc.ChromeOptions()


pfad_des_ordners = "C:/Users/Noah/Downloads/Website_Klicker"

def proxy_settings (pfad_des_ordners):
    with open (pfad_des_ordners+"/proxy_settings.txt", "r") as read_proxy_settings:
        lines_of_proxy_settings_txt = read_proxy_settings.readlines()
        proxy_settings_eingelesen = lines_of_proxy_settings_txt[1].split(":")
    #PROXY_FOLDER = os.path.join('extension', 'proxy_folder')
    PROXY_FOLDER = pfad_des_ordners + "/extension/proxy_folder"
    #PROXY_HOST = "superproxy.zenrows.com"
    #PROXY_PORT = "1337"
    #PROXY_USER = "y3rMTmT8WBS7"
    #PROXY_PASS = "cGFBgtoViTu9"
    PROXY_HOST = proxy_settings_eingelesen[0]
    PROXY_PORT = proxy_settings_eingelesen[1]
    PROXY_USER = proxy_settings_eingelesen[2]
    PROXY_PASS = proxy_settings_eingelesen[3]
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    with open(f"{PROXY_FOLDER}/manifest.json","w") as f:
        f.write(manifest_json)
    with open(f"{PROXY_FOLDER}/background.js","w") as f:
        f.write(background_js)
    print(PROXY_FOLDER)
    return PROXY_FOLDER   

#options = ChromeOptions()
#options.add_argument(f"--load-extension={PROXY_FOLDER}")
#options.add_argument(f"--load-extension={proxy_settings(pfad_des_ordners)}")

#driver = uc.Chrome(options=options)

#driver.get("https://myip.com")
#time.sleep(2)

#time.sleep(1000)