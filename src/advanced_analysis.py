"""
Advanced analysis functions for resume scoring, skill matching, and analytics
"""
import re
from typing import Dict, List, Tuple
import json


def calculate_ats_score(resume_text: str) -> Dict[str, any]:
    """
    Calculate ATS (Applicant Tracking System) compatibility score
    
    Args:
        resume_text: Resume text content
        
    Returns:
        Dictionary with score and breakdown
    """
    score = 0
    max_score = 100
    breakdown = {}
    
    # Check for contact information (20 points)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    has_email = bool(re.search(email_pattern, resume_text))
    has_phone = bool(re.search(phone_pattern, resume_text))
    
    contact_score = 0
    if has_email:
        contact_score += 10
    if has_phone:
        contact_score += 10
    
    breakdown['contact_info'] = contact_score
    score += contact_score
    
    # Check for section headers (20 points)
    common_sections = [
        r'experience|work history',
        r'education|qualification',
        r'skills|technical skills',
        r'projects|portfolio'
    ]
    
    section_score = 0
    for section in common_sections:
        if re.search(section, resume_text, re.IGNORECASE):
            section_score += 5
    
    breakdown['section_headers'] = section_score
    score += section_score
    
    # Check for dates (15 points)
    date_patterns = [
        r'\b(19|20)\d{2}\b',  # Year
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(19|20)\d{2}\b',  # Month Year
        r'\b\d{1,2}/\d{1,2}/(19|20)\d{2}\b'  # MM/DD/YYYY
    ]
    
    date_count = sum(len(re.findall(pattern, resume_text, re.IGNORECASE)) for pattern in date_patterns)
    date_score = min(15, date_count * 3)
    breakdown['dates'] = date_score
    score += date_score
    
    # Check for action verbs (20 points)
    action_verbs = [
        'developed', 'created', 'managed', 'led', 'designed', 'implemented',
        'built', 'achieved', 'improved', 'increased', 'reduced', 'optimized',
        'coordinated', 'analyzed', 'established', 'maintained'
    ]
    
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    verb_score = min(20, verb_count * 2)
    breakdown['action_verbs'] = verb_score
    score += verb_score
    
    # Check for quantifiable achievements (15 points)
    number_pattern = r'\d+%|\d+\+|[\$€£]\d+|\d+[kK]\+?'
    achievement_count = len(re.findall(number_pattern, resume_text))
    achievement_score = min(15, achievement_count * 3)
    breakdown['quantifiable_achievements'] = achievement_score
    score += achievement_score
    
    # Length check (10 points)
    word_count = len(resume_text.split())
    if 300 <= word_count <= 1500:
        length_score = 10
    elif 200 <= word_count < 300 or 1500 < word_count <= 2000:
        length_score = 5
    else:
        length_score = 2
    
    breakdown['optimal_length'] = length_score
    score += length_score
    
    return {
        'total_score': min(score, max_score),
        'max_score': max_score,
        'breakdown': breakdown,
        'grade': get_grade(score)
    }


def extract_skills(resume_text: str, from_ai: str = None) -> Dict[str, List[str]]:
    """
    Extract technical and soft skills from resume
    
    Args:
        resume_text: Resume text
        from_ai: Additional skills extracted by AI
        
    Returns:
        Dictionary categorizing skills
    """
    # Common technical skills
    tech_skills_keywords = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'sql', 'nosql',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
        'machine learning', 'ai', 'deep learning', 'tensorflow', 'pytorch',
        'html', 'css', 'mongodb', 'postgresql', 'mysql', 'redis',
        'rest api', 'graphql', 'microservices', 'agile', 'scrum'
    ]
    
    # Soft skills
    soft_skills_keywords = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'analytical', 'creative', 'adaptable', 'time management',
        'collaboration', 'critical thinking', 'decision making'
    ]
    
    text_lower = resume_text.lower()
    
    technical_skills = [skill for skill in tech_skills_keywords if skill.lower() in text_lower]
    soft_skills = [skill for skill in soft_skills_keywords if skill.lower() in text_lower]
    
    # Add AI-extracted skills if provided
    if from_ai:
        ai_skills = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', from_ai)
        technical_skills.extend([s for s in ai_skills if s.lower() not in [t.lower() for t in technical_skills]])
    
    return {
        'technical': list(set(technical_skills)),
        'soft': list(set(soft_skills)),
        'total_count': len(set(technical_skills)) + len(set(soft_skills))
    }


def calculate_job_match_score(resume_skills: List[str], job_title: str, job_description: str = "") -> int:
    """
    Calculate how well resume matches with a job posting
    
    Args:
        resume_skills: List of skills from resume
        job_title: Job title
        job_description: Job description text
        
    Returns:
        Match score (0-100)
    """
    score = 0
    job_text = (job_title + " " + job_description).lower()
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    # Count matching skills
    matches = sum(1 for skill in resume_skills_lower if skill in job_text)
    
    if len(resume_skills) > 0:
        score = min(100, int((matches / len(resume_skills)) * 100))
    
    # Bonus for title keywords
    title_words = job_title.lower().split()
    title_matches = sum(1 for word in title_words if word in ' '.join(resume_skills_lower))
    score = min(100, score + (title_matches * 5))
    
    return score


