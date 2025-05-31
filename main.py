import undetected_chromedriver as uc
import time
import sys


def create_chrome_driver():
    """Create Chrome driver with error handling for Python 3.13 compatibility"""

    options = uc.ChromeOptions()

    # Use your full Chrome "User Data" directory, not just the profile folder
    user_data_dir = "C:\\Users\\harry\\AppData\\Local\\Google\\Chrome\\User Data"
    profile_dir = "Profile 4"

    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")

    # Additional options to improve stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    try:
        # Method 1: Try with version parameter (may work with updated undetected-chromedriver)
        driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
        return driver
    except Exception as e1:
        print(f"Method 1 failed: {e1}")

        try:
            # Method 2: Try without use_subprocess
            driver = uc.Chrome(options=options, version_main=None)
            return driver
        except Exception as e2:
            print(f"Method 2 failed: {e2}")

            try:
                # Method 3: Try with basic configuration
                driver = uc.Chrome(options=options)
                return driver
            except Exception as e3:
                print(f"Method 3 failed: {e3}")
                print("All methods failed. Consider using regular selenium WebDriver instead.")
                return None


def main():
    print(f"Python version: {sys.version}")

    driver = create_chrome_driver()

    if driver:
        try:
            driver.get("https://myaccount.google.com/")
            print("Successfully opened Google My Account page")
            time.sleep(100000)  # Keep browser open
        except Exception as e:
            print(f"Error navigating to page: {e}")
        finally:
            driver.quit()
    else:
        print("Failed to create Chrome driver")


if __name__ == "__main__":
    main()