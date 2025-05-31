from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_path = r"C:\Users\ASUS\Downloads\chrome-win64\chrome-win64\chrome.exe"
driver_path = r"C:\Users\ASUS\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

options = Options()
options.binary_location = chrome_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")  # helps with DevTools port issue
options.add_argument("--disable-gpu")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://example.com")

input("Press Enter to quit...")
driver.quit()
