from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import re


def search_and_save():
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
        # Search query
        search_query = 'site:instagram.com "Football Coach" "@gmail.com"'
        google_url = f"https://www.google.com/search?q={search_query}"

        driver.get(google_url)
        time.sleep(3)

        # Get search results
        results = []
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")

        for result in search_results[:10]:  # Get first 10 results
            try:
                # Get title and link
                title_element = result.find_element(By.CSS_SELECTOR, "h3")
                title = title_element.text

                link_element = result.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href")

                # Get snippet/description
                try:
                    snippet_element = result.find_element(By.CSS_SELECTOR, "div[style='-webkit-line-clamp:2']")
                    snippet = snippet_element.text
                except:
                    snippet = "No description available"

                # Extract email if visible in snippet
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@gmail\.com\b', snippet)
                email = email_match.group(0) if email_match else "Email not visible"

                results.append({
                    'Title': title,
                    'Instagram_Link': link,
                    'Description': snippet,
                    'Email': email
                })

                print(f"Found: {title}")

            except Exception as e:
                print(f"Error processing result: {e}")
                continue

        # Save to CSV
        csv_filename = "football_coaches_instagram.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Instagram_Link', 'Description', 'Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow(row)

        print(f"\nSaved {len(results)} results to {csv_filename}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


# Run the search
if __name__ == "__main__":
    search_and_save()