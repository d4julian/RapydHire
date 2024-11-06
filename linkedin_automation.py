from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from config import UserProfile
import time

class LinkedInAutomation:
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.driver = None

    def initialize_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
        chrome_options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self):
        self.initialize_driver()
        self.driver.get("https://www.linkedin.com")
        
        print("Please sign in manually to your LinkedIn account.")
        print("After signing in, press Enter to continue...")
        input()
        
        # Verify login status
        self.verify_login()
        print("Login verified successfully!")

    def verify_login(self, max_attempts=3):
        attempts = 0
        while attempts < max_attempts:
            try:
                # Try to find an element that's only visible when logged in
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-identity-module, .global-nav"))
                )
                return True
            except TimeoutException:
                attempts += 1
                if attempts < max_attempts:
                    print("Login not detected. Please ensure you're logged in.")
                    print("Press Enter when ready...")
                    input()
                else:
                    raise Exception("Failed to verify login after multiple attempts")

    def search_jobs(self):
        self.driver.get("https://www.linkedin.com/jobs/")
        time.sleep(2)  # Allow page to load
        
        jobs = []
        # TODO: Implement job search based on user_profile.desired_job_titles
        # and user_profile.preferred_locations
        return jobs

    def apply_to_job(self, job_url: str):
        self.driver.get(job_url)
        # TODO: Implement job application logic
        
    def __del__(self):
        if self.driver:
            self.driver.quit()
