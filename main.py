import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

options = uc.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/YourUser/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=Profile 1")  # Optional: your specific profile

driver = uc.Chrome(options=options)
driver.get("https://example.com")

time.sleep(3)

# Example scraping:
title = driver.title
print("Page Title:", title)

# Find some element (example)
element = driver.find_element(By.XPATH, "//h1")
print("Main Header:", element.text)

driver.quit()
