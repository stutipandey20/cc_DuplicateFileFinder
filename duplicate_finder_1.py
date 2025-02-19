import os
import hashlib

class DuplicateFileFinder:
    def __init__(self, directory):
        # Initialize with the target directory
        self.directory = directory
        self.files_list = []
        self.size_map = {} # dictionary to store files grouped by size

    def scan_directory(self):
        # step 1: recursively scans the directory and lists all files
        # step 2: Recursively scans the directory and records file paths.
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)

                self.files_list.append(file_path)
                if file_size in self.size_map:
                    self.size_map[file_size].append(file_path)
                else:
                    self.size_map[file_size] = [file_path]

    # Step 2:
    def find_potential_duplicates(self):
        # Identify potential duplicates based on file sizes
        print("\nPotential Duplicate Files (Same Size):")
        duplicates_found = False

        for size, files in self.size_map.items():
            if len(files) > 1:
                duplicates_found = True
                print(f"Files of size {size} bytes:")
                for file in files:
                    print(f"  - {file}")

        if not duplicates_found:
            print("No potential duplicates found.")

    def list_files(self):
        # display all the files found in the directory
        print("\n Files found in the directory are:")
        for file in self.files_list:
            print(file)

if __name__ == "__main__":
    directory = input("Enter the directory to scan: ")

    if not os.path.exists(directory):
        print("Invalid directory, please enter a valid path")
    else:
        finder = DuplicateFileFinder(directory)
        finder.scan_directory()
        finder.list_files()
        finder.find_potential_duplicates()

# not a very reliable method as it checks the size of the files to compare/ check duplicate
# a number of files can have similar size, but different contents
