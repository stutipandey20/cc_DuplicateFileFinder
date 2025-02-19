import os
import hashlib

class DuplicateFileFinder:
    def __init__(self, directory):
        # Initialize with the target directory
        self.directory = directory
        self.files_list = []

    def scan_directory(self):
        # step 1: recursively scans the directory and lists all files
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)

                self.files_list.append(file_path)

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
        

# only lists down the files which are there in the directory