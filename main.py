import asyncio
from config import user_profile, app_config
from linkedin_automation import LinkedInAutomation
from ai_parser import AIJobParser

def main():
    linkedin_bot = LinkedInAutomation()
    try:
        linkedin_bot.login()
        
        


    except Exception as e: 
        print(f"Error occurred: {e}")
    finally:
        if linkedin_bot.driver: linkedin_bot.__del__()
if __name__ == "__main__":
    main()
