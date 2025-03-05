import os
import sys
import hashlib
from collections import defaultdict

"""
    In Step 5, we added support for an optional command-line argument --minsize=N, 
    which allows users to ignore files smaller than N bytes.

    Why? Helps focus on larger files when freeing up disk space.
    How? During directory scanning, we skip files smaller than min_size, reducing unnecessary processing.
    What it does? Filters out small files before performing duplicate detection, making the script more efficient and customizable. 🚀
"""

class DuplicateFileFinder:
    def __init__(self, directory, min_size=0):
        self.directory = directory
        self.min_size = min_size  # Ignore files smaller than this size
        self.size_map = defaultdict(list)  # Group files by size
        self.hash_map = defaultdict(list)  # Group files by hash
        self.verified_duplicates = []  # Stores truly identical files

    def scan_directory(self):
        # Recursively scans the directory and groups files by size, filtering small files.
        try:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)  # Get file size
                    
                    # Ignore files smaller than min_size
                    if file_size < self.min_size:
                        continue  

                    self.size_map[file_size].append(file_path)
        except Exception as e:
            print(f"❌ Error scanning directory: {e}")

    def get_file_hash(self, file_path):
        # Computes the MD5 hash of a file. 
        hasher = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):  # Read file in chunks (efficient)
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"❌ Error hashing file {file_path}: {e}")
            return None

    def byte_by_byte_comparison(self, file1, file2):
        # Compares two files byte by byte to confirm they are identical. 
        try:
            with open(file1, "rb") as f1, open(file2, "rb") as f2:
                while True:
                    chunk1 = f1.read(4096)
                    chunk2 = f2.read(4096)

                    if chunk1 != chunk2:
                        return False  # Files are different

                    if not chunk1:  # End of file
                        break
            return True  # Files are identical
        except Exception as e:
            print(f"❌ Error comparing files {file1} and {file2}: {e}")
            return False

    def find_true_duplicates(self):
        # Identifies exact duplicate files using MD5 hashing and byte-by-byte comparison. 
        print("\n🔍 Checking for true duplicates using MD5 hashing...")

        for file_size, files in self.size_map.items():
            if len(files) > 1:  # Only hash files that have potential duplicates
                for file in files:
                    file_hash = self.get_file_hash(file)

                    if file_hash:
                        self.hash_map[file_hash].append(file)

        # Byte-by-byte verification
        print("\n✅ Verifying duplicates with byte-by-byte comparison...")

        for file_hash, files in self.hash_map.items():
            if len(files) > 1:  # Confirmed hash duplicates
                for i in range(len(files)):
                    for j in range(i + 1, len(files)):
                        if self.byte_by_byte_comparison(files[i], files[j]):
                            self.verified_duplicates.append((files[i], files[j]))

        # Display final confirmed duplicates
        if self.verified_duplicates:
            print("\n🔥 Confirmed Duplicates:")
            for file1, file2 in self.verified_duplicates:
                print(f"  - {file1} == {file2}")
        else:
            print("✅ No final duplicate files found after byte-by-byte comparison.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ccdupe.py <directory_path> [--minsize=N]")
        sys.exit(1)

    directory = sys.argv[1]
    min_size = 0

    # Check for optional --minsize argument
    if len(sys.argv) == 3 and sys.argv[2].startswith("--minsize="):
        try:
            min_size = int(sys.argv[2].split("=")[1])
        except ValueError:
            print("❌ Invalid minsize value. Please enter a valid number.")
            sys.exit(1)

    if not os.path.isdir(directory):
        print(f"❌ Invalid directory: {directory}")
        sys.exit(1)

    print(f"\n📂 Scanning directory: {directory} (Ignoring files smaller than {min_size} bytes)")

    finder = DuplicateFileFinder(directory, min_size)
    finder.scan_directory()
    finder.find_true_duplicates()

"""
Running Script:
    Without --minsize (default: considers all files)
        python3 ccdupe_5.py test_data

    Ignoring files smaller than 1000 bytes
        python3 ccdupe_5.py test_data --minsize=1000
"""

""" 
    min_size = int(sys.argv[2].split("=")[1])
    Splits the string "--minsize=1000" into => ["--minsize", "1000"]
    The "=" is the separator.

    .split("=")[1]
    Extracts the second part (index 1), which is "1000".

    int(...)
    Converts "1000" (a string) into an integer (1000).
"""

