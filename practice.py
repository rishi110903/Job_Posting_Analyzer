from config import SKILLS_DATABASE
job_text = "We need Python and SQL experience"

# Convert text to lowercase
text_lower = job_text.lower()  # "we need python and sql experience"

for category, skills in SKILLS_DATABASE.items():
    for skill in skills:
        if skill in text_lower:
            print(f"found: {skill}")