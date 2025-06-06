import os
import shutil
import glob
from google.colab import files
import rpy2.robjects as ro

def import_files():
    """
    Checks if all required QIIME2 files exist in the project’s qiime2_output folder.
    If any are missing, prompts the user to upload them. After upload, moves files into place,
    renames any Galaxy*.qza to <project>_classifier.qza, and then verifies that all required
    files are now present. If any still missing, raises an error listing them.
    """
    # Retrieve 'projects' and 'base_path' from R environment
    projects = str(ro.r["projects"][0])
    base_path = str(ro.r["base_path"][0])  # base_path should end with "/"
    
    # Build the full destination directory path
    dest_dir = os.path.join(base_path, projects, "qiime2_output")
    os.makedirs(dest_dir, exist_ok=True)
    
    # Define required wildcard patterns (substring must appear and must end with .qza)
    required_patterns = {
        "table*.qza":                "file containing 'table' and ending with .qza",
        "classifier*.qza":           "file containing 'classifier' and ending with .qza",
        "rooted-tree*.qza":          "file containing 'rooted-tree' and ending with .qza",
        "representative_sequences*.qza": "file containing 'representative_sequences' and ending with .qza"
    }
    # metadata_extra can be .txt, .tsv, or .csv
    metadata_patterns = ["metadata*.tsv", "metadata*.txt", "metadata*.csv"]
    
    def check_missing():
        """Return a list of descriptions of missing required files."""
        missing = []
        for pattern, description in required_patterns.items():
            if not glob.glob(os.path.join(dest_dir, pattern)):
                missing.append(description)
        # For metadata: require at least one of the three extensions
        if not any(glob.glob(os.path.join(dest_dir, pat)) for pat in metadata_patterns):
            missing.append("metadata file ending in .tsv, .txt, or .csv")
        return missing
    
    # Initial check
    missing = check_missing()
    if not missing:
        print("All required files are already present in:", dest_dir)
        # Rename any Galaxy*.qza if found
        galaxy_files = glob.glob(os.path.join(dest_dir, "Galaxy*.qza"))
        if galaxy_files:
            old_file = galaxy_files[0]
            new_file = os.path.join(dest_dir, f"{projects}_classifier.qza")
            os.rename(old_file, new_file)
            print(f"Renamed '{os.path.basename(old_file)}' to '{os.path.basename(new_file)}'.")
        return
    
    # If some files are missing, prompt for upload
    print("Missing required files:", ", ".join(missing))
    print("Please upload the missing files now.")
    
    # Upload files
    uploaded = files.upload()
    for filename in uploaded.keys():
        dest_path = os.path.join(dest_dir, filename)
        shutil.move(filename, dest_path)
    del uploaded
    print("Uploaded files moved to:", dest_dir)
    
    # After upload, rename Galaxy*.qza if present
    galaxy_files = glob.glob(os.path.join(dest_dir, "Galaxy*.qza"))
    if galaxy_files:
        old_file = galaxy_files[0]
        new_file = os.path.join(dest_dir, f"{projects}_classifier.qza")
        os.rename(old_file, new_file)
        print(f"Renamed '{os.path.basename(old_file)}' to '{os.path.basename(new_file)}'.")
    
    # Final check
    still_missing = check_missing()
    if still_missing:
        error_msg = (
            "Error: The following required files are still missing after upload:\n  - "
            + "\n  - ".join(still_missing)
        )
        raise FileNotFoundError(error_msg)
    
    print("All required files are now present in:", dest_dir)
