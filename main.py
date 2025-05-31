import sys
import types

# Patch distutils.version.LooseVersion using packaging.version.Version
try:
    from packaging.version import Version

    distutils_module = types.ModuleType("distutils.version")
    distutils_module.LooseVersion = Version
    sys.modules["distutils.version"] = distutils_module

except ImportError:
    print("Please install 'packaging' using: pip install packaging")
    sys.exit(1)

# Now safe to import undetected_chromedriver
import undetected_chromedriver as uc
import time

# Setup Chrome options
options = uc.ChromeOptions()

# Use your actual Chrome profile path
profile_path = "C:\\Users\\harry\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"
options.add_argument(f"--user-data-dir={profile_path}")

# Launch Chrome with your profile
driver = uc.Chrome(options=options, use_subprocess=True)

# Navigate to desired URL
driver.get("https://myaccount.google.com/")

# Keep browser open
time.sleep(100000)
