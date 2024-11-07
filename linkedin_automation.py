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
            # Wait for job list to load
            job_list = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
            )
            time.sleep(2)  # Wait for page to load
            print("Jobs page loaded successfully!")
            self.scroll_to_bottom()

            # Get all job cards
            job_cards = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".job-card-list")
                )
            )

            for card in job_cards:
                try:
                    # Wait for card to be clickable
                    print(1)
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(card)
                    ).click()
                    time.sleep(2)  # Wait for job details to load
                    print(1)

                    # Get job details with explicit waits
                    title = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title")
                        )
                    ).text
                    print(1)
                    company = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name")
                        )
                    ).text
                    print(1)

                    job = Job(title=title, company=company)
                    print(f"Checking job: {job.title} at {job.company}...")

                    if any(existing_job.company == job.company and existing_job.title == job.title for existing_job in jobs):
                        print("Already applied at this company. Skipping...")
                        continue

                    # Check if job is already applied to or has Easy Apply
                    easy_apply_button = self.driver.find_elements(
                        By.CSS_SELECTOR, 
                        "button.jobs-apply-button[aria-label*='Easy Apply']"
                    )
                    
                    if not easy_apply_button:
                        print("Job does not have Easy Apply. Skipping...")
                        continue

                    # Get job description
                    description = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".jobs-description-content__text")
                        )
                    ).text
                    job.description = description

                    jobs.append(job)
                    print(f"Found applicable job: {job.title} at {job.company}")
                    self.click_apply_button()

                except TimeoutException:
                    print("Timeout while processing job card. Skipping...")
                    continue
                except Exception as e:
                    print(f"Error processing job card: {e}")
                    continue

            print(f"Found {len(jobs)} potential jobs to apply to")
            return jobs

        except TimeoutException:
            print("Jobs page failed to load. Please try again.")
            raise
        except Exception as e:
            print(f"Error during job search: {e}")
            return []

    def apply_to_job(self, job: Job):
        try:
            self.click_apply_button()
            print(f"Attempting to apply to job: {job.title} at {job.company}")
            time.sleep(5)
        # Fill out application form
            while True:
                dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "div[data-test-text-entity-list-form-component]")
                text_inputs = self.driver.find_elements(By.CLASS_NAME, "artdeco-text-input--container")

                for dropdown in dropdowns:
                    label = dropdown.find_element(By.TAG_NAME, "label").text
                    select = dropdown.find_element(By.TAG_NAME, "select")
                    options = select.find_elements(By.TAG_NAME, "option")

                    # Logic to select dropdown option
                    options[0].click()
                    time.sleep(2)

                for text_input in text_inputs:
                    label = text_input.find_element(By.TAG_NAME, "label").text
                    input_field = text_input.find_element(By.TAG_NAME, "input")

                    # Logic to fill out text input
                    input_field.send_keys("Test")
                    time.sleep(2)


                upload_button = self.driver.find_element(By.CSS_SELECTOR, 
                    "button[aria-label='Upload resume button. Only, DOC, DOCX, PDF formats are supported. Max file size is (2 MB).']")
                
                if upload_button:
                    upload_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                    upload_button.send_keys(os.path.abspath(".\\assets\\resume.pdf"))
                    print("Resume uploaded successfully!")
                    time.sleep(2)
                
                # Click next button
                next_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-easy-apply-next-button]")
                if not next_button: break
                next_button.click()
                time.sleep(2)
        
            # Review application
            review_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Review your application"]')
            if not review_button: return False
            review_button.click()
            time.sleep(2)
            
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Submit application"]')
            if not submit_button: return False
            submit_button.click()

        except Exception as e:
            print(f"Error applying to job: {e}")
            return False


    def select_dropdown_option(self, dropdown: str, option: str):
        pass

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
        
        
    def __del__(self):
        if self.driver is not None: self.driver.quit()
