from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import requests
from urllib.parse import quote_plus


def extract_emails_from_text(text):
    """Extract all email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text, re.IGNORECASE)
    return list(set(emails))  # Remove duplicates


def scrape_instagram_profile(driver, url, max_wait=10):
    """Scrape email from Instagram profile"""
    emails = []

    try:
        print(f"Visiting: {url}")
        driver.get(url)

        # Wait for page to load
        WebDriverWait(driver, max_wait).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        # Get page source and look for emails
        page_source = driver.page_source
        emails.extend(extract_emails_from_text(page_source))

        # Look specifically in bio/description areas
        bio_selectors = [
            'div[data-testid="user-bio"]',
            'div.-vDIg span',
            'div.C7I1f span',
            'div.tb97a',
            'span.AFWDX',
            'div.L4X6L',
            'h1._7UhW9',
            'div.KlCQn div'
        ]

        for selector in bio_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text
                    if text:
                        emails.extend(extract_emails_from_text(text))
            except:
                continue

        # Look for "Contact" or "Email" buttons/links
        contact_selectors = [
            'a[href*="mailto:"]',
            'button[title*="Email"]',
            'a[title*="Email"]'
        ]

        for selector in contact_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    href = element.get_attribute('href')
                    if href and 'mailto:' in href:
                        email = href.replace('mailto:', '').split('?')[0]
                        if '@' in email:
                            emails.append(email)
            except:
                continue

        # Remove duplicates and filter valid emails
        unique_emails = []
        for email in emails:
            email = email.strip().lower()
            if email and email not in unique_emails and '@' in email:
                unique_emails.append(email)

        return unique_emails

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


def search_and_scrape_emails():
    # Chrome options with your profile
    options = Options()
    options.binary_location = r"C:\Users\ASUS\Downloads\chrome-win64\chrome-win64\chrome.exe"
    options.add_argument(r"--user-data-dir=C:\Users\ASUS\AppData\Local\Google\Chrome for Testing\User Data")
    options.add_argument("--profile-directory=Profile 3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")

    # ChromeDriver service
    service = Service(r"C:\Users\ASUS\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

    # Create driver
    driver = webdriver.Chrome(service=service, options=options)

    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Multiple search queries for better results
        search_queries = [
            'site:instagram.com "fitness coach" email',
            'site:instagram.com "personal trainer" contact',
            'site:instagram.com "fitness instructor" gmail',
            'site:instagram.com "coach" "@gmail.com"',
            'site:instagram.com "trainer" "@yahoo.com"'
        ]

        all_results = []

        for query in search_queries:
            print(f"\nSearching: {query}")
            google_url = f"https://www.google.com/search?q={quote_plus(query)}"

            driver.get(google_url)
            time.sleep(3)

            # Get search results
            search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")

            for i, result in enumerate(search_results[:5]):  # Limit to 5 per query
                try:
                    # Get title and link
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    title = title_element.text

                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    link = link_element.get_attribute("href")

                    # Skip if not Instagram link
                    if "instagram.com" not in link:
                        continue

                    # Get snippet/description
                    try:
                        snippet_element = result.find_element(By.CSS_SELECTOR, "div[style='-webkit-line-clamp:2']")
                        snippet = snippet_element.text
                    except:
                        try:
                            snippet_element = result.find_element(By.CSS_SELECTOR, ".VwiC3b")
                            snippet = snippet_element.text
                        except:
                            snippet = "No description available"

                    # Check if we already have this profile
                    if any(r['Instagram_Link'] == link for r in all_results):
                        continue

                    print(f"Found profile: {title}")

                    # Scrape emails from the Instagram profile
                    emails = scrape_instagram_profile(driver, link)

                    # Also check snippet for emails
                    snippet_emails = extract_emails_from_text(snippet)
                    emails.extend(snippet_emails)

                    # Remove duplicates
                    unique_emails = list(set(emails))

                    all_results.append({
                        'Title': title,
                        'Instagram_Link': link,
                        'Description': snippet,
                        'Emails_Found': ', '.join(unique_emails) if unique_emails else "No email found",
                        'Email_Count': len(unique_emails)
                    })

                    print(f"Emails found: {unique_emails if unique_emails else 'None'}")

                    # Small delay between profile visits
                    time.sleep(2)

                except Exception as e:
                    print(f"Error processing result: {e}")
                    continue

            # Delay between searches
            time.sleep(5)

        # Save to CSV
        csv_filename = "instagram_fitness_coaches_with_emails.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Instagram_Link', 'Description', 'Emails_Found', 'Email_Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in all_results:
                writer.writerow(row)

        print(f"\nSaved {len(all_results)} results to {csv_filename}")

        # Print summary
        profiles_with_emails = [r for r in all_results if r['Email_Count'] > 0]
        print(f"Profiles with emails found: {len(profiles_with_emails)}")
        print(f"Total profiles scraped: {len(all_results)}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


# Alternative function for more targeted email extraction
def extract_emails_from_instagram_bio(driver, profile_url):
    """More focused email extraction from Instagram bio"""
    try:
        driver.get(profile_url)
        time.sleep(5)

        # Wait for profile to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )

        emails = []

        # Try to find and click "Contact" button if exists
        try:
            contact_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Contact')]")
            contact_button.click()
            time.sleep(2)

            # Look for email in contact info
            email_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto:')]")
            for elem in email_elements:
                href = elem.get_attribute('href')
                if href:
                    email = href.replace('mailto:', '').split('?')[0]
                    emails.append(email)

        except:
            pass

        # Look in bio text
        try:
            bio_element = driver.find_element(By.XPATH, "//div[@data-testid='user-bio']//span")
            bio_text = bio_element.text
            bio_emails = extract_emails_from_text(bio_text)
            emails.extend(bio_emails)
        except:
            pass

        return list(set(emails))

    except Exception as e:
        print(f"Error extracting from {profile_url}: {e}")
        return []


# Run the search
if __name__ == "__main__":
    search_and_scrape_emails()