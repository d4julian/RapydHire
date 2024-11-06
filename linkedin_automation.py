from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import UserProfile

class LinkedInAutomation:
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.driver = None

    def login(self):
        pass

    def search_jobs(self):
        pass

    def apply_to_job(self, job_url: str):
        pass
