from selenium import webdriver
import time

## Example Proxy
PROXY = "41.242.116.150:50003"

## Create WebDriver Options to Add Proxy
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={PROXY}')
chrome = webdriver.Chrome(options=chrome_options)

## Make Request Using Proxy
chrome.get("http://httpbin.org/ip")

time.sleep(1000)