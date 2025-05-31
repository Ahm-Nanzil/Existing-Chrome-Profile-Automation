from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_driver():
    """Setup Chrome driver with custom paths"""
    # Chrome options
    chrome_options = Options()
    chrome_options.binary_location = r"C:\Users\ASUS\Downloads\chrome-win64\chrome-win64\chrome.exe"

    # Optional: Add these for headless mode (browser won't show)
    # chrome_options.add_argument("--headless")

    # Service with custom chromedriver path
    service = Service(r"C:\Users\ASUS\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

    # Create driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_example():
    """Simple scraping example"""
    driver = setup_driver()

    try:
        # Navigate to a website
        driver.get("https://httpbin.org/html")

        # Wait for page to load
        time.sleep(2)

        # Find elements by different methods
        title = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Page title: {title}")

        # Find all paragraphs
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for i, p in enumerate(paragraphs):
            print(f"Paragraph {i + 1}: {p.text}")

        # Example: Scrape quotes from quotes.toscrape.com
        driver.get("http://quotes.toscrape.com/")
        time.sleep(2)

        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        for quote in quotes[:3]:  # Get first 3 quotes
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            print(f"Quote: {text}")
            print(f"Author: {author}")
            print("-" * 50)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()


def scrape_with_wait():
    """Example with explicit waits (recommended)"""
    driver = setup_driver()

    try:
        driver.get("http://quotes.toscrape.com/")

        # Wait for quotes to load
        wait = WebDriverWait(driver, 10)
        quotes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

        print(f"Found {len(quotes)} quotes")

        for quote in quotes[:5]:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]

            print(f"Text: {text}")
            print(f"Author: {author}")
            print(f"Tags: {', '.join(tags)}")
            print("-" * 60)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Starting simple scraping...")
    scrape_example()

    print("\nStarting scraping with waits...")
    scrape_with_wait()