def get_grade(score: int) -> str:
    """Convert numerical score to letter grade"""
    if score >= 90:
        return 'A+'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B+'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    else:
        return 'D'


def estimate_salary_range(job_title: str, location: str = "India") -> Dict[str, str]:
    """
    Estimate salary range based on job title and location
    
    Args:
        job_title: Job title
        location: Location
        
    Returns:
        Dictionary with salary estimates
    """
    title_lower = job_title.lower()
    
    # Salary ranges for India (in LPA - Lakhs Per Annum)
    salary_ranges = {
        'intern': {'min': '1.5', 'max': '3', 'avg': '2.5'},
        'junior': {'min': '3', 'max': '6', 'avg': '4.5'},
        'software engineer': {'min': '4', 'max': '12', 'avg': '7'},
        'senior': {'min': '12', 'max': '25', 'avg': '18'},
        'lead': {'min': '20', 'max': '40', 'avg': '28'},
        'manager': {'min': '25', 'max': '50', 'avg': '35'},
        'architect': {'min': '30', 'max': '60', 'avg': '42'},
        'director': {'min': '40', 'max': '80', 'avg': '55'},
        'data scientist': {'min': '6', 'max': '20', 'avg': '12'},
        'devops': {'min': '5', 'max': '18', 'avg': '10'},
        'full stack': {'min': '5', 'max': '15', 'avg': '9'},
        'frontend': {'min': '4', 'max': '12', 'avg': '7'},
        'backend': {'min': '5', 'max': '14', 'avg': '8.5'},
    }
    
    # Find matching salary range
    for key, value in salary_ranges.items():
        if key in title_lower:
            return {
                'min': value['min'] + ' LPA',
                'max': value['max'] + ' LPA',
                'avg': value['avg'] + ' LPA',
                'currency': 'INR'
            }
    
    # Default range
    return {
        'min': '4 LPA',
        'max': '12 LPA',
        'avg': '7 LPA',
        'currency': 'INR'
    }


def generate_interview_tips(job_title: str, skills: List[str]) -> List[str]:
    """
    Generate interview preparation tips based on job role
    
    Args:
        job_title: Job title
        skills: List of required skills
        
    Returns:
        List of interview tips
    """
    tips = [
        "📚 Review STAR method (Situation, Task, Action, Result) for behavioral questions",
        "💡 Prepare examples of your past projects and achievements",
        "🤔 Practice explaining complex technical concepts in simple terms",
    ]
    
    title_lower = job_title.lower()
    
    # Role-specific tips
    if 'data' in title_lower or 'ml' in title_lower or 'ai' in title_lower:
        tips.extend([
            "📊 Be ready to discuss your data analysis projects and methodologies",
            "🧮 Brush up on statistics, probability, and machine learning algorithms",
            "💻 Practice SQL queries and data manipulation problems"
        ])
    elif 'frontend' in title_lower or 'react' in title_lower or 'ui' in title_lower:
        tips.extend([
            "🎨 Prepare your portfolio of UI/UX projects",
            "⚛️ Review React/Vue/Angular lifecycle and hooks",
            "📱 Discuss responsive design and browser compatibility"
        ])
    elif 'backend' in title_lower or 'api' in title_lower:
        tips.extend([
            "🔧 Review RESTful API design principles",
            "🗄️ Discuss database design and optimization",
            "🔐 Understand authentication, authorization, and security best practices"
        ])
    elif 'devops' in title_lower or 'sre' in title_lower:
        tips.extend([
            "☁️ Review CI/CD pipeline concepts",
            "🐳 Discuss containerization and orchestration (Docker, Kubernetes)",
            "📊 Understand monitoring, logging, and alerting strategies"
        ])
    elif 'full stack' in title_lower:
        tips.extend([
            "🌐 Be prepared for both frontend and backend questions",
            "🔄 Discuss your experience with complete project lifecycle",
            "🛠️ Review system design fundamentals"
        ])
    else:
        tips.extend([
            "🔍 Research the company's products and recent news",
            "💬 Prepare thoughtful questions to ask the interviewer",
            "🎯 Highlight projects relevant to the job description"
        ])
    
    # Add skills-specific tips
    if 'python' in [s.lower() for s in skills]:
        tips.append("🐍 Review Python data structures and common libraries")
    if any(cloud in [s.lower() for s in skills] for cloud in ['aws', 'azure', 'gcp']):
        tips.append("☁️ Discuss your cloud architecture experience and cost optimization")
    
    return tips[:8]  # Return top 8 tips
