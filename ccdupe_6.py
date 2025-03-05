import os
import sys
import hashlib
from collections import defaultdict

"""
Now that we can identify confirmed duplicates, we will allow the user to interactively delete duplicates by choosing which file to keep.
    ✅ What we’ll add in this step:

    Prompt the user to choose which duplicate file to delete.
    Provide a numbered list of duplicate files.
    Delete the selected file while keeping the other.
    Allow skipping deletion by entering an invalid option.

"""

class DuplicateFileFinder:
    def __init__(self, directory, min_size=0):
        self.directory = directory
        self.min_size = min_size  # Ignore files smaller than this size
        self.size_map = defaultdict(list)  # Group files by size
        self.hash_map = defaultdict(list)  # Group files by hash
        self.verified_duplicates = []  # Stores truly identical files

    def scan_directory(self):
        """ Recursively scans the directory and groups files by size, filtering small files. """
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
        """ Identifies exact duplicate files using MD5 hashing and byte-by-byte comparison. """
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

        # Display final confirmed duplicates and allow deletion
        if self.verified_duplicates:
            print("\n🔥 Confirmed Duplicates:")
            for file1, file2 in self.verified_duplicates:
                print(f"  1) {file1}")
                print(f"  2) {file2}")

                choice = input("\nWhich file should be deleted? (Enter 1 or 2, any other key to skip): ")

                if choice == "1":
                    os.remove(file1)
                    print(f"🗑 Deleted: {file1}")
                elif choice == "2":
                    os.remove(file2)
                    print(f"🗑 Deleted: {file2}")
                else:
                    print("✅ Skipping deletion.")

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
    📌 How It Works
    Prompts the user to choose which duplicate file to delete.
    Displays a numbered list (1 or 2) of duplicate files.
    Deletes the selected file, keeping the other.
    Skips deletion if the user enters an invalid option
"""

"""
Running Script:
    python3 ccdupe_6.py test_data
"""