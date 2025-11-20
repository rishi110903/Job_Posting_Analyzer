# Job Posting Analyzer - Week 1 Complete Learning Guide

**Project Goal:** Build a real, production-ready Job Posting Analyzer that extracts skills from job postings.

**Week 1 Focus:** Foundation - Understand the problem, set up tools, build the scraping component

**Time Commitment:** 2-4 hours/day × 7 days = 14-28 hours total

---

## DAY 1: Project Setup + Problem Deep Dive

### What You'll Do Today
- [ ] Set up project folder and Git repository
- [ ] Understand the problem you're solving
- [ ] Plan your project architecture
- [ ] Write your first documentation

### Step 1: Create Project Folder (10 minutes)

Open your terminal/command prompt and run:

```bash
cd Desktop  # or wherever you want the project
mkdir job-posting-analyzer
cd job-posting-analyzer
git init
```

This creates a new Git repository for your project.

### Step 2: Create Initial Project Structure (5 minutes)

Create these folders and files:

```
job-posting-analyzer/
├── README.md
├── requirements.txt
├── config.py
├── scraper.py
├── skills_extractor.py
├── main.py
└── .gitignore
```

**In your terminal, create them:**

```bash
touch README.md requirements.txt config.py scraper.py skills_extractor.py main.py .gitignore
```

### Step 3: Write Your Project README (30 minutes)

Open `README.md` in VS Code and write:

```markdown
# Job Posting Analyzer

## Problem Statement
Job seekers waste time manually reading job postings to understand what skills are required. This tool automates the extraction of skills, experience levels, and key requirements from job postings.

## Goals for This Project
1. Extract text from job posting URLs
2. Identify and categorize required skills
3. Determine experience level required
4. Output structured data (JSON format)

## Tech Stack
- **Python 3.9+**: Core language
- **BeautifulSoup4**: Web scraping HTML content
- **Requests**: Making HTTP requests
- **spaCy**: NLP for entity recognition
- **JSON**: Data serialization

## Why These Technologies?
- **BeautifulSoup** over Selenium: Faster for static HTML, perfect for job postings
- **spaCy** over NLTK: Better pre-trained models, faster processing
- **JSON output**: Standard format for data interchange

## High-Level Architecture

```
User Input (Job URL)
         ↓
Scraper Component (fetch HTML)
         ↓
Data Cleaning (remove noise)
         ↓
NLP Component (extract skills)
         ↓
Categorization (group by type)
         ↓
JSON Output (display results)
```

## Project Phases
- **Phase 1 (Week 1):** Scraping component - fetch and clean job posting text
- **Phase 2 (Week 2):** NLP component - extract skills using spaCy
- **Phase 3 (Week 3):** API + Deployment - create REST API and deploy

## What I'll Learn
- Web scraping fundamentals
- Data cleaning with Python
- NLP basics with spaCy
- API development with FastAPI
- Deployment to cloud

## Repository Structure
- `scraper.py`: Contains code to fetch and parse job postings
- `skills_extractor.py`: Contains NLP logic to extract skills
- `main.py`: Entry point, orchestrates the flow
- `config.py`: Configuration settings

## How to Run (Will be updated after completion)
```bash
pip install -r requirements.txt
python main.py
```

## Demo Link (Will be added after deployment)
Coming soon...

## What Challenges Do I Expect?
1. Different HTML structures across job sites (LinkedIn, Indeed, Naukri)
2. Skill name variations (Python vs Python3 vs Python programming)
3. Rate limiting from websites
4. Accuracy of NLP model

## Next Steps
- Set up development environment
- Build scraper for one job site
- Test on real job postings
```

**Save this file.** This README proves you're thinking about the problem, not just coding randomly.

### Step 4: Set Up .gitignore (5 minutes)

Create `.gitignore` file (tells Git what to ignore):

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
.env

# Project specific
*.log
test_output/
data/
```

**Why?** You don't want to upload unnecessary files to GitHub.

### Step 5: Create Initial requirements.txt (5 minutes)

This file lists all Python libraries you'll use. Create `requirements.txt`:

```
requests==2.31.0
beautifulsoup4==4.12.2
spacy==3.7.2
python-dotenv==1.0.0
```

**What are these?**
- `requests`: For fetching web pages
- `beautifulsoup4`: For parsing HTML
- `spacy`: For NLP
- `python-dotenv`: For managing configuration

### Step 6: First Git Commit (5 minutes)

In terminal, run:

```bash
git add .
git commit -m "Initial project setup with documentation"
```

**What you learned today:**
- Created a proper project structure
- Wrote clear documentation BEFORE coding
- Set up version control (Git)
- Planned your architecture before building

---

## DAY 2: Python Environment Setup + First Test

### What You'll Do Today
- [ ] Install Python libraries
- [ ] Create first working script
- [ ] Test that everything works
- [ ] Make your first HTTP request

### Step 1: Install Required Libraries (10 minutes)

In terminal, run:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

The second command downloads the English language model for spaCy.

### Step 2: Create config.py (5 minutes)

Open `config.py` and write:

```python
# Configuration file for Job Posting Analyzer

