"""
Main entry point for Job Posting Analyzer
Combines scraping, skills extraction, and file management
"""

from scraper import JobScraper
from skills_extractor import SkillExtractor
from file_manager import FileManager


def display_results(result, analysis):
    """
    Display analysis results in formatted way
    
    Args:
        result (dict): Scraping results with 'url' and 'text'
        analysis (dict): Skills analysis with 'total_skills', etc.
    """
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n📊 Statistics:")
    print(f"   • Job URL: {result['url']}")
    print(f"   • Text length: {len(result['text']):,} characters")
    print(f"   • Total skills: {analysis['total_skills']}")
    print(f"   • Categories: {len(analysis['categorized'])}")
    
    if analysis['all_skills']:
        print(f"\n🔍 All Skills Found:")
        print(f"   {', '.join(analysis['all_skills'])}")
    else:
        print("\n⚠ No skills found in this job posting")
    
    if analysis['categorized']:
        print("\n" + "=" * 70)
        print("SKILLS BY CATEGORY")
        print("=" * 70)
        
        for category, skills in analysis['categorized'].items():
            category_name = category.replace('_', ' ').title()
            print(f"\n📌 {category_name}:")
            for skill in skills:
                print(f"   • {skill}")


def analyze_new_job():
    """Analyze a new job posting - complete workflow"""
    
    # Initialize components
    print("\nInitializing components...")
    scraper = JobScraper()
    extractor = SkillExtractor()
    file_manager = FileManager()
    print("✓ Ready\n")
    
    # Get URL from user
    print("Enter job posting URL to analyze:")
    print("(or press Enter for default test URL)")
    url = input("\nURL: ").strip()
    
    if not url:
        url = "https://www.python.org/jobs/6940/"
        print(f"Using default: {url}")
    
    # STEP 1: Scrape the job posting
    print("\n" + "=" * 70)
    print("STEP 1: SCRAPING JOB POSTING")
    print("=" * 70)
    print()
    
    result = scraper.scrape_job(url)
    
    if not result:
        print("✗ Scraping failed.")
        print("\nPossible reasons:")
        print("  • Invalid URL")
        print("  • Network connection issue")
        print("  • Website blocking requests")
        print("\nPlease try a different URL.")
        return  # Exit function early
    
    print(f"✓ Successfully scraped job posting")
    print(f"   • Text extracted: {len(result['text']):,} characters")
    print(f"   • Word count: {len(result['text'].split()):,} words")
    
    # STEP 2: Extract skills
    print("\n" + "=" * 70)
    print("STEP 2: EXTRACTING SKILLS")
    print("=" * 70)
    print()
    
    analysis = extractor.analyze_skills(result['text'])
    
    print(f"✓ Skill extraction complete")
    print(f"   • Skills found: {analysis['total_skills']}")
    
    # STEP 3: Display results
    display_results(result, analysis)
    
    # STEP 4: Save results
    print("\n" + "=" * 70)
    print("STEP 3: SAVE RESULTS")
    print("=" * 70)
    print()
    
    save_choice = input("Save results to file? (Y/n): ").strip().lower()
    
    if save_choice == 'n' or save_choice == 'no':
        print("⚠ Results not saved (displayed only)")
    else:
        # Prepare complete data for saving
        complete_data = {
            'job_info': {
                'url': result['url'],
                'text_length': len(result['text']),
                'word_count': len(result['text'].split())
            },
            'skills_analysis': analysis
        }
        
        saved_path = file_manager.save_analysis(complete_data, result['url'])
        
        if saved_path:
            print(f"\n✓ Analysis saved successfully!")
        else:
            print("\n⚠ Could not save results")
    
    print("\n" + "=" * 70)
    print("✓ ANALYSIS COMPLETE")
    print("=" * 70)


def view_saved_analyses():
    """View previously saved analyses"""
    
    file_manager = FileManager()
    
    print("\n" + "=" * 70)
    print("SAVED ANALYSES")
    print("=" * 70)
    
    files = file_manager.list_saved_analyses()
    
    if not files:
        print("\nNo saved analyses found yet.")
        print("Analyze a job posting and save it first!")
        return
    
    print("\nEnter file number to view details (or press Enter to go back):")
    choice = input("Choice: ").strip()
    
    if not choice:
        return
    
    if choice.isdigit():
        index = int(choice) - 1
        
        if 0 <= index < len(files):
            data = file_manager.load_analysis(files[index])
            
            if data:
                print("\n" + "=" * 70)
                print("SAVED ANALYSIS DETAILS")
                print("=" * 70)
                
                # Show metadata
                print(f"\n📅 Analysis Date: {data['metadata']['analysis_date']}")
                print(f"🔗 Job URL: {data['metadata']['job_url']}")
                
                # Show results
                results = data['results']
                job_info = results.get('job_info', {})
                skills = results.get('skills_analysis', {})
                
                print(f"\n📊 Statistics:")
                print(f"   • Text length: {job_info.get('text_length', 'N/A'):,} characters")
                print(f"   • Total skills: {skills.get('total_skills', 0)}")
                print(f"   • Categories: {len(skills.get('categorized', {}))}")
                
                if skills.get('all_skills'):
                    print(f"\n🔍 Skills Found:")
                    print(f"   {', '.join(skills['all_skills'])}")
                
                if skills.get('categorized'):
                    print("\n" + "=" * 70)
                    print("SKILLS BY CATEGORY")
                    print("=" * 70)
                    
                    for category, skill_list in skills['categorized'].items():
                        print(f"\n📌 {category.replace('_', ' ').title()}:")
                        for skill in skill_list:
                            print(f"   • {skill}")
        else:
            print(f"\n⚠ Invalid choice. Please enter 1-{len(files)}")
    else:
        print("\n⚠ Please enter a number")


def show_menu():
    """Display main menu"""
    print("\n" + "=" * 70)
    print("          JOB POSTING ANALYZER")
    print("=" * 70)
    print("\nWhat would you like to do?")
    print("\n1. Analyze new job posting")
    print("2. View saved analyses")
    print("3. Exit")
    print()


def main():
    """Main program loop"""
    
    print("=" * 70)
    print("     Welcome to Job Posting Analyzer")
    print("=" * 70)
    
    while True:
        show_menu()
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            analyze_new_job()
        
        elif choice == '2':
            view_saved_analyses()
        
        elif choice == '3':
            print("\n" + "=" * 70)
            print("✓ Thanks for using Job Posting Analyzer!")
            print("=" * 70)
            break
        
        else:
            print("\n⚠ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
