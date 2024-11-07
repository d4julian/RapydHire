from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from config import user_profile, app_config
import time
import os  # Added import
from job import Job

class LinkedInAutomation:

    def __init__(self):
        self.driver = None  # Initialize driver to None

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
            self.search_jobs(timeout=timeout)
        except TimeoutException:
            print("Login timed out. Please try again.")
            self.driver.quit()
            raise Exception("Login timed out")
    
    def scroll_to_bottom(self):
        # Scroll to bottom of page
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for page to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def createQuery(self, app_config: AppConfig) -> str:
        query_parts = "https://www.linkedin.com/jobs/search/?"
        
        # Add position titles first
        if app_config.position: query_parts.append(f"keywords={'+'.join(app_config.position)}&f_AL=true")
        query_parts.append(f"&distance={app_config.distance}")
        
        # Add work preferences
        if app_config.remote or app_config.hybrid or app_config.onsite:
            site_string = "&f_WT=2"
            if app_config.onsite: site_string += "1,"
            if app_config.remote: site_string += "2,"
            if app_config.hybrid: site_string += "3,"
            query_parts.append(site_string[:-1])  # Remove trailing comma        
        # Add experience levels
        if app_config.experience_levels:
            experience_string = "&f_E="
            if app.config.experience_levels["internship"]: experience_string += "1,"
            if app_config.experience_levels["entry_level"]: experience_string += "2,"
            if app_config.experience_levels["associate"]: experience_string += "3,"
            if app_config.experience_levels["mid_senior_level"]: experience_string += "4,"
            if app_config.experience_levels["director"]: experience_string += "5,"
            if app_config.experience_levels["executive"]: experience_string += "6,"
            query_parts.append(experience_string[:-1])
        # Add distance
        query_parts.append(f"&distance={app_config.distance}")
        # Add locations
        if app_config.locations: query_parts.append(f"&location={'+'.join(app_config.locations[0])}")
        # Add job types
        if app_config.job_types:
            job_type_string = "&f_JT="
            if app_config.job_types["full_time"]: job_type_string += "F,"
            if app_config.job_types["part_time"]: job_type_string += "P,"
            if app_config.job_types["contract"]: job_type_string += "C,"
            if app_config.job_types["internship"]: job_type_string += "I,"
            query_parts.append(job_type_string[:-1])
        # Add date posted
        if app_config.date_posted:
            date_string = "&f_TPR="
            if app_config.date_posted["24_hours"]: date_string += "r86400,"
            elif app_config.date_posted["week"]: date_string += "r604800,"
            elif app_config.date_posted["month"]: date_string += "r2592000,"
            elif app_config.date_posted["any_time"]: date_string = ""
            query_parts.append("" if date_string == "" else date_string[:-1])
        
        
        
        # Join all parts with &
        return ''.join(query_parts)

    def search(self, query: str):
        formatted_query = query.replace(' ', '+')
        base_url = "https://www.linkedin.com/jobs/search/?"
        params = {
            'keywords': formatted_query,
            'distance': f"{app_config.distance}.0",
            'f_WT': 2 if app_config.remote else None,  # 2 is LinkedIn's code for remote jobs
        }
        
        # Build URL with & before each parameter
        
        self.driver.get(createQuery(app_config))

    def search_jobs(self, timeout=60) -> List[Job]:
        self.driver.get("https://www.linkedin.com/jobs/")
        try:
            logger.info("Searching for jobs...")
            print(f"Attempting to load jobs page...")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search jobs']")))
            print(f"Jobs page loaded successfully!")
            self.scroll_to_bottom()
        
            job_cards = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'job-card-container')]")
            
            print("Reached bottom of page")
        except TimeoutException:
            print(f"Jobs page failed to load. Please try again.")
            self.driver.quit()
            raise Exception("Jobs page failed to load")
        return []

    def apply_to_job(self, job_url: str):
        self.driver.get(job_url)
        # TODO: Implement job application logic
        
    def __del__(self):
        if self.driver is not None: self.driver.quit()
