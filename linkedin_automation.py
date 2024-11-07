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
        # Scroll back to top of page
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)  # Wait for page to load

    def createQuery(self) -> str:
        query_parts = ["https://www.linkedin.com/jobs/search/?"]
        
        # Add position titles first
        if app_config.position: query_parts.append(f"keywords={app_config.position.replace(' ', '+')}&f_AL=true")
        query_parts.append(f"&distance={app_config.distance}")
        
        # Add work preferences
        if app_config.remote or app_config.hybrid or app_config.onsite:
            site_string = "&f_WT=2"
            if app_config.onsite: site_string += "1,"
            if app_config.remote: site_string += "2,"
            if app_config.hybrid: site_string += "3,"
            query_parts.append(site_string[:-1])  # Remove trailing comma        
        # Add experience levels
        if app_config.experience_level:
            experience_string = "&f_E="
            if app_config.experience_level["internship"]: experience_string += "1,"
            if app_config.experience_level["entry_level"]: experience_string += "2,"
            if app_config.experience_level["associate"]: experience_string += "3,"
            if app_config.experience_level["mid_senior_level"]: experience_string += "4,"
            if app_config.experience_level["director"]: experience_string += "5,"
            if app_config.experience_level["executive"]: experience_string += "6,"
            query_parts.append(experience_string[:-1])
        # Add distance
        query_parts.append(f"&distance={app_config.distance}")
        # Add locations
        if app_config.locations: query_parts.append(f"&location={''.join(app_config.locations[0])}")
        # Add job types
        if app_config.job_types:
            job_type_string = "&f_JT="
            if app_config.job_types["full_time"]: job_type_string += "F,"
            if app_config.job_types["part_time"]: job_type_string += "P,"
            if app_config.job_types["contract"]: job_type_string += "C,"
            if app_config.job_types["internship"]: job_type_string += "I,"
            query_parts.append(job_type_string[:-1])
        # Add date posted
        if app_config.date:
            date_string = "&f_TPR="
            if app_config.date["24_hours"]: date_string += "r86400,"
            elif app_config.date["week"]: date_string += "r604800,"
            elif app_config.date["month"]: date_string += "r2592000,"
            elif app_config.date["any_time"]: date_string = ""
            query_parts.append("" if date_string == "" else date_string[:-1])
        
        print(f"Query: {''.join(query_parts)}")
        return ''.join(query_parts)

    def search_jobs(self, timeout=60):
        time.sleep(2)
        jobs = []
        self.driver.get(self.createQuery())
        try:
            print("Attempting to load jobs page...")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'jobs-search__job-details')]")))
            print("Jobs page loaded successfully!")
            self.scroll_to_bottom()
        
            job_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'job-card-list')]")

            for card in job_cards:
                card.click()
                job = Job(
                    title=self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-title')]").text, 
                    company=self.driver.find_element(By.XPATH, "//div[contains(@class, 'company-name')]").text)
                print(f"Checking job: {job.title} at {job.company}...")
                if any(existing_job.company == job.company for existing_job in jobs):
                    print("Already applied at this company. Skipping...")
                    continue

                if job.company in job_cards:
                    print("Job already applied to. Skipping...")
                    continue

                easy_apply = False
                applied = False
                for element in card.find_elements(By.XPATH, "//*"):
                    if element.text == "Applied":
                        applied = True
                        break
                    if element.text == "Easy Apply": easy_apply = True

                if not easy_apply or applied: 
                    print("Job already applied to. Skipping..." if applied else "Job does not have Easy Apply. Skipping...")
                    continue

                print("hi")

                job.description = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(By.XPATH, "//div[contains(@class, 'jobs-description-content__text')]")).text

                # easy_apply_jobs.append(job)
                print(f"Attempting to apply: {job.title} at {job.company}")
                jobs.append(job)
                if not self.click_apply_button():
                    print("Failed to find Easy Apply button. Skipping...")
                    continue
                time.sleep(2)
            
            print("Reached bottom of page")
        except TimeoutException:
            print(f"Jobs page failed to load. Please try again.")
            self.driver.quit()
            raise Exception("Jobs page failed to load")
        return jobs

    def click_apply_button(self) -> bool:
        search_methods = [
            {
                'description': "find all 'Easy Apply' buttons using find_elements",
                'find_elements': True,
                'xpath': '//button[contains(@class, "jobs-apply-button") and contains(., "Easy Apply")]'
            },
            {
                'description': "'aria-label' containing 'Easy Apply to'",
                'xpath': '//button[contains(@aria-label, "Easy Apply to")]'
            },
            {
                'description': "button text search",
                'xpath': '//button[contains(text(), "Easy Apply") or contains(text(), "Apply now")]'
            }
        ]
        for method in search_methods:
            try:
                if method.get('find_elements'):
                    buttons = self.driver.find_elements(By.XPATH, method.get('xpath'))
                else:
                    buttons = [self.driver.find_element(By.XPATH, method.get('xpath'))]
                if len(buttons) > 0:
                    print(f"Found {len(buttons)} buttons using {method.get('description')}")
                    for button in buttons:
                        button.click()
                        return True
            except Exception as e:
                print(f"Error occurred while trying to find buttons using {method.get('description')}: {e}")
                return False
        
        return False

    def apply_to_job(self, job: Job):
        print(f"Attempting to apply to job: {job.title} at {job.company}")
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]")))

        button.click()
        time.sleep(5)
        
        
    def __del__(self):
        if self.driver is not None: self.driver.quit()