# URLs to test with
TEST_URLS = {
    'naukri': 'https://www.naukri.com/job-listings-python-developer-fresher-0-3-years-bangalore-0?k=python%20developer&l=bangalore&exp=0,3&jobAge=7&pageNo=1',
    'indeed': 'https://www.indeed.com/jobs?q=python+developer&l=india&fromage=7'
}

# Headers to avoid being blocked (pretend we're a browser)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# NLP Model
NLP_MODEL = 'en_core_web_sm'

# Skills dictionary (we'll expand this later)
TECHNICAL_SKILLS = [
    'python', 'java', 'javascript', 'react', 'angular', 'node.js',
    'sql', 'mongodb', 'postgresql', 'mysql', 'redis',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes',
    'git', 'jenkins', 'gitlab', 'fastapi', 'flask', 'django',
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch',
    'html', 'css', 'rest api', 'graphql', 'microservices'
]
```

**Why?**
- Centralized configuration (easy to change later)
- User-Agent header prevents websites from blocking us
- Skills list for manual skill detection (backup to NLP)

### Step 3: Test Internet Connection + Scraping (15 minutes)

Create a test file called `test_scraper.py`:

```python
import requests
from config import HEADERS, TEST_URLS

# Step 1: Make an HTTP request
print("Testing internet connection...")
try:
    response = requests.get('https://www.google.com', headers=HEADERS, timeout=5)
    print(f"✓ Internet working! Status code: {response.status_code}")
except Exception as e:
    print(f"✗ Internet error: {e}")
    exit()

# Step 2: Try fetching a job posting
print("\nTesting job posting fetch...")
try:
    url = TEST_URLS['naukri']
    response = requests.get(url, headers=HEADERS, timeout=10)
    print(f"✓ Successfully fetched page! Status: {response.status_code}")
    print(f"  Page size: {len(response.text)} characters")
    
    # Save first 500 characters to see what we got
    print(f"\nFirst 500 characters of page:\n{response.text[:500]}")
except Exception as e:
    print(f"✗ Scraping error: {e}")
```

Run it:

```bash
python test_scraper.py
```

**What to expect:**
- You should see "Status code: 200" (success)
- You should see HTML content
- This proves your scraper can reach websites

**What you learned today:**
- How to install Python libraries
- What HEADERS do (avoid being blocked)
- How to make HTTP requests
- How to debug code (print statements)

### Step 4: Git Commit (3 minutes)

```bash
git add config.py test_scraper.py
git commit -m "Add configuration and test basic scraping"
```

---

## DAY 3: Build BeautifulSoup Scraper

### What You'll Do Today
- [ ] Understand HTML structure
- [ ] Learn BeautifulSoup basics
- [ ] Build a function to extract text from job postings
- [ ] Test on real job posting

### Step 1: Understand HTML (15 minutes)

**Why?** You need to know what HTML looks like to scrape it.

Open a browser, go to any job posting (e.g., Naukri.com), right-click → "Inspect" → you'll see HTML.

HTML structure of a job posting looks like:

```html
<div class="job-posting">
    <h1>Python Developer</h1>
    <div class="details">
        <span class="experience">2-3 years</span>
        <span class="salary">₹5-8 LPA</span>
    </div>
    <div class="description">
        <p>Required Skills: Python, Django, PostgreSQL...</p>
    </div>
</div>
```

**Key concept:** BeautifulSoup finds specific tags (like `<div class="description">`) and extracts text from them.

### Step 2: Learn BeautifulSoup Syntax (15 minutes)

Create a file `learn_beautifulsoup.py` to practice:

```python
from bs4 import BeautifulSoup

