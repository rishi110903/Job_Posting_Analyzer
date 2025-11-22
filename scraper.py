"""
Web scraper to fetch job posting content
"""

import requests
from bs4 import BeautifulSoup
from config import HEADERS, TIMEOUT


class JobScraper:
    """Fetches and parses job posting HTML"""
    
    def __init__(self):
        self.headers = HEADERS
        self.timeout = TIMEOUT
    
    def fetch_job_posting(self, url):
        """
        Fetch HTML content from job posting URL
        
        Args:
            url (str): Job posting URL
            
        Returns:
            str: Raw HTML content or None if error
        """
        try:
            print(f"Fetching job posting from: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()  # Raise error for bad status codes
            
            print(f"✓ Successfully fetched content (Status: {response.status_code})")
            return response.text
            
        except requests.exceptions.Timeout:
            print(f"✗ Error: Request timed out after {self.timeout} seconds")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching URL: {e}")
            return None
    
    def parse_html(self, html_content):
        """
        Parse HTML and extract text content
        
        Args:
            html_content (str): Raw HTML
            
        Returns:
            str: Cleaned text content
        """
        if not html_content:
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            print(f"✓ Extracted {len(text)} characters of text")
            return text
            
        except Exception as e:
            print(f"✗ Error parsing HTML: {e}")
            return None
    
    def scrape_job(self, url):
        """
        Main method: fetch and parse job posting
        
        Args:
            url (str): Job posting URL
            
        Returns:
            dict: Contains 'url', 'raw_html', 'text'
        """
        html = self.fetch_job_posting(url)
        if not html:
            return None
        
        text = self.parse_html(html)
        if not text:
            return None
        
        return {
            'url': url,
            'raw_html': html,
            'text': text
        }


# Test the scraper (will be called from main.py)
if __name__ == "__main__":
    scraper = JobScraper()
    
    # Test with a simple webpage
    test_url = "https://jobs.lever.co/example"  # Generic job posting format
    result = scraper.scrape_job(test_url)
    
    if result:
        print("\n--- SCRAPER TEST SUCCESSFUL ---")
        print(f"URL: {result['url']}")
        print(f"Text length: {len(result['text'])} characters")
        print(f"\nFirst 500 characters:\n{result['text'][:500]}...")
    else:
        print("\n--- SCRAPER TEST FAILED ---")
