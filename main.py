"""
Main entry point for Job Posting Analyzer
"""

from scraper import JobScraper


def main():
    """Main execution function"""
    print("=" * 60)
    print("JOB POSTING ANALYZER")
    print("=" * 60)
    print()
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Test URL - using a public job posting
    # You can replace this with any job posting URL you want to test
    test_url = input("Enter a job posting URL to analyze (or press Enter for default): ").strip()
    
    if not test_url:
        # Default test URL - a simple job posting page
        test_url = "https://www.python.org/jobs/6940/"
    
    print(f"\nAnalyzing job posting from: {test_url}\n")
    
    # Scrape the job posting
    result = scraper.scrape_job(test_url)
    
    if result:
        print("\n" + "=" * 60)
        print("✓ SCRAPING SUCCESSFUL")
        print("=" * 60)
        print(f"\nExtracted {len(result['text'])} characters")
        print(f"\nFirst 1000 characters of job posting:\n")
        print("-" * 60)
        print(result['text'][:1000])
        print("-" * 60)
        print("\n✓ Scraper is working!")
    else:
        print("\n" + "=" * 60)
        print("✗ SCRAPING FAILED")
        print("=" * 60)
        print("\nTry a different URL or check your internet connection.")


if __name__ == "__main__":
    main()
