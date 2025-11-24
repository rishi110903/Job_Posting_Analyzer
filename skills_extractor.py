"""
Skills Extractor (Version 1.0 - Day 3)

This is the original regex-based implementation.
Kept for comparison and as a fallback option.

For the enhanced NLP version, see: skills_extractor_v2.py

Accuracy: ~70%
Speed: Fast
Dependencies: None (only regex)
"""

import re
from config import SKILLS_DATABASE, ALL_SKILLS

class SkillExtractor:
    """Extracts technical skills from job posting text"""
    
    def __init__(self):
        self.skills_database = SKILLS_DATABASE
        self.all_skills = ALL_SKILLS
        
        print(f"SkillExtractor initialized with {len(self.all_skills)} skills")
    def extract_skills(self, text):
        """
        Extract skills from job posting text
        
        Args:
            text (str): Cleaned job posting text
            
        Returns:
            list: List of skills found (lowercase)
        """
        if not text:
            return []
        
        text_lower = text.lower()
        
        # Store found skills
        found_skills = []
        
        # Check each skill
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        print(f"✓ Found {len(found_skills)} skills")
        return found_skills
    
    def categorize_skills(self, skills_list):
        """
        Categorize skills by type
        
        Args:
            skills_list (list): List of skill names
            
        Returns:
            dict: Skills grouped by category
        """
        categorized = {}
        
        for category, skills in self.skills_database.items():
            # Find skills from this category in our list
            category_skills = [s for s in skills_list if s in skills]
            
            if category_skills:
                categorized[category] = category_skills
        
        return categorized
    def analyze_skills(self, text):
        """
        Complete analysis: extract and categorize skills
        
        Args:
            text (str): Job posting text
            
        Returns:
            dict: Complete analysis with skills and categories
        """
        # Extract all skills
        skills = self.extract_skills(text)
        
        # Categorize them
        categorized = self.categorize_skills(skills)
        
        # Return comprehensive result
        return {
            'total_skills': len(skills),
            'all_skills': skills,
            'categorized': categorized
        }
# Test the extractor
if __name__ == "__main__":
    print("=" * 60)
    print("SKILLS EXTRACTOR TEST")
    print("=" * 60)
    print()
    
    # Create extractor
    extractor = SkillExtractor()
    
    # Sample job posting text
    sample_text = """
    We are seeking a Software Engineer with expertise in Python 
    and SQL. Experience with AWS cloud platform is required.
    
    Required Skills:
    - Python programming (3+ years)
    - SQL database design
    - Docker and Kubernetes
    - Git version control
    - Django or Flask framework
    
    Nice to have:
    - Machine learning experience
    - React or Angular
    - CI/CD pipelines
    """
    
    print("Sample Job Text:")
    print("-" * 60)
    print(sample_text)
    print("-" * 60)
    print()
    
    # Extract skills
    print("Extracting skills...\n")
    skills = extractor.extract_skills(sample_text)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nTotal skills found: {len(skills)}")
    print(f"Skills: {', '.join(skills)}")
    
    # Categorize
    print("\n" + "-" * 60)
    print("CATEGORIZED SKILLS")
    print("-" * 60)
    
    categorized = extractor.categorize_skills(skills)
    for category, skill_list in categorized.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for skill in skill_list:
            print(f"  • {skill}")
    
    # Full analysis
    print("\n" + "=" * 60)
    print("COMPLETE ANALYSIS")
    print("=" * 60)
    
    analysis = extractor.analyze_skills(sample_text)
    print(f"\nTotal: {analysis['total_skills']} skills")
    print(f"Categories: {len(analysis['categorized'])}")

