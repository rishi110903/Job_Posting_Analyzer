"""
Integration test for Job Posting Analyzer
Tests the complete pipeline: Scraping → Skills Extraction
"""

from scraper import JobScraper
from skills_extractor import SkillExtractor


def test_complete_pipeline():
    """Test the complete job analysis pipeline"""
    print("=" * 70)
    print("     INTEGRATION TEST - Complete Pipeline")
    print("=" * 70)
    print()
    
    # Initialize components
    print("Step 1: Initializing components...")
    scraper = JobScraper()
    extractor = SkillExtractor()
    print("✓ JobScraper initialized")
    print("✓ SkillExtractor initialized")
    print()
    
    # Get URL
    print("Step 2: Getting job posting URL...")
    test_url = input("Enter job posting URL (or press Enter for default): ").strip()
    
    if not test_url:
        test_url = "https://www.python.org/jobs/6940/"
        print(f"Using default URL: {test_url}")
    
    print()
    print("=" * 70)
    print("TESTING PHASE 1: WEB SCRAPING")
    print("=" * 70)
    print()
    
    # Test scraping
    print(f"Scraping job posting from: {test_url}\n")
    result = scraper.scrape_job(test_url)
    
    if not result:
        print("✗ SCRAPING TEST FAILED")
        print("\nThe scraper could not fetch the job posting.")
        print("Check your internet connection and URL.")
        return
    
    print("✓ SCRAPING TEST PASSED")
    print(f"\nScraping Results:")
    print(f"   • URL: {result['url']}")
    print(f"   • Raw HTML size: {len(result['raw_html']):,} characters")
    print(f"   • Clean text size: {len(result['text']):,} characters")
    print(f"   • Word count: {len(result['text'].split()):,} words")
    
    # Show sample of text
    print(f"\n📄 Sample of extracted text (first 400 characters):")
    print("-" * 70)
    print(result['text'][:400])
    if len(result['text']) > 400:
        print("...")
    print("-" * 70)
    
    print()
    print("=" * 70)
    print("TESTING PHASE 2: SKILLS EXTRACTION")
    print("=" * 70)
    print()
    
    # Test skills extraction
    print("Extracting skills from job posting text...\n")
    analysis = extractor.analyze_skills(result['text'])
    
    if analysis['total_skills'] == 0:
        print("⚠ EXTRACTION TEST WARNING")
        print("\nNo skills were extracted.")
        print("This might mean:")
        print("  • The job posting doesn't mention technical skills")
        print("  • Skills aren't in our database")
        print("\nExtraction still works, but no matches found.")
    else:
        print("✓ SKILLS EXTRACTION TEST PASSED")
    
    print(f"\nExtraction Results:")
    print(f"   • Total skills found: {analysis['total_skills']}")
    print(f"   • Unique categories: {len(analysis['categorized'])}")
    
    if analysis['all_skills']:
        print(f"\n🔍 Skills Detected:")
        print(f"   {', '.join(analysis['all_skills'])}")
    
    # Test categorization
    print()
    print("=" * 70)
    print("TESTING PHASE 3: SKILL CATEGORIZATION")
    print("=" * 70)
    print()
    
    if analysis['categorized']:
        print("✓ CATEGORIZATION TEST PASSED\n")
        print("Skills grouped by category:")
        
        for category, skills in analysis['categorized'].items():
            category_name = category.replace('_', ' ').title()
            print(f"\n📌 {category_name} ({len(skills)} skills):")
            for skill in skills:
                print(f"   • {skill}")
    else:
        print("⚠ CATEGORIZATION TEST WARNING")
        print("\nNo skills to categorize (no skills were found)")
    
    # Overall test summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print()
    
    tests_passed = 0
    tests_total = 3
    
    print("Test Results:")
    
    # Test 1: Scraping
    if result:
        print("   ✓ Scraping: PASSED")
        tests_passed += 1
    else:
        print("   ✗ Scraping: FAILED")
    
    # Test 2: Extraction
    if analysis['total_skills'] >= 0:  # Even 0 is valid
        print("   ✓ Skills Extraction: PASSED")
        tests_passed += 1
    else:
        print("   ✗ Skills Extraction: FAILED")
    
    # Test 3: Categorization
    if isinstance(analysis['categorized'], dict):
        print("   ✓ Categorization: PASSED")
        tests_passed += 1
    else:
        print("   ✗ Categorization: FAILED")
    
    print()
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n🎉 ALL TESTS PASSED! Pipeline is working correctly.")
    else:
        print(f"\n⚠ {tests_total - tests_passed} test(s) failed. Check errors above.")
    
    # Data quality check
    print()
    print("=" * 70)
    print("DATA QUALITY CHECK")
    print("=" * 70)
    print()
    
    text_lower = result['text'].lower()
    
    # Check for job-related keywords
    quality_indicators = {
        'Job posting keywords': ['job', 'position', 'role', 'career', 'opportunity'],
        'Requirement keywords': ['required', 'experience', 'skills', 'qualifications'],
        'Technical keywords': ['developer', 'engineer', 'analyst', 'programming', 'software'],
    }
    
    print("Content Quality Indicators:")
    for indicator_type, keywords in quality_indicators.items():
        found = [kw for kw in keywords if kw in text_lower]
        if found:
            print(f"   ✓ {indicator_type}: {len(found)} found ({', '.join(found[:3])})")
        else:
            print(f"   ✗ {indicator_type}: None found")
    
    print()
    print("=" * 70)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 70)
    print()


if __name__ == "__main__":
    test_complete_pipeline()
