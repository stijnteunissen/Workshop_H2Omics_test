import os
import shutil
import pandas as pd
from IPython.display import display
import re
import rpy2.robjects as ro

def import_files():
    # Retrieve R variables and convert them to Python strings.
    # Assuming the R variables are defined and are character vectors of length 1.
    base_path = str(ro.r("base_path")[0])
    projects = str(ro.r("projects")[0])
    norm_method = str(ro.r("norm_method")[0])
    
    # Define paths using the retrieved R variables.
    project_folder = os.path.join(base_path, projects)
    qiime2_output_folder = os.path.join(project_folder, "qiime2_output")
    git_folder = os.path.join("/content/Workshop_H2Omics_test/H2Omics_workshop/sequencing_data", norm_method)
    
    # Ensure qiime2_output folder exists
    os.makedirs(qiime2_output_folder, exist_ok=True)
    
    # Bepaal het CSV-bestand op basis van norm_method:
    csv_path = None
    if norm_method.lower() == "qpcr":
        csv_pattern = re.compile(r".*qPCR.*\.csv$", re.IGNORECASE)
    elif norm_method.lower() == "fcm":
        csv_pattern = re.compile(r".*fcm.*\.csv$", re.IGNORECASE)
    else:
        csv_pattern = None

    if csv_pattern and os.path.exists(git_folder):
        for file in os.listdir(git_folder):
            if csv_pattern.search(file):
                csv_path = os.path.join(git_folder, file)
                break

    # Zoek het metadata_extra TSV-bestand in dezelfde git folder.
    tsv_path = None
    tsv_pattern = re.compile(r".*metadata_extra.*\.tsv$", re.IGNORECASE)
    if os.path.exists(git_folder):
        for file in os.listdir(git_folder):
            if tsv_pattern.search(file):
                tsv_path = os.path.join(git_folder, file)
                break

    # Read and display the CSV and TSV files, showing only the first 5 rows.
    if csv_path and os.path.exists(csv_path):
        csv_data = pd.read_csv(csv_path)
        print("CSV File (first 5 rows):")
        display(csv_data.head(5))
        print("\n" + "-"*80 + "\n")
    else:
        print(f"CSV file not found in git folder: {git_folder}")

    if tsv_path and os.path.exists(tsv_path):
        tsv_data = pd.read_csv(tsv_path, sep='\t')
        print("TSV File (first 5 rows):")
        display(tsv_data.head(5))
    else:
        print(f"TSV file not found in git folder: {git_folder}")

    # Define file patterns to search for
    file_patterns = [
        r"table.*\.qza$", r"rooted-tree.*\.qza$", r"classifier.*\.qza$", r"metadata\.tsv$",
        r"metadata_extra\.tsv$", r"dna-sequences.*\.csv$", r"fcm.*\.csv$", r"qPCR.*\.csv$", r"prediction.*\.RDS$"
    ]

    # Iterate through files in git_folder and copy those matching the patterns to qiime2_output_folder
    if os.path.exists(git_folder):
        for file_name in os.listdir(git_folder):
            file_path = os.path.join(git_folder, file_name)

            # Check if the file matches any of the specified patterns
            if any(re.search(pattern, file_name) for pattern in file_patterns):
                dest_path = os.path.join(qiime2_output_folder, file_name)
                shutil.copy2(file_path, dest_path)
                print(f"Copied: {file_path} -> {dest_path}")
    else:
        print(f"Git folder not found: {git_folder}")
