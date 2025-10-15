#!/usr/bin/env python
"""
Script to update all 2023 dates to 2025 in the HUTANO system
"""

import os
import re
import glob
import shutil
from datetime import datetime

def backup_file(file_path):
    """Create a backup of the file before modifying"""
    backup_path = file_path + '.backup'
    shutil.copy2(file_path, backup_path)
    return backup_path

def update_dates_in_file(file_path):
    """Update all 2023 dates to 2025 in a single file"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Define replacement patterns
        replacements = [
            (r'2023-(\d{2})-(\d{2})', r'2025-\1-\2'),  # 2023-01-01 -> 2025-01-01
            (r'(\d{2})/(\d{2})/2023', r'\1/\2/2025'),  # 01/01/2023 -> 01/01/2025
            (r'(\d{2})-(\d{2})-2023', r'\1-\2-2025'),  # 01-01-2023 -> 01-01-2025
            (r'\b2023\b', '2025'),                      # 2023 -> 2025 (word boundary)
        ]
        
        # Apply replacements
        changes_made = 0
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changes_made += len(re.findall(pattern, content))
                content = new_content
        
        # Write back if changes were made
        if content != original_content:
            # Create backup first
            backup_path = backup_file(file_path)
            
            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return changes_made, backup_path
        
        return 0, None
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return 0, None

def update_all_dates(directory):
    """Update all 2023 dates to 2025 in all relevant files"""
    print("🔄 Starting comprehensive date update from 2023 to 2025...")
    print("=" * 60)
    
    # File patterns to update
    patterns = [
        '**/*.py',
        '**/*.html',
        '**/*.js',
        '**/*.css',
        '**/*.csv',
        '**/*.md',
        '**/*.txt'
    ]
    
    total_files = 0
    total_changes = 0
    updated_files = []
    
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(directory, pattern), recursive=True):
            # Skip backup files and certain directories
            if (file_path.endswith('.backup') or 
                '__pycache__' in file_path or 
                '.git' in file_path or
                'node_modules' in file_path):
                continue
            
            total_files += 1
            changes, backup_path = update_dates_in_file(file_path)
            
            if changes > 0:
                updated_files.append({
                    'file': file_path,
                    'changes': changes,
                    'backup': backup_path
                })
                total_changes += changes
                print(f"✅ Updated {file_path} ({changes} changes)")
    
    print("=" * 60)
    print("📊 Update Summary:")
    print(f"   Total files scanned: {total_files}")
    print(f"   Files updated: {len(updated_files)}")
    print(f"   Total date changes: {total_changes}")
    print()
    
    if updated_files:
        print("📝 Updated files:")
        for file_info in updated_files[:10]:  # Show first 10
            print(f"   - {file_info['file']} ({file_info['changes']} changes)")
        
        if len(updated_files) > 10:
            print(f"   ... and {len(updated_files) - 10} more files")
    
    return updated_files, total_changes

def main():
    """Main function"""
    print("🎯 HUTANO Date Update Tool")
    print("Updating all 2023 dates to 2025 for current data")
    print("=" * 60)
    
    # Check if hutano directory exists
    hutano_dir = "hutano"
    if not os.path.exists(hutano_dir):
        print("❌ HUTANO directory not found!")
        return
    
    # Perform the update
    updated_files, total_changes = update_all_dates(hutano_dir)
    
    print("=" * 60)
    if total_changes > 0:
        print("✅ Date update completed successfully!")
        print(f"🔄 {total_changes} dates updated from 2023 to 2025")
        print("📁 Backup files created for all modified files")
        print()
        print("🎯 Next steps:")
        print("   1. Test the system to ensure everything works")
        print("   2. Upload sample data to see immediate updates")
        print("   3. Check dashboard for current 2025 data")
    else:
        print("ℹ️  No 2023 dates found to update")

if __name__ == "__main__":
    main()