# Example HTML (imagine this came from a job posting)
html_content = """
<html>
    <head><title>Python Developer Job</title></head>
    <body>
        <div class="job-header">
            <h1>Senior Python Developer</h1>
            <span class="salary">₹10-15 LPA</span>
        </div>
        <div class="job-description">
            <h2>About the Role</h2>
            <p>We are looking for a Python developer with 3-5 years experience.</p>
            <p>Required Skills: Python, FastAPI, PostgreSQL, Docker</p>
        </div>
    </body>
</html>
"""

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Method 1: Find first element
title = soup.find('h1')  # Finds <h1>
print(f"Title: {title.text}")  # Prints: Senior Python Developer

# Method 2: Find by class
salary = soup.find('span', class_='salary')  # Finds <span class="salary">
print(f"Salary: {salary.text}")  # Prints: ₹10-15 LPA

# Method 3: Find all elements
paragraphs = soup.find_all('p')  # Finds ALL <p> tags
for para in paragraphs:
    print(f"Paragraph: {para.text}")

# Method 4: Get all text
all_text = soup.get_text()  # All text without HTML tags
print(f"\nAll text:\n{all_text}")
```

Run it:

```bash
python learn_beautifulsoup.py
```

**Output you'll see:**
```
Title: Senior Python Developer
Salary: ₹10-15 LPA
Paragraph: We are looking for a Python developer with 3-5 years experience.
Paragraph: Required Skills: Python, FastAPI, PostgreSQL, Docker
...
```

**Key BeautifulSoup methods:**
- `soup.find('tag')` - Find first occurrence
- `soup.find_all('tag')` - Find all occurrences
- `soup.find('tag', class_='classname')` - Find by class
- `element.text` - Extract text from element

### Step 3: Build Scraper Function (30 minutes)

Now build real scraper in `scraper.py`:

```python
import requests
from bs4 import BeautifulSoup
from config import HEADERS
import json

