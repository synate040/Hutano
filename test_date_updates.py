#!/usr/bin/env python
"""
Test script to verify that all 2023 dates have been updated to 2025
"""

import os
import re
import glob

def find_2023_dates(directory):
    """Find all files containing 2023 dates"""
    files_with_2023 = []
    
    # File patterns to search
    patterns = [
        '**/*.py',
        '**/*.html',
        '**/*.js',
        '**/*.css',
        '**/*.csv',
        '**/*.md',
        '**/*.txt'
    ]
    
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(directory, pattern), recursive=True):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Look for 2023 dates
                    if '2023' in content:
                        # Find specific date patterns
                        date_patterns = [
                            r'2023-\d{2}-\d{2}',  # 2023-01-01
                            r'\d{2}/\d{2}/2023',  # 01/01/2023
                            r'\d{2}-\d{2}-2023',  # 01-01-2023
                            r'2023',              # Just the year
                        ]
                        
                        matches = []
                        for date_pattern in date_patterns:
                            matches.extend(re.findall(date_pattern, content))
                        
                        if matches:
                            files_with_2023.append({
                                'file': file_path,
                                'matches': list(set(matches))
                            })
                            
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return files_with_2023

def main():
    """Main function to test date updates"""
    print("🔍 Checking for remaining 2023 dates in HUTANO system...")
    print("=" * 60)
    
    # Check the hutano directory
    hutano_dir = "hutano"
    if not os.path.exists(hutano_dir):
        print("❌ HUTANO directory not found!")
        return
    
    files_with_2023 = find_2023_dates(hutano_dir)
    
    if files_with_2023:
        print(f"⚠️  Found {len(files_with_2023)} files still containing 2023 dates:")
        print()
        
        for file_info in files_with_2023:
            print(f"📄 {file_info['file']}")
            for match in file_info['matches']:
                print(f"   - {match}")
            print()
    else:
        print("✅ No 2023 dates found! All dates have been successfully updated to 2025.")
    
    print("=" * 60)
    print("🎯 Summary:")
    print(f"   Files checked: Multiple Python, HTML, JS, CSS, CSV files")
    print(f"   Files with 2023: {len(files_with_2023)}")
    print(f"   Status: {'❌ Needs attention' if files_with_2023 else '✅ All updated'}")

if __name__ == "__main__":
    main()
