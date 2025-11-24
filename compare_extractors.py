"""
Comparing original vs enhanced skill extractor
"""

from skills_extractor import SkillExtractor  # Original (old version)
from skills_extractor_v2 import EnhancedSkillExtractor  # New (updated version)


def compare_extractors():
    """Compare both extractors side by side"""
    
    print("=" * 70)
    print("EXTRACTOR COMPARISON TEST")
    print("=" * 70)
    print()
    
    # Test text with variations
    test_text = """
    Looking for a Python3 developer with ML experience.
    Must know JavaScript (ES6), Docker containerization, and K8s.
    5+ years experience required. AWS or Google Cloud Platform knowledge is a plus.
    """
    
    print("Test Text:")
    print("-" * 70)
    print(test_text)
    print("-" * 70)
    print()
    
    # Test original extractor
    print("=" * 70)
    print("ORIGINAL EXTRACTOR (Day 3)")
    print("=" * 70)
    print()
    
    original = SkillExtractor()
    original_results = original.extract_skills(test_text)
    
    print(f"\nSkills found: {len(original_results)}")
    print(f"Skills: {', '.join(sorted(original_results))}")
    
    # Test enhanced extractor
    print("\n" + "=" * 70)
    print("ENHANCED EXTRACTOR (Day 5)")
    print("=" * 70)
    print()
    
    enhanced = EnhancedSkillExtractor()
    enhanced_results = enhanced.extract_skills(test_text)
    
    print(f"\nSkills found: {len(enhanced_results)}")
    print(f"Skills: {', '.join(sorted(enhanced_results))}")
    
    # Comparison
    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)
    
    original_set = set(original_results)
    enhanced_set = set(enhanced_results)
    
    missed_by_original = enhanced_set - original_set
    caught_by_both = original_set & enhanced_set
    
    print(f"\n✓ Caught by both: {len(caught_by_both)}")
    if caught_by_both:
        print(f"   {', '.join(sorted(caught_by_both))}")
    
    print(f"\n✨ Caught ONLY by enhanced: {len(missed_by_original)}")
    if missed_by_original:
        print(f"   {', '.join(sorted(missed_by_original))}")
        print(f"\n   Why enhanced caught these:")
        print(f"   • Handles variations (Python3 → python, ML → machine learning)")
        print(f"   • Recognizes abbreviations (K8s → kubernetes, ES6 → javascript)")
        print(f"   • Uses NLP context understanding")
    
    improvement = ((len(enhanced_set) - len(original_set)) / len(original_set) * 100) if original_set else 0
    print(f"\n📈 Improvement: +{improvement:.0f}% more skills detected")


if __name__ == "__main__":
    compare_extractors()
