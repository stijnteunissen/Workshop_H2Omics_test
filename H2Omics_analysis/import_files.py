import os
import shutil
from google.colab import files
import glob
import ipywidgets as widgets
from IPython.display import display

def import_files():
    """
    Uploads qiime files, moves them to the designated project folder,
    and provides an interactive widget to process the files.
    
    Args:
        projects (str): The project name.
    """
    # Upload qiime files
    uploaded = files.upload()
    
    # Clean the project name if needed
    projects = str(projects).strip("[]'\"")
    
    # Construct the destination path using the known folder structure
    dest_dir = os.path.join('drive/MyDrive', 'wetsus_data_analysis', projects, 'r_visualisation', projects, 'qiime2_output')
    
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Process and move the uploaded files to the qiime2_output folder
    for filename in uploaded.keys():
        dest_path = os.path.join(dest_dir, filename)
        shutil.move(filename, dest_path)
    
    # Optionally, clear the 'uploaded' dictionary
    del uploaded
    
    print("Files have been successfully moved to:", dest_dir)
    
    # Create a dropdown widget
    dropdown = widgets.Dropdown(
        options=['Galaxy Classification', 'Not Galaxy Classification'],
        value='Galaxy Classification',
        description='Method:',
    )
    
    # Create a button to trigger the action
    button = widgets.Button(description="Continue script")
    
    # Define the function to process files when the button is clicked
    def process_files(b):
        if dropdown.value == 'Galaxy Classification':
            file_pattern = os.path.join(dest_dir, "Galaxy*.qza")
            matching_files = glob.glob(file_pattern)
            
            if matching_files:
                old_file = matching_files[0]
                new_file = os.path.join(dest_dir, f"{projects}_classifier.qza")
                os.rename(old_file, new_file)
                print(f"Renamed {old_file} to {new_file}")
            else:
                print("No file matching 'Galaxy*.qza' found in", dest_dir)
        else:
            print("Skipped processing because 'Not Galaxy Classification' was selected.")
    
    # Bind the button to the process_files function
    button.on_click(process_files)
    
    # Display the dropdown and button
    display(dropdown, button)
