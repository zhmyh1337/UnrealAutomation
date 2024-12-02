import os
import shutil
from . import config, ctx


def delete_directory_contents(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # Loop through the contents of the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # If it's a file, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it's a directory, remove it recursively
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def execute():
    delete_directory_contents(ctx.output_dir)
    return True
