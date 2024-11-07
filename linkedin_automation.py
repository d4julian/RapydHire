from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from config import UserProfile, AppConfig
import time
import os  # Added import

class LinkedInAutomation:

    def __init__(self):
        self.initialize_driver()

    def initialize_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")

        user_data_dir = "selenium_profile"
        chrome_options.add_argument(f"--user-data-dir={os.path.abspath(user_data_dir)}")
        chrome_options.add_argument("--profile-directory=Default")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Chrome driver initialized successfully! Running version: {self.driver.capabilities['browserVersion']}")


    def login(self, timeout=60):
        self.driver.get("https://www.linkedin.com/login")

        print("Please sign in manually to your LinkedIn account. You have 60 seconds before this session times out...")
        
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains("linkedin.com/feed"))
            print("Login successful!")
            self.search_jobs()
        except TimeoutException:
            print("Login timed out. Please try again.")
            self.driver.quit()
            raise Exception("Login timed out")
        

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
        if self.driver is not None:
            self.driver.quit()
