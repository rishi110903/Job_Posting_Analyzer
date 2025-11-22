"""
Configuration settings for Job Posting Analyzer
"""

# User Agent to mimic browser requests (prevents blocking)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Request timeout (seconds)
TIMEOUT = 10

# Comprehensive Skills Database
SKILLS_DATABASE = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 
        'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r'
    ],
    'web_frameworks': [
        'django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'nodejs',
        'express', 'spring', 'laravel', 'rails'
    ],
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
        'dynamodb', 'cassandra', 'elasticsearch'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean'
    ],
    'devops_tools': [
        'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions',
        'terraform', 'ansible', 'ci/cd'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch',
        'scikit-learn', 'pandas', 'numpy', 'jupyter'
    ],
    'general_tools': [
        'git', 'jira', 'confluence', 'slack', 'agile', 'scrum'
    ]
}

# Flatten all skills into a single list for easy access
ALL_SKILLS = []
for category, skills in SKILLS_DATABASE.items():
    ALL_SKILLS.extend(skills)