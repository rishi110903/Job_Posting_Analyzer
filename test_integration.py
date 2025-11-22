"""
Test integration between scraper and skills extractor
"""

from scraper import JobScraper
from skills_extractor import SkillExtractor

def test_complete_pipeline():
    print("=" * 60)
    print("COMPLETE PIPELINE TEST")
    print("=" * 60)
    print()
    
    # Initialize components
    scraper = JobScraper()
    extractor = SkillExtractor()
    
    # Get URL
    url = input("Enter job posting URL (or press Enter for default): ").strip()
    if not url:
        url = "https://www.python.org/jobs/6940/"
    
    print(f"\n1. Scraping job from: {url}\n")
    
    # Scrape
    result = scraper.scrape_job(url)
    
    if not result:
        print("✗ Scraping failed")
        return
    
    print(f"✓ Scraped {len(result['text'])} characters\n")
    
    # Extract skills
    print("2. Extracting skills...\n")
    analysis = extractor.analyze_skills(result['text'])
    
    # Display results
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"\nJob URL: {result['url']}")
    print(f"Skills found: {analysis['total_skills']}")
    print(f"\nAll skills: {', '.join(analysis['all_skills'])}")
    
    print("\n" + "-" * 60)
    print("By Category:")
    print("-" * 60)
    
    for category, skills in analysis['categorized'].items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for skill in skills:
            print(f"  • {skill}")

if __name__ == "__main__":
    test_complete_pipeline()