def fetch_job_posting(url):
    """
    Fetch HTML content from a job posting URL.
    
    Args:
        url (str): URL of job posting
        
    Returns:
        str: Raw HTML content
        
    Why this function?
    - Handles errors gracefully (if website is down)
    - Adds headers to avoid being blocked
    - Logs what's happening for debugging
    """
    try:
        print(f"🔄 Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"❌ Failed! Status code: {response.status_code}")
            return None
        
        print(f"✓ Successfully fetched! Size: {len(response.text)} chars")
        return response.text
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out - website took too long to respond")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check your internet")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def extract_text_from_html(html_content):
    """
    Extract clean text from HTML content.
    
    Args:
        html_content (str): Raw HTML from job posting
        
    Returns:
        str: Cleaned text without HTML tags
        
    Why this function?
    - Removes script tags (not visible to users)
    - Removes style tags (not relevant)
    - Gets only readable text
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        print(f"✓ Extracted {len(text)} characters of clean text")
        return text
        
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return None


def scrape_job_posting(url):
    """
    Complete pipeline: fetch URL → extract text
    
    Args:
        url (str): Job posting URL
        
    Returns:
        dict: Contains 'success' boolean and either 'text' or 'error'
    """
    # Step 1: Fetch HTML
    html = fetch_job_posting(url)
    if not html:
        return {'success': False, 'error': 'Failed to fetch URL'}
    
    # Step 2: Extract text
    text = extract_text_from_html(html)
    if not text:
        return {'success': False, 'error': 'Failed to extract text'}
    
    return {
        'success': True,
        'text': text,
        'url': url,
        'length': len(text)
    }


# Testing function
if __name__ == '__main__':
    # Test with a simple job URL
    test_url = 'https://www.naukri.com/job-listings-python-developer-fresher-0-3-years-bangalore-0'
    
    print("=" * 50)
    print("TESTING JOB POSTING SCRAPER")
    print("=" * 50)
    
    result = scrape_job_posting(test_url)
    
    if result['success']:
        print(f"\n✓ SUCCESS!")
        print(f"URL: {result['url']}")
        print(f"Text length: {result['length']} characters")
        print(f"\nFirst 300 characters:\n{result['text'][:300]}")
    else:
        print(f"\n✗ FAILED: {result['error']}")
```

**What you learned:**
- How to structure functions with clear purpose
- Error handling (try/except)
- HTML parsing with BeautifulSoup
- Logging for debugging
- Docstrings (explaining your code)

### Step 4: Test Your Scraper (10 minutes)

Run it:

```bash
python scraper.py
```

**Expected output:**
```
==================================================
TESTING JOB POSTING SCRAPER
==================================================
🔄 Fetching: https://www.naukri.com/job-listings...
✓ Successfully fetched! Size: 245632 chars
✓ Extracted 18234 characters of clean text

✓ SUCCESS!
URL: https://www.naukri.com/job-listings...
Text length: 18234 characters

First 300 characters:
[You'll see actual job posting text here]
```

### Step 5: Git Commit (5 minutes)

```bash
git add scraper.py learn_beautifulsoup.py
git commit -m "Build web scraper with BeautifulSoup"
```

**Delete test files you don't need:**
```bash
rm learn_beautifulsoup.py test_scraper.py
```

---

## DAY 4: Data Cleaning + Text Preprocessing

### What You'll Do Today
- [ ] Learn why data cleaning matters
- [ ] Build cleaning functions
- [ ] Test on real scraped text
- [ ] Prepare data for NLP

### Step 1: Understand Why Cleaning Matters (10 minutes)

Raw scraped text is messy:
```
Job Description    Python Developer   ₹5-8 LPA   Location: Bangalore 
 

  Requirements:
   - Python 3.8+
   - FastAPI or Django
```

After cleaning:
```
Python Developer Location Bangalore Requirements Python 3.8 FastAPI or Django
```

Cleaned text is easier for NLP to extract skills from.

### Step 2: Build Text Cleaning Functions (30 minutes)

Update `scraper.py` and add these functions:

```python
import re
import string

def clean_text(text):
    """
    Clean raw text for NLP processing.
    
    Removes:
    - Extra whitespace
    - Special characters (but keep important ones)
    - URLs
    - Email addresses
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text
    """
    # Convert to lowercase (skills written as "Python", "python", "PYTHON" are same)
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'\b\d{10,}\b', '', text)
    
    # Remove special characters but keep hyphens, dots, +
    text = re.sub(r'[^a-z0-9\s\.\+\-\#]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def segment_text_by_sections(text):
    """
    Segment text into logical sections (Requirements, Skills, Experience, etc)
    
    Why?
    - "Skills:" sections are most important for skill extraction
    - We can focus NLP on relevant sections
    
    Args:
        text (str): Cleaned text
        
    Returns:
        dict: Text segments by section
    """
    segments = {
        'full_text': text,
        'requirements': '',
        'skills': '',
        'experience': '',
        'qualifications': ''
    }
    
    # Find Requirements section
    if 'requirement' in text:
        start = text.find('requirement')
        end = text.find('responsibility') if 'responsibility' in text else len(text)
        segments['requirements'] = text[start:end]
    
    # Find Skills section
    if 'skill' in text:
        start = text.find('skill')
        end = text.find('experience') if 'experience' in text else len(text)
        segments['skills'] = text[start:end]
    
    # Find Experience section
    if 'experience' in text:
        start = text.find('experience')
        segments['experience'] = text[start:]
    
    return segments


# Test the cleaning
if __name__ == '__main__':
    # Example messy text
    messy_text = """
    Job Description: Python Developer
    
    Requirements:
    - Python 3.8+, Django/FastAPI
    - PostgreSQL, Redis
    - Docker, Kubernetes
    - Experience: 2-3 years
    
    Contact: john@example.com or 9876543210
    Website: https://www.example.com
    """
    
    print("BEFORE CLEANING:")
    print(messy_text)
    
    cleaned = clean_text(messy_text)
    print("\n\nAFTER CLEANING:")
    print(cleaned)
    
    segments = segment_text_by_sections(cleaned)
    print("\n\nSEGMENTED:")
    for section, content in segments.items():
        if content:
            print(f"{section}: {content[:100]}...")
```

Run it:
```bash
python scraper.py
```

**What you learned:**
- Regex for text cleaning
- Importance of lowercasing
- Text segmentation for better NLP
- Why preprocessing matters

### Step 3: Integrate Cleaning into Scraper (15 minutes)

Update the `scrape_job_posting` function:

```python
def scrape_job_posting(url):
    """
    Complete pipeline: fetch URL → extract text → clean text
    """
    # Step 1: Fetch HTML
    html = fetch_job_posting(url)
    if not html:
        return {'success': False, 'error': 'Failed to fetch URL'}
    
    # Step 2: Extract text
    text = extract_text_from_html(html)
    if not text:
        return {'success': False, 'error': 'Failed to extract text'}
    
    # Step 3: Clean text (NEW)
    cleaned_text = clean_text(text)
    
    # Step 4: Segment text (NEW)
    segments = segment_text_by_sections(cleaned_text)
    
    return {
        'success': True,
        'raw_text': text,
        'cleaned_text': cleaned_text,
        'segments': segments,
        'url': url,
        'length': len(cleaned_text)
    }
```

### Step 4: Git Commit (5 minutes)

```bash
git add scraper.py
git commit -m "Add text cleaning and segmentation"
```

---

## DAY 5-7: Build Skill Extraction with NLP

### What You'll Do Days 5-7
- [ ] Learn spaCy basics
- [ ] Build skill extraction function
- [ ] Test on real job postings
- [ ] Create output JSON

### Create skills_extractor.py (Day 5-6, 60 minutes)

```python
import spacy
from config import TECHNICAL_SKILLS, NLP_MODEL
import json

class SkillExtractor:
    """
    Extract technical skills from job posting text using NLP and pattern matching.
    
    Why a class?
    - Keeps NLP model loaded in memory (faster processing)
    - Organizes related functions together
    - Can cache results
    """
    
    def __init__(self):
        """Load the spaCy model once (takes time, so we do it once)"""
        print("Loading NLP model...")
        self.nlp = spacy.load(NLP_MODEL)
        print("✓ NLP model loaded")
        
        # Create lowercase skills set for faster lookup
        self.skills_lowercase = set(skill.lower() for skill in TECHNICAL_SKILLS)
    
    def extract_skills_pattern_matching(self, text):
        """
        Extract skills using pattern matching (keyword search)
        
        Simple approach: Look for skill names in text
        Faster but less accurate than NLP
        """
        found_skills = set()
        
        for skill in self.skills_lowercase:
            # Search for exact skill name
            if skill in text.lower():
                found_skills.add(skill)
        
        return list(found_skills)
    
    def extract_skills_nlp(self, text):
        """
        Extract skills using NLP (more advanced)
        
        Uses spaCy to understand context and find skills even if
        spelled differently
        """
        doc = self.nlp(text)
        
        # Extract named entities and noun chunks
        entities = [ent.text.lower() for ent in doc.ents]
        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        
        found_skills = set()
        
        # Check if entities or chunks match skills
        for item in entities + noun_chunks:
            if item in self.skills_lowercase:
                found_skills.add(item)
        
        return list(found_skills)
    
    def extract_all_skills(self, text):
        """
        Extract skills using both methods (hybrid approach)
        
        Combines pattern matching + NLP for best results
        """
        # Method 1: Pattern matching (fast, reliable)
        pattern_skills = self.extract_skills_pattern_matching(text)
        
        # Method 2: NLP (more sophisticated)
        nlp_skills = self.extract_skills_nlp(text)
        
        # Combine and remove duplicates
        all_skills = set(pattern_skills + nlp_skills)
        
        return sorted(list(all_skills))
    
    def categorize_skills(self, skills):
        """
        Categorize skills into groups
        
        Makes output more organized
        """
        categories = {
            'languages': ['python', 'java', 'javascript', 'c++', 'go', 'rust', 'typescript'],
            'frameworks': ['django', 'fastapi', 'flask', 'react', 'angular', 'node.js'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'google cloud'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'gitlab', 'git'],
            'data_tools': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
            'other': []
        }
        
        categorized = {cat: [] for cat in categories}
        
        for skill in skills:
            found = False
            for category, category_skills in categories.items():
                if skill in category_skills:
                    categorized[category].append(skill)
                    found = True
                    break
            
            if not found:
                categorized['other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}


# Test the extractor (Day 6)
if __name__ == '__main__':
    extractor = SkillExtractor()
    
    test_text = """
    We are looking for a Python developer with 3-5 years experience.
    Required Skills: Python, Django, FastAPI, PostgreSQL, Redis, Docker, Kubernetes.
    Experience with AWS or Azure is a plus.
    Knowledge of machine learning (TensorFlow, PyTorch) preferred.
    """
    
    print("=" * 50)
    print("SKILL EXTRACTION TEST")
    print("=" * 50)
    print(f"\nTest text:\n{test_text}\n")
    
    # Extract skills
    skills = extractor.extract_all_skills(test_text)
    print(f"\n✓ Found {len(skills)} skills:")
    print(skills)
    
    # Categorize
    categorized = extractor.categorize_skills(skills)
    print(f"\n✓ Categorized:")
    for category, skill_list in categorized.items():
        print(f"  {category}: {skill_list}")
    
    # Output as JSON
    output = {
        'skills_found': skills,
        'skills_by_category': categorized,
        'total_skills': len(skills)
    }
    print(f"\n✓ JSON Output:")
    print(json.dumps(output, indent=2))
```

### Day 7: Create Main Orchestration File

Create `main.py`:

```python
"""
Main entry point for Job Posting Analyzer

