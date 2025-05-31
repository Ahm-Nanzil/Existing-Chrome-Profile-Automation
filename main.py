from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Path to your Chrome user data and profile
user_data_dir = r"C:\Users\ASUS\AppData\Local\Google\Chrome\User Data"
profile_dir = "Profile 4"


# Setup Chrome options
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_dir}")
options.add_argument("--start-maximized")

# Optional: avoid detection (basic)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Setup Chrome service (auto-detects ChromeDriver if in PATH)
driver = webdriver.Chrome(options=options)

# Go to a page to scrape
driver.get("https://example.com")

# Wait for page to load
time.sleep(2)

# Simple scraping (e.g., get page title)
print("Page Title:", driver.title)

# Optional: scrape an element
element = driver.find_element("tag name", "h1")
print("H1 Text:", element.text)

# Keep browser open for debugging
time.sleep(10)
driver.quit()
