import asyncio
from config import load_user_profile
from linkedin_automation import LinkedInAutomation
from ai_parser import AIJobParser

async def main():
    user_profile = load_user_profile("assets/config.yaml")
    
    linkedin_bot = LinkedInAutomation(user_profile)
    try:
        linkedin_bot.login()
        print("Successfully logged in! Starting job search...")
        
        ai_parser = AIJobParser()
    
        while True:
            try:
                jobs = linkedin_bot.search_jobs()
                
                for job in jobs:
                    parsed_job = await ai_parser.parse_job_description(job.description)
                    
                    if job.is_easy_apply and is_job_suitable(parsed_job, user_profile):
                        linkedin_bot.apply_to_job(job.url)
                
                await asyncio.sleep(3600)  # Wait an hour before next search
            except Exception as e:
                print(f"Error occurred: {e}")
                linkedin_bot.login()  # Attempt to re-login if session expired

    except Exception as e:
        print(f"Error occurred: {e}")
        if linkedin_bot.driver:
            linkedin_bot.driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
