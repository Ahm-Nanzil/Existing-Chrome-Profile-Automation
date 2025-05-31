import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()

# Use your full Chrome "User Data" directory, not just the profile folder
user_data_dir = "C:\\Users\\harry\\AppData\\Local\\Google\\Chrome\\User Data"
profile_dir = "Profile 4"

options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_dir}")

driver = uc.Chrome(options=options, use_subprocess=True)

driver.get("https://myaccount.google.com/")
time.sleep(100000)
