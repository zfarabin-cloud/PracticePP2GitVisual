# copy_delete_files.py
import os

# Python program to delete file by specified path.
# Before deleting check for access and whether a given path exists or not.
def delete_file_if_exists(file_path):

    if os.path.exists(file_path):
        if os.access(file_path, os.W_OK):
                os.remove(file_path)

# Delete Folder
os.rmdir("myfolder")

# Python program to copy the contents of a file to another file
def copy(source, destinatioin):

    with open(source, "r") as src:
        with open(destinatioin, "w") as dest:
            for line in src:
                dest.write(line)

