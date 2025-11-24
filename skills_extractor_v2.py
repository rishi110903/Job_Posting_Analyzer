"""
Enhanced Skills Extractor using spaCy NLP
Handles skill variations, compound terms, and context
"""

import re
import spacy
from config import SKILLS_DATABASE, ALL_SKILLS


class EnhancedSkillExtractor:
    """Enhanced skill extraction using NLP and pattern matching"""
    
    def __init__(self):
        """Initialize with spaCy model and skills database"""
        print("Loading spaCy NLP model...")
        try:
            self.nlp = spacy.load('en_core_web_sm')
            print("✓ spaCy model loaded successfully")
        except OSError:
            print("✗ spaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise
        
        self.skills_database = SKILLS_DATABASE
        self.all_skills = ALL_SKILLS
        self.skill_variations = self._build_skill_variations()
        
        print(f"✓ EnhancedSkillExtractor initialized with {len(self.all_skills)} base skills")
    
    def _build_skill_variations(self):
        """
        Build map of skill variations to canonical names
        
        Returns:
            dict: Mapping of variations to standard skill names
        """
        variations = {}
        
        # Common variations
        skill_patterns = {
            'python': ['python', 'python3', 'python2', 'python programming'],
            'javascript': ['javascript', 'js', 'ecmascript', 'es6', 'es2015'],
            'java': ['java', 'java programming', 'core java'],
            'c++': ['c++', 'cpp', 'c plus plus'],
            'c#': ['c#', 'csharp', 'c sharp'],
            'sql': ['sql', 'structured query language', 'tsql', 'plsql'],
            'machine learning': ['machine learning', 'ml', 'machine-learning'],
            'deep learning': ['deep learning', 'dl', 'deep-learning'],
            'docker': ['docker', 'containerization', 'docker containers'],
            'kubernetes': ['kubernetes', 'k8s', 'container orchestration'],
            'aws': ['aws', 'amazon web services', 'amazon aws'],
            'azure': ['azure', 'microsoft azure', 'ms azure'],
            'gcp': ['gcp', 'google cloud', 'google cloud platform'],
        }
        
        # Map all variations to canonical name
        for canonical, variants in skill_patterns.items():
            for variant in variants:
                variations[variant.lower()] = canonical
        
        # Add original skills as their own variations
        for skill in self.all_skills:
            if skill not in variations:
                variations[skill] = skill
        
        return variations
    
    def extract_skills(self, text):
        """
        Extract skills using NLP and pattern matching
        
        Args:
            text (str): Job posting text
            
        Returns:
            list: List of skills found
        """
        if not text:
            return []
        
        found_skills = set()
        text_lower = text.lower()
        
        # Method 1: Simple pattern matching (fast, catches obvious ones)
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Method 2: NLP-based extraction (catches variations)
        doc = self.nlp(text)
        
        # Extract noun chunks (compound terms like "machine learning")
        for chunk in doc.noun_chunks:
            chunk_lower = chunk.text.lower()
            
            # Check if chunk matches any skill variation
            if chunk_lower in self.skill_variations:
                canonical = self.skill_variations[chunk_lower]
                found_skills.add(canonical)
        
        # Extract proper nouns (technology names)
        for token in doc:
            if token.pos_ == 'PROPN':  # Proper noun
                token_lower = token.text.lower()
                if token_lower in self.skill_variations:
                    canonical = self.skill_variations[token_lower]
                    found_skills.add(canonical)
        
        print(f"✓ Found {len(found_skills)} unique skills")
        return sorted(list(found_skills))
    
    def extract_experience_level(self, text):
        """
        Extract required experience level from text
        
        Args:
            text (str): Job posting text
            
        Returns:
            dict: Experience information with years and level
        """
        experience_info = {
            'years': None,
            'level': None,
            'keywords': []
        }
        
        text_lower = text.lower()
        
        # Experience level keywords
        level_patterns = {
            'junior': r'\b(junior|entry.?level|graduate|fresher)\b',
            'mid-level': r'\b(mid.?level|intermediate|experienced)\b',
            'senior': r'\b(senior|lead|principal|staff)\b',
            'expert': r'\b(expert|architect|distinguished)\b'
        }
        
        for level, pattern in level_patterns.items():
            if re.search(pattern, text_lower):
                experience_info['level'] = level
                experience_info['keywords'].append(level)
        
        # Extract years of experience
        year_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\s*(?:to|-)\s*(\d+)\s*years?',
            r'(?:minimum|at least|min\.?)\s*(\d+)\s*years?',
            r'(\d+)\+\s*(?:years?|yrs?)',
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, text_lower)
            if match:
                years_str = match.group(1)
                full_match = match.group(0)
                
                if '+' in full_match:
                    experience_info['years'] = f"{years_str}+"
                else:
                    experience_info['years'] = int(years_str)
                
                break
        
        return experience_info
    
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
            category_skills = [s for s in skills_list if s in skills]
            
            if category_skills:
                categorized[category] = sorted(category_skills)
        
        return categorized
    
    def analyze_skills(self, text):
        """
        Complete analysis: extract skills, experience, and categorize
        
        Args:
            text (str): Job posting text
            
        Returns:
            dict: Complete analysis with skills, categories, and experience
        """
        # Extract skills
        skills = self.extract_skills(text)
        
        # Categorize
        categorized = self.categorize_skills(skills)
        
        # Extract experience level
        experience = self.extract_experience_level(text)
        
        # Return comprehensive result
        return {
            'total_skills': len(skills),
            'all_skills': skills,
            'categorized': categorized,
            'experience_required': experience
        }


# Test the enhanced extractor
if __name__ == "__main__":
    print("=" * 70)
    print("ENHANCED SKILLS EXTRACTOR TEST")
    print("=" * 70)
    print()
    
    # Create enhanced extractor
    extractor = EnhancedSkillExtractor()
    
    # Sample job posting with variations
    sample_text = """
    Senior Software Engineer - Machine Learning
    
    We are seeking an experienced ML engineer with strong Python programming
    skills. The ideal candidate will have 5+ years of experience working with
    Python3, deep learning frameworks like TensorFlow or PyTorch, and cloud
    platforms (AWS or GCP).
    
    Required Skills:
    - Expert in Python and JavaScript (ES6)
    - Experience with containerization (Docker, K8s)
    - Strong SQL and database design skills
    - Familiarity with CI/CD pipelines
    - Bachelor's degree in Computer Science
    
    Nice to have:
    - React or Angular experience
    - AWS certification
    - Machine-learning model deployment experience
    """
    
    print("Sample Job Text:")
    print("-" * 70)
    print(sample_text)
    print("-" * 70)
    print()
    
    # Analyze
    print("Running analysis...\n")
    analysis = extractor.analyze_skills(sample_text)
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n📊 Statistics:")
    print(f"   • Total skills: {analysis['total_skills']}")
    print(f"   • Categories: {len(analysis['categorized'])}")
    
    print(f"\n🔍 All Skills:")
    print(f"   {', '.join(analysis['all_skills'])}")
    
    print(f"\n👔 Experience Required:")
    exp = analysis['experience_required']
    if exp['years']:
        print(f"   • Years: {exp['years']}")
    if exp['level']:
        print(f"   • Level: {exp['level']}")
    
    print("\n" + "=" * 70)
    print("CATEGORIZED SKILLS")
    print("=" * 70)
    
    for category, skills in analysis['categorized'].items():
        print(f"\n📌 {category.replace('_', ' ').title()}:")
        for skill in skills:
            print(f"   • {skill}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
