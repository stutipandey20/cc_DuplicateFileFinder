import os
import hashlib

# here we will make use of hashing (MD5) to check for duplicates
# compute the hash of each file
# This will help us confirm which files are truly identical.

class DuplicateFileFinder:
    def __init__(self, directory):
        # Initialize with the target directory.
        self.directory = directory
        self.size_map = {}  # Stores files grouped by size
        self.hash_map = {}  # Stores files grouped by hash

    def scan_directory(self):
        # Recursively scans the directory and records file paths.
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)  # Get file size

                # Group files by size first (pre-filtering step)
                if file_size in self.size_map:
                    self.size_map[file_size].append(file_path)
                else:
                    self.size_map[file_size] = [file_path]

    def get_file_hash(self, file_path):
        # Computes the MD5 hash of a file.
        hasher = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):  # Read file in chunks
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error hashing file {file_path}: {e}")
            return None
        
    def find_true_duplicates(self):
        # Identifies true duplicate files using MD5 hashing.
        print("\n Checking for true duplicates using MD5 hashing...")
        duplicates_found = False

        for files in self.size_map.items():
            if len(files) > 1:  # Only hash files that have potential duplicates
                for file in files:
                    if isinstance(file, str) and os.path.isfile(file):  # ✅ Ensure we only pass a string, not a list or tuple
                        file_hash = self.get_file_hash(file)
                    
                        if file_hash:
                            if file_hash in self.hash_map:
                                self.hash_map[file_hash].append(file)
                                duplicates_found =  True
                            else:
                                self.hash_map[file_hash] = [file]
                    else:
                        print(f"❌ Skipping invalid file entry: {file}")
        
        if duplicates_found:
            print("\nTrue Duplicates Found:")
        for file_hash, files in self.hash_map.items():
            if len(files) > 1:  # Confirmed duplicates
                print(f"MD5 Hash: {file_hash}")
                for file in files:
                    print(f"  - {file}")
        else:
            print("No exact duplicate files found.")

if __name__ == "__main__":
    directory = input("Enter the directory to scan: ")

    if not os.path.exists(directory):
        print("Invalid directory. Please enter a valid path.")
    else:
        finder = DuplicateFileFinder(directory)
        finder.scan_directory()
        finder.print
        # finder.find_true_duplicates()