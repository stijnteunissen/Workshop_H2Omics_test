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
    git_folder = os.path.join("/content/drive/MyDrive/H2Omics_workshop/sequencing_data", norm_method)
    
    # Ensure qiime2_output folder exists
    os.makedirs(qiime2_output_folder, exist_ok=True)

    # Read and display the CSV and TSV files, showing only the first 5 rows.
    csv_path = "/content/drive/MyDrive/H2Omics_workshop/sequencing_data/qpcr/ELLY_proj2_HGT_16S_per_mL_sample_qPCR.csv"
    tsv_path = "/content/drive/MyDrive/H2Omics_workshop/sequencing_data/qpcr/ELLY_GMAC_proj2_Q17712_Q17733@qPCR_metadata_extra.tsv"
    
    if os.path.exists(csv_path):
        csv_data = pd.read_csv(csv_path)
        print("CSV File (first 5 rows):")
        display(csv_data.head(5))
        print("\n" + "-"*80 + "\n")
    else:
        print(f"CSV file not found: {csv_path}")

    if os.path.exists(tsv_path):
        tsv_data = pd.read_csv(tsv_path, sep='\t')
        print("TSV File (first 5 rows):")
        display(tsv_data.head(5))
    else:
        print(f"TSV file not found: {tsv_path}")

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
