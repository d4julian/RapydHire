from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import yaml
from pathlib import Path

@dataclass
class PersonalInformation:
    first_name: str
    last_name: str
    email: str
    phone: str
    phone_prefix: str
    address: str
    city: str
    country: str
    zip_code: str
    date_of_birth: str
    github: Optional[str] = None
    linkedin: Optional[str] = None

@dataclass
class Education:
    education_level: str
    institution: str
    field_of_study: str
    final_evaluation_grade: str
    start_date: str
    year_of_completion: str
    exam: Optional[str] = None

@dataclass
class Experience:
    position: str
    company: str
    employment_period: str
    location: str
    industry: str
    key_responsibilities: List[Dict[str, str]]
    skills_acquired: List[str]

@dataclass
class Project:
    name: str
    description: str
    link: str

@dataclass
class Language:
    language: str
    proficiency: str

@dataclass
class WorkPreferences:
    remote_work: str
    in_person_work: str
    open_to_relocation: str
    willing_to_complete_assessments: str
    willing_to_undergo_drug_tests: str
    willing_to_undergo_background_checks: str

@dataclass
class UserProfile:
    personal_information: PersonalInformation
    education_details: List[Education]
    experience_details: List[Experience]
    projects: List[Project]
    achievements: List[str]
    certifications: List[str]
    languages: List[Language]
    interests: List[str]
    availability: Dict[str, str]
    salary_expectations: Dict[str, str]
    self_identification: Dict[str, str]
    legal_authorization: Dict[str, str]
    work_preferences: WorkPreferences

@dataclass
class AppConfig:
    remote: bool
    hybrid: bool
    onsite: bool
    experience_level: Dict[str, bool]
    job_types: Dict[str, bool]
    date: Dict[str, bool]
    position: str
    locations: List[str]
    apply_once_at_company: bool
    distance: int
    company_blacklist: List[str]
    title_blacklist: List[str]
    location_blacklist: List[str]
    job_applicants_threshold: Dict[str, int]
    llm_model: str
    llm_api_url: str

def load_user_profile(path: str) -> UserProfile:
    with open(Path(path), 'r') as f:
        data = yaml.safe_load(f)
    
    data['personal_information'] = PersonalInformation(**data['personal_information'])
    data['education_details'] = [Education(**edu) for edu in data['education_details']]
    data['experience_details'] = [Experience(**exp) for exp in data['experience_details']]
    data['projects'] = [Project(**proj) for proj in data['projects']]
    data['languages'] = [Language(**lang) for lang in data['languages']]
    data['work_preferences'] = WorkPreferences(**data['work_preferences'])
    
    return UserProfile(**data)

def load_app_config(path: str) -> AppConfig:
    with open(Path(path), 'r') as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)

app_config = load_app_config("assets/config.yaml")
user_profile = load_user_profile("assets/user.yaml")