import os
import sys
from collections import defaultdict

class DuplicateFileFinder:
    def __init__(self, directory):
        self.directory = directory
        self.size_map = defaultdict(list) # Stores files grouped by size

    def scan_directory(self):
        """ Recursively scans the directory and groups files by size. """
        try:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path) # Get file size

                    # Store files with the same size together
                    self.size_map[file_size].append(file_path)
        except Exception as e:
            print(f"❌ Error scanning directory: {e}")

    def find_potential_duplicates(self):
        """Identifies files with the same size as potential duplicates."""
        print("\n🔍 Potential Duplicate Files (based on size):")

        found_duplicates = False
        for file_size, files in self.size_map.items():
            if len(files) > 1:  # Only consider files with the same size
                found_duplicates = True
                print(f"Potential duplicates ({file_size} bytes):")
                for file in files:
                    print(f" - {file}")

        if not found_duplicates:
            print("✅ No potential duplicates found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ccdupe_2.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"❌ Invalid directory: {directory}")
        sys.exit(1)

    print(f"\n📂 Scanning directory: {directory}")
    finder = DuplicateFileFinder(directory)
    finder.scan_directory()
    finder.find_potential_duplicates()

"""
Running Script:
    python3 ccdupe_2.py test_data
"""