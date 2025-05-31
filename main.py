from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set your paths
chrome_path = r"C:\Users\ASUS\Downloads\chrome-win64\chrome-win64\chrome.exe"
driver_path = r"C:\Users\ASUS\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
user_data_dir = r"C:\Users\ASUS\AppData\Local\Google\Chrome\User Data"
profile_dir = "Profile 4"  # or whichever profile you want to use

# Setup Chrome options
options = Options()
options.binary_location = chrome_path
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_dir}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open a page
driver.get("https://example.com")

# Keep the browser open
input("Press Enter to close...")
driver.quit()
