import os

path = "." # Current directory
contents = os.listdir(path)
print("List of files and folders:")
for i in contents:
    print(i)