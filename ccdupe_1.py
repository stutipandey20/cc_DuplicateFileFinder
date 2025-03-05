import os
import sys

def scan_directory(directory):
    """ Recursively scans a directory and prints file paths. """
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                # Get the relative file path from the base directory
                file_path = os.path.relpath(os.path.join(root, file), directory)
                print(file_path)
    except Exception as e:
        print(f"Error scanning directory: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ccdupe.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"❌ Invalid directory: {directory}")
        sys.exit(1)

    print(f"\n📂 Scanning directory: {directory}\n")
    scan_directory(directory)

"""
Running Script:
    python3 ccdupe_1.py test_data
"""