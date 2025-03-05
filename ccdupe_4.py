import os
import sys
import hashlib
from collections import defaultdict

'''
This class is for final byte by byte comparison among duplicate files.
Now that we have true duplicates based on hashing, we will perform a final check 
to ensure that the files are 100% identical by comparing them byte by byte.

✅ Why is this necessary?

Although MD5 collisions are rare, they can happen.
Instead of relying only on hashing, we compare every byte of each file to confirm they are exact duplicates.

'''

class DuplicateFileFinder:
    def __init__(self, directory):
        self.directory = directory
        self.size_map = defaultdict(list)  # Group files by size
        self.hash_map = defaultdict(list)  # Group files by hash
        self.verified_duplicates = []  # Stores truly identical files

    def scan_directory(self):
        """ Recursively scans the directory and groups files by size. """
        try:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)  # Get file size
                    
                    # Store files with the same size together
                    self.size_map[file_size].append(file_path)
        except Exception as e:
            print(f"❌ Error scanning directory: {e}")

    def get_file_hash(self, file_path):
        """ Computes the MD5 hash of a file. """
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
        """ Compares two files byte by byte to confirm they are identical. """
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
        """ Identifies exact duplicate files using MD5 hashing. """
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
    if len(sys.argv) != 2:
        print("Usage: python ccdupe.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"❌ Invalid directory: {directory}")
        sys.exit(1)

    print(f"\n📂 Scanning directory: {directory}")

    finder = DuplicateFileFinder(directory)
    finder.scan_directory()
    finder.find_true_duplicates()

"""
Running Script:
    python3 ccdupe_4.py test_data
"""

'''
📌 How It Works
    Hashes files with MD5 (Step 3).
    Identifies potential duplicates using hash comparisons.
    Performs a byte-by-byte comparison to verify that files are truly identical.
    Displays only confirmed duplicates.
'''