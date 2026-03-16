# create_list_dirs.py
import os

# Create a single directory
if not os.path.exists("test_folder"):
    os.mkdir("test_folder")
    print("Directory 'test_folder' created.")

# Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)

# List all files and folders in the current directory
print("\nContents of current directory:")
content_list = os.listdir(".")
for item in content_list:
    print(f"- {item}")

# Distinguish between files and directories
print("\nDetailed view:")
for item in content_list:
    if os.path.isdir(item):
        print(f"[DIR]  {item}")
    else:
        print(f"[FILE] {item}")