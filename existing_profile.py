from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import psutil
import os
import time


def debug_print(message):
    print(f"[DEBUG] {message}")


def kill_chrome_processes():
    debug_print("Killing Chrome processes...")
    try:
        # Taskkill method
        debug_print("Running taskkill...")
        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], check=True)
        subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'], check=True)
    except subprocess.CalledProcessError as e:
        debug_print(f"taskkill failed: {e}")

    # Psutil method
    debug_print("Checking with psutil...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and (
                    'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower()):
                debug_print(f"Terminating PID {proc.info['pid']} ({proc.info['name']})")
                psutil.Process(proc.info['pid']).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            debug_print(f"Couldn't terminate process: {e}")


def verify_profile_path():
    profile_path = r"C:\Users\ASUS\AppData\Local\Google\Chrome\User Data\Profile"
    debug_print(f"Verifying profile path: {profile_path}")

    if not os.path.exists(profile_path):
        debug_print("Profile path does not exist!")
        return False

    debug_print("Profile path exists")
    return True


# Main execution
debug_print("Starting debug process...")

# 1. Process killing
kill_chrome_processes()
time.sleep(3)  # Wait for processes to terminate

# 2. Profile verification
if not verify_profile_path():
    debug_print("Profile verification failed - trying Default profile")
    profile_dir = "Default"
else:
    profile_dir = "Profile 3"

# 3. Chrome options
debug_print("Configuring Chrome options...")
chrome_options = Options()
user_data_dir = r"C:\Users\ASUS\AppData\Local\Google\Chrome\User Data"

chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_dir}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
# Add these additional options to your existing code:
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")  # Disable all extensions
chrome_options.add_argument("--disable-plugins")   # Disable plugins
# 4. Try to launch Chrome
debug_print("Attempting to launch Chrome...")
try:
    driver = webdriver.Chrome(options=chrome_options)
    debug_print("Chrome launched successfully!")

    debug_print("Navigating to pump.fun/create...")
    driver.get("https://pump.fun/create")
    debug_print(f"Current URL: {driver.current_url}")

    input("Press Enter to close browser...")
    driver.quit()
except Exception as e:
    debug_print(f"Failed to launch Chrome: {e}")
    debug_print("Trying without profile...")

    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
        debug_print("Launched Chrome without profile!")
        driver.get("https://google.com")
        debug_print(f"Current URL: {driver.current_url}")
        input("Press Enter to close browser...")
        driver.quit()
    except Exception as e:
        debug_print(f"Complete failure: {e}")