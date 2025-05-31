import undetected_chromedriver as webdriver
import time

options = webdriver.Chrome0ptions()
profile = "C:\\Users\\harry\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"
options.add_argument(f"user-data-dir={profile}")
driver = webdriver. Chrome(options=options, use_subprocess=True)
driver.get("https://myaccount.google.com/")

time.sleep(100000)