import os
import sys
import hashlib
from collections import defaultdict

'''
Now that we've identified potential duplicates based on file size, 
we need to confirm true duplicates by hashing file contents.

✅ Why use hashing?
Files can have the same size but different content (e.g., different text files of equal length).
A hash function like MD5 generates a unique "fingerprint" for each file.
If two files have the same MD5 hash, they are almost certainly identical.
'''

class DuplicateFileFinder:
    def __init__(self, directory):
        self.directory = directory
        self.size_map = defaultdict(list)  # Group files by size
        self.hash_map = defaultdict(list)  # Group files by hash

    def scan_directory(self):
        # Recursively scans the directory and groups files by size

        ''' 
        root -> the current directory path being processed
        _ / dirs -> a list of subdirectoris in the current directory
        files -> a list of files in the current directory

        os.walk(directory) is a built-in Python function that recursively traverses a directory tree.
        It returns a generator that yields tuples containing:
        '''
        try:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file) # get the file path
                    file_size = os.path.getsize(file_path) # get the size of the file

                    # store files with the same size together
                    self.size_map[file_size].append(file_path)

        except Exception as e:
            print(f"❌ Error scanning directory: {e}")

    def get_file_hash(self, file_path):
        # Computes the MD5 hash of a file. 
        hasher = hashlib.md5() # an MD5 hash object
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):  # Read file in chunks (efficient)
                    hasher.update(chunk)
            # return the unique identity string of the file
            return hasher.hexdigest() # Converts the final binary hash into a human-readable hexadecimal string
        except Exception as e:
            print(f"❌ Error hashing file {file_path}: {e}")  
            return None

    def find_true_duplicates(self):
        # Identifies exact duplicate files using MD5 hashing.
        print("\n🔍 Checking for true duplicates using MD5 hashing...")

        for file_size, files in self.size_map.items():
            if len(files) > 1:  # Only hash files that have potential duplicates
                for file in files:
                    file_hash = self.get_file_hash(file)

                    if file_hash:
                        self.hash_map[file_hash].append(file)

        # display exact duplicates
        duplicates_found = False
        for file_hash, files in self.hash_map.items():
            if len(files) > 1: # confirmed duplicates
                duplicates_found = True
                print(f"\n✅ True Duplicates (MD5: {file_hash}):")
                for file in files:
                    print(f" - {file}")

        if not duplicates_found:
            print("✅ No exact duplicate files found.")

if __name__ == "__main__":
    if len(sys.argv) != 2: # too few to many arguments
        print("Usage: python3 ccdupe_3.py <directory_path>")
        sys.exit(1) # stops execution and returns exit code 1 (indicating an error).

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
    python3 ccdupe_3.py test_data
"""

'''
    In Python, _ is a convention used to indicate that we are ignoring a value.
    Here, _ is used for dirs because we don’t need subdirectory names.
    equivalent to:
        for root, dirs, files in os.walk(self.directory):
            # We're not using `dirs`, so we replace it with `_`
            # We only process files because finding duplicates is based on files, not directories

    4096 (bytes) is 4 KB, a common block size in file systems.
    Instead of reading the entire file at once (which is memory-intensive for large files), we read it in 4 KB chunks.
    This makes the program more memory-efficient and faster.

    When f.read(4096) returns None or an empty string (""), the loop stops
    := walrus operator

    Equivalent Traditional syntax:
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
            
'''
