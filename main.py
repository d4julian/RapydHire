import asyncio
from config import load_user_profile
from linkedin_automation import LinkedInAutomation
from ai_parser import AIJobParser

async def main():
    user_profile = load_user_profile("assets/config.yaml")
    
    ai_parser = AIJobParser()
    
    while True:
        jobs = []
        
        for job in jobs:
            parsed_job = await ai_parser.parse_job_description(job.description)
            
            if job.is_easy_apply and is_job_suitable(parsed_job, user_profile):
                linkedin_bot.apply_to_job(job.url)
        
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
