"""
File Manager - Handles saving and loading analysis results
"""

import json
import os
from datetime import datetime


class FileManager:
    """Manages saving and loading job analysis results"""
    
    def __init__(self, output_dir='output'):
        """
        Initialize FileManager
        
        Args:
            output_dir (str): Directory to save results
        """
        self.output_dir = output_dir
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ Created output directory: {self.output_dir}")
    
    def generate_filename(self, job_url):
        """
        Generate unique filename for job analysis
        
        Args:
            job_url (str): Job posting URL
            
        Returns:
            str: Filename with timestamp
        """
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Extract domain from URL for readability
        try:
            from urllib.parse import urlparse
            domain = urlparse(job_url).netloc
            # Remove www. and special characters
            domain = domain.replace('www.', '').replace('.', '_')
            filename = f"job_{domain}_{timestamp}.json"
        except:
            # Fallback if URL parsing fails
            filename = f"job_analysis_{timestamp}.json"
        
        return filename
    
    def save_analysis(self, analysis_data, job_url):
        """
        Save job analysis to JSON file
        
        Args:
            analysis_data (dict): Complete analysis results
            job_url (str): Job posting URL
            
        Returns:
            str: Path to saved file or None if failed
        """
        try:
            # Generate filename
            filename = self.generate_filename(job_url)
            filepath = os.path.join(self.output_dir, filename)
            
            # Add metadata
            output_data = {
                'metadata': {
                    'analysis_date': datetime.now().isoformat(),
                    'job_url': job_url,
                    'analyzer_version': '1.0'
                },
                'results': analysis_data
            }
            
            # Save to JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Results saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            return None
    
    def load_analysis(self, filename):
        """
        Load analysis from JSON file
        
        Args:
            filename (str): Name of file to load
            
        Returns:
            dict: Analysis data or None if failed
        """
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✓ Loaded analysis from: {filepath}")
            return data
            
        except FileNotFoundError:
            print(f"✗ File not found: {filename}")
            return None
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON in file: {filename}")
            return None
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return None
    
    def list_saved_analyses(self):
        """
        List all saved analysis files
        
        Returns:
            list: List of filenames
        """
        try:
            files = [f for f in os.listdir(self.output_dir) 
                    if f.endswith('.json') and f != '.gitkeep']
            
            if files:
                print(f"\n✓ Found {len(files)} saved analysis files:")
                for i, filename in enumerate(files, 1):
                    filepath = os.path.join(self.output_dir, filename)
                    # Get file modification time
                    mod_time = os.path.getmtime(filepath)
                    date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M')
                    print(f"   {i}. {filename} (saved: {date_str})")
            else:
                print("\n⚠ No saved analyses found")
            
            return files
            
        except Exception as e:
            print(f"✗ Error listing files: {e}")
            return []


# Test the file manager
if __name__ == "__main__":
    print("=" * 70)
    print("FILE MANAGER TEST")
    print("=" * 70)
    print()
    
    # Create file manager
    fm = FileManager()
    
    # Test data
    test_analysis = {
        'total_skills': 5,
        'all_skills': ['python', 'sql', 'aws', 'docker', 'git'],
        'categorized': {
            'programming_languages': ['python'],
            'databases': ['sql'],
            'cloud_platforms': ['aws'],
            'devops_tools': ['docker', 'git']
        }
    }
    
    test_url = "https://example.com/job/12345"
    
    # Save test
    print("Test 1: Saving analysis...")
    saved_path = fm.save_analysis(test_analysis, test_url)
    
    if saved_path:
        print("\n✓ Save test passed")
        
        # List test
        print("\nTest 2: Listing saved files...")
        files = fm.list_saved_analyses()
        
        if files:
            print("\n✓ List test passed")
            
            # Load test
            print("\nTest 3: Loading analysis...")
            loaded_data = fm.load_analysis(files[0])
            
            if loaded_data:
                print("\n✓ Load test passed")
                print("\nLoaded data:")
                print(json.dumps(loaded_data, indent=2))
            else:
                print("\n✗ Load test failed")
        else:
            print("\n✗ List test failed")
    else:
        print("\n✗ Save test failed")
    
    print("\n" + "=" * 70)
    print("FILE MANAGER TEST COMPLETE")
    print("=" * 70)
