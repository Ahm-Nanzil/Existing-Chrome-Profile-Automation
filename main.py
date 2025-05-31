from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def simple_scrape():
    # Chrome options with your profile
    options = Options()
    options.binary_location = r"C:\Users\ASUS\Downloads\chrome-win64\chrome-win64\chrome.exe"
    options.add_argument(r"--user-data-dir=C:\Users\ASUS\AppData\Local\Google\Chrome for Testing\User Data")
    options.add_argument("--profile-directory=Profile 3")

    # ChromeDriver service
    service = Service(r"C:\Users\ASUS\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

    # Create driver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Go to a website
        driver.get("https://www.example.com")
        time.sleep(3)

        # Get page title
        title = driver.title
        print(f"Page Title: {title}")

        # Get all text from the page
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"Page Content:\n{body_text}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


# Run the scraper
if __name__ == "__main__":
    simple_scrape()