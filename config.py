from dataclasses import dataclass
from typing import List, Optional
import yaml
from pathlib import Path

@dataclass
class UserProfile:
    email: str
    phone: str
    full_name: str
    location: str
    resume_path: str
    linkedin_email: str
    linkedin_password: str
    years_of_experience: int
    education: List[dict]
    work_experience: List[dict]
    skills: List[str]
    desired_job_titles: List[str]
    preferred_locations: List[str]
    minimum_salary: Optional[int] = None

def load_user_profile(config_path: str) -> UserProfile:
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
    return UserProfile(**data)