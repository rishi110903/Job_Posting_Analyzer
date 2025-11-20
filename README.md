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

## What you will Learn
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

