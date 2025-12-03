# Job Posting Analyzer

## 🎯 Project Overview
Job Posting Analyzer is a complete end-to-end application that automates the extraction of technical skills from job postings. It uses NLP (spaCy) to identify programming languages, frameworks, databases, cloud platforms, and DevOps tools, then categorizes them and detects experience requirements.

Built as a 5-day intensive project demonstrating full-stack development skills, from web scraping to API deployment.

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

## 📦 Installation & Setup
Prerequisites
Python 3.8+

Git

Internet connection

## Step 1: Clone Repository
git clone https://github.com/yourusername/job-posting-analyzer.git
cd job-posting-analyzer
## Step 2: Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
## Step 3: Install Dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm


## 🚀 Live Demo
API Endpoint: http://localhost:8000 (local)
API Docs: http://localhost:8000/docs
Status: ✅ Fully functional, ready for deployment

## 📁 Project Structure

job-posting-analyzer/
<br>
api/ <ul>

<li>__init__.py</li>
<li>main.py</li>
<li>models.py</li>                

<p>pydantic model</p>
<ul>
<li>config.py  # Settings & skills database</li>
<li>scraper.py # Web scraping (JobScraper class)</li>
<li>skills_extractor.py # V1: Basic regex extractor</li>
<li>skills_extractor_v2.py # V2: Enhanced NLP extractor ⭐</li>
<li>file_manager.py # JSON file persistence</li>
<li>main.py # CLI application</li>
<li>test_integration.py  # Integration tests</li>
<li>compare_extractors.py # V1 vs V2 comparison</li>
<li>requirements.txt # Dependencies</li>
<li>README.md </li>
<li>.gitignore</li>
<ul>
 output/                   
    <li>.gitkeep</li>