Orchestrates:
1. Scraping
2. Cleaning
3. Skill extraction
4. Output
"""

from scraper import scrape_job_posting
from skills_extractor import SkillExtractor
import json

def analyze_job_posting(url):
    """
    Complete pipeline: URL → Skills extracted
    
    Args:
        url (str): Job posting URL
        
    Returns:
        dict: Analysis results
    """
    print("\n" + "=" * 60)
    print("JOB POSTING ANALYZER")
    print("=" * 60)
    
    # Step 1: Scrape
    print("\n[Step 1/3] Scraping job posting...")
    scrape_result = scrape_job_posting(url)
    
    if not scrape_result['success']:
        print(f"❌ Scraping failed: {scrape_result['error']}")
        return None
    
    # Step 2: Extract skills
    print("\n[Step 2/3] Extracting skills...")
    extractor = SkillExtractor()
    skills = extractor.extract_all_skills(scrape_result['cleaned_text'])
    categorized = extractor.categorize_skills(skills)
    
    # Step 3: Format output
    print("\n[Step 3/3] Formatting results...")
    
    result = {
        'url': url,
        'status': 'success',
        'analysis': {
            'total_skills_found': len(skills),
            'skills_list': skills,
            'skills_by_category': categorized,
            'text_length': scrape_result['length']
        }
    }
    
    return result


def display_results(results):
    """Pretty print the results"""
    if not results:
        return
    
    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    
    print(f"\nURL: {results['url']}")
    print(f"Total Skills Found: {results['analysis']['total_skills_found']}")
    
    print(f"\nSkills by Category:")
    for category, skills_list in results['analysis']['skills_by_category'].items():
        print(f"  • {category.upper()}: {', '.join(skills_list)}")
    
    print(f"\n✓ Full results as JSON:")
    print(json.dumps(results, indent=2))


# Test it
if __name__ == '__main__':
    # Test with a job URL
    test_url = 'https://www.naukri.com/job-listings-python-developer-fresher-0-3-years-bangalore-0'
    
    results = analyze_job_posting(test_url)
    display_results(results)
    
    # Save results to JSON file
    if results:
        with open('analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to analysis_results.json")
```

### Final Commits (Day 7)

```bash
git add skills_extractor.py main.py
git commit -m "Add skill extraction with spaCy and main orchestration"

git add requirements.txt
git commit -m "Complete Week 1: Core scraping and extraction"
```

---

## WEEK 1 SUMMARY

### What You Built
- [x] Web scraper using BeautifulSoup
- [x] Text cleaning and preprocessing
- [x] NLP-based skill extraction
- [x] Categorization of skills
- [x] JSON output

### Skills You Gained
- ✓ Web scraping with Python
- ✓ HTML parsing
- ✓ Data cleaning (regex, text processing)
- ✓ Natural Language Processing basics
- ✓ Function design and documentation
- ✓ Error handling
- ✓ Git version control

### GitHub Commits Made
1. Initial project setup with documentation
2. Configuration and test basic scraping
3. Build web scraper with BeautifulSoup
4. Add text cleaning and segmentation
5. Add skill extraction with spaCy and main orchestration

### Testing Checklist
- [ ] Scraper successfully fetches job postings
- [ ] Text extraction removes HTML correctly
- [ ] Text cleaning works properly
- [ ] Skill extraction finds real skills
- [ ] Output formats correctly as JSON
- [ ] Git history shows incremental progress

### Files Created
```
job-posting-analyzer/
├── .git/
├── .gitignore
├── README.md (completed)
├── requirements.txt
├── config.py
├── scraper.py (complete)
├── skills_extractor.py (complete)
├── main.py (complete)
└── analysis_results.json (test output)
```

---

## TROUBLESHOOTING COMMON ERRORS

### "ModuleNotFoundError: No module named 'requests'"
**Solution:** Run `pip install -r requirements.txt` again

### "Failed to fetch URL - Connection refused"
**Solution:** Check your internet connection

### "spaCy model not found"
**Solution:** Run `python -m spacy download en_core_web_sm`

### "BeautifulSoup parsing issues"
**Solution:** Check if website HTML structure changed (websites update)

---

## NEXT STEPS (Week 2)

- Deploy to FastAPI (create REST API)
- Add frontend (Streamlit)
- Improve skill extraction accuracy
- Add support for multiple job sites
- Deploy to Google Cloud

