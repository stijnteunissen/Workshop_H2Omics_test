# norm_and_import.py

import os
import shutil
import re
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output 
import rpy2.robjects as ro

def norm_and_import():
    # Dropdown to select normalization method
    norm_dropdown = widgets.Dropdown(
        options=[("fcm", "fcm"), ("qpcr", "qpcr")],
        value="qpcr",
        description="Norm Method:",
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='max-content')
    )

    # Confirm button
    confirm_button = widgets.Button(description="Run Import")

    def on_confirm(b):
        clear_output(wait=True)
        display(norm_dropdown, confirm_button)

        # Assign norm_method to R
        norm_method = norm_dropdown.value
        ro.r.assign("norm_method", norm_method)
        ro.r.assign("copy_correction", ro.BoolVector([True]))
        print("Normalization method assigned to R:", norm_method)

        # Set present_variable_factors based on method
        if norm_method == "fcm":
            factors = ["timepoint", "treatment"]
        elif norm_method == "qpcr":
            factors = ["timepoint", "treatment"]
        else:
            factors = []
            print("Unrecognized norm_method.")

        # Assign to R
        ro.r.assign("present_variable_factors", ro.StrVector(factors))

        # Retrieve R variables and convert to strings
        base_path = str(ro.r("base_path")[0])
        projects = str(ro.r("projects")[0])
        
        project_folder = os.path.join(base_path, projects)
        qiime2_output_folder = os.path.join(project_folder, "qiime2_output")
        git_folder = os.path.join(
            "/content/Workshop_H2Omics_test/H2Omics_workshop/sequencing_data", 
            norm_method
        )
        os.makedirs(qiime2_output_folder, exist_ok=True)

        # Determine the CSV pattern
        if norm_method == "qpcr":
            csv_pattern = re.compile(r".*qPCR.*\.csv$", re.IGNORECASE)
        elif norm_method == "fcm":
            csv_pattern = re.compile(r".*fcm.*\.csv$", re.IGNORECASE)
        else:
            csv_pattern = None

        # Find CSV file
        csv_path = None
        if csv_pattern and os.path.exists(git_folder):
            for file in os.listdir(git_folder):
                if csv_pattern.search(file):
                    csv_path = os.path.join(git_folder, file)
                    break

        # Find TSV file
        tsv_path = None
        tsv_pattern = re.compile(r".*metadata_extra.*\.tsv$", re.IGNORECASE)
        if os.path.exists(git_folder):
            for file in os.listdir(git_folder):
                if tsv_pattern.search(file):
                    tsv_path = os.path.join(git_folder, file)
                    break

        # Display CSV
        if csv_path and os.path.exists(csv_path):
            csv_data = pd.read_csv(csv_path)
            print("CSV File (first 5 rows):")
            display(csv_data.head(5))
            print("\n" + "-"*80 + "\n")
        else:
            print(f"CSV file not found in git folder: {git_folder}")

        # Display TSV
        if tsv_path and os.path.exists(tsv_path):
            tsv_data = pd.read_csv(tsv_path, sep='\t')
            print("TSV File (first 5 rows):")
            display(tsv_data.head(5))
        else:
            print(f"TSV file not found in git folder: {git_folder}")

        # Define file patterns to copy
        file_patterns = [
            r"table.*\.qza$", r"rooted-tree.*\.qza$", r"classifier.*\.qza$", r"metadata\.tsv$",
            r"metadata_extra\.tsv$", r"dna-sequences.*\.csv$", r"fcm.*\.csv$", r"qPCR.*\.csv$", r"prediction.*\.RDS$"
        ]

        # Copy files matching patterns
        if os.path.exists(git_folder):
            for file_name in os.listdir(git_folder):
                if any(re.search(pattern, file_name) for pattern in file_patterns):
                    src = os.path.join(git_folder, file_name)
                    dst = os.path.join(qiime2_output_folder, file_name)
                    shutil.copy2(src, dst)
        else:
            print(f"Git folder not found: {git_folder}")

    confirm_button.on_click(on_confirm)
    display(norm_dropdown, confirm_button)
