import os
import shutil
import glob
from google.colab import files
import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def import_files():
    """
    Uploads QIIME2 files, moves them to the appropriate project folder based on R variables,
    and provides an interactive widget for additional file processing.
    """
    # Retrieve 'projects' and 'base_path' from R environment
    projects = str(ro.r["projects"][0])
    base_path = str(ro.r["base_path"][0])  # base_path ends with "/"

    # Upload QIIME2 files from local machine
    uploaded = files.upload()

    # Build the full destination directory path
    dest_dir = os.path.join(base_path, projects, 'qiime2_output')

    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Move uploaded files to the qiime2_output directory
    for filename in uploaded.keys():
        dest_path = os.path.join(dest_dir, filename)
        shutil.move(filename, dest_path)

    # Optionally clear the uploaded dictionary
    del uploaded

    print("Files have been successfully moved to:", dest_dir)

    # Directly process and rename Galaxy file if found
    file_pattern = os.path.join(dest_dir, "Galaxy*.qza")
    matching_files = glob.glob(file_pattern)

    if matching_files:
        old_file = matching_files[0]
        new_file = os.path.join(dest_dir, f"{projects}_classifier.qza")
        os.rename(old_file, new_file)

