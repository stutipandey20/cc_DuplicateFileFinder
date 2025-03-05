Duplicate File Finder (ccdupe.py)

This project is from John Crickett Coding Challenges

📌 Description

This Python script scans a given directory recursively to detect and identify duplicate files.
It uses a multi-step approach to efficiently find and confirm duplicate files:

File Size Filtering – Groups files by size to eliminate non-duplicates quickly.

MD5 Hashing – Generates unique hash values for files with the same size.

Byte-by-Byte Comparison – Confirms whether files are truly identical.

(Future Feature) Option to delete duplicates or ignore files below a certain size.

✅ Features

Recursively scans a directory and subdirectories.

Groups files based on size as an initial filter.

Uses MD5 hashing to find likely duplicates.

Performs a byte-by-byte comparison for 100% accuracy.

Displays a list of confirmed duplicate files.

🚀 Usage

Run the script from the terminal:

python3 ccdupe.py <directory_path>

Example:

python3 ccdupe_1.py test_data

Sample Output:

📂 Scanning directory: test_data

🔍 Checking for true duplicates using MD5 hashing...

✅ Verifying duplicates with byte-by-byte comparison...

🔥 Confirmed Duplicates:
  - test_data/file1 == test_data/file21
  - test_data/file1 == test_data/subdir/duplicate_of_file1

📋 Requirements

Python 3.8+

Works on Windows, macOS, and Linux

📅 Future Enhancements

🛠 Step 5: Ignore files below a certain size.

🗑 Step 6: Allow users to delete duplicate files interactively.

📄 Step 7: Save the duplicate file report to a log file.

📜 License

This project is licensed under the MIT License.

👤 Author

Stuti Pandey

