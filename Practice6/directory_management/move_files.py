# move_files.py
import os
import shutil

# 1. Renaming a file using os
# Ensure 'myfile.txt' exists from your write_files.py practice
if os.path.exists("myfile.txt"):
    os.rename("myfile.txt", "renamed_file.txt")
    print("File renamed to renamed_file.txt")

# 2. Moving a file into a folder using shutil
if not os.path.exists("archive"):
    os.mkdir("archive")

if os.path.exists("renamed_file.txt"):
    shutil.move("renamed_file.txt", "archive/renamed_file.txt")
    print("File moved to 'archive' folder.")