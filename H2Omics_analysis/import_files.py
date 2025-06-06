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
    dest_dir = os.path.join(base_path, projects, 'qiime2_output')
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    # Define required filenames
    required = [
        "table.qza",
        "classifier.qza",
        "rooted-tree.qza",
        "representative_sequences.qza",
        "metadata.tsv"
    ]
    # metadata_extra can be .txt, .tsv, or .csv
    extra_patterns = ["metadata_extra.tsv", "metadata_extra.txt", "metadata_extra.csv"]
    
    def check_missing():
        """Return a list of missing required files (wildcard for metadata_extra)."""
        missing = []
        for fname in required:
            if not os.path.exists(os.path.join(dest_dir, fname)):
                missing.append(fname)
        if not any(os.path.exists(os.path.join(dest_dir, p)) for p in extra_patterns):
            missing.append("metadata_extra.(tsv/text/csv)")
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
        error_msg = ("Error: The following required files are still missing "
                     f"after upload: {', '.join(still_missing)}")
        raise FileNotFoundError(error_msg)
    
    print("All required files are now present in:", dest_dir)