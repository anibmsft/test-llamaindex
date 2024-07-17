import os

# Define the top level directory
top_level_dir = "ingestion"

# Walk through all directories and subdirectories
for dirpath, dirnames, filenames in os.walk(top_level_dir):
    # Create __init__.py in each directory
    print(dirpath)
    open(os.path.join(dirpath, "__init__.py"), 'a').close()

print(f"__init__.py files have been successfully created in all directories and subdirectories of {top_level_dir}.")
