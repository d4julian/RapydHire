import asyncio
from config import load_user_profile, load_app_config
from linkedin_automation import LinkedInAutomation
from ai_parser import AIJobParser

def main():
    linkedin_bot = LinkedInAutomation()
    try:
        linkedin_bot.login()
        
        ai_parser = AIJobParser()


    except Exception as e:
        print(f"Error occurred: {e}")
        if linkedin_bot.driver:
            linkedin_bot.driver.quit()

if __name__ == "__main__":
    main()
