import os
import shutil
import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def starting_project():
    # Define the main directory as in the original R script
    main_dir = "drive/MyDrive/H2Omics_data_analysis"
    
    # Create the main folder if it does not exist
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
        print("Main folder 'H2Omics_data_analysis' created.")
    else:
        print("Main folder 'H2Omics_data_analysis' already exists.")
    
    # Find existing project folders (directly under main_dir)
    existing_projects = [d for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]
    
    # Set up options for the dropdown
    if not existing_projects:
        start_new_project = True
        options = ["Start new project"]
    else:
        start_new_project = False
        options = existing_projects + ["Start new project"]
    
    # Widgets for project selection and creation
    project_dropdown = widgets.Dropdown(
        options=options,
        description="Project:"
    )
    new_project_text = widgets.Text(
        description="New Project Name:",
        placeholder="Enter project name"
    )
    confirm_button = widgets.Button(description="Confirm Project")
    output = widgets.Output()
    
    # Function to create the project structure (similar to create_project_structure in R)
    def create_project_structure(project_name, base_folder):
        # Path to the r_visualisation folder
        r_vis_path = os.path.join(base_folder, "r_visualisation")
        # Path to the project folder inside r_visualisation
        project_path = os.path.join(r_vis_path, project_name)
        # Path to the qiime2_output folder
        qiime2_output_path = os.path.join(project_path, "qiime2_output")
        
        # Create the r_visualisation folder if it doesn't exist
        if not os.path.exists(r_vis_path):
            os.makedirs(r_vis_path)
            print(f"Folder 'r_visualisation' created in {base_folder}.")
        else:
            print(f"Folder 'r_visualisation' already exists in {base_folder}.")
        
        # Create the project folder and the qiime2_output subfolder
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            print(f"Project folder '{project_name}' created in r_visualisation.")
        else:
            print(f"Project folder '{project_name}' already exists in r_visualisation.")
        
        if not os.path.exists(qiime2_output_path):
            os.makedirs(qiime2_output_path)
            print(f"Folder 'qiime2_output' created in {project_path}.")
        else:
            print(f"Folder 'qiime2_output' already exists in {project_path}.")
        
        # Ensure that r_vis_path ends with an os.sep (e.g., '/')
        base_path = r_vis_path if r_vis_path.endswith(os.sep) else r_vis_path + os.sep
        return project_path, base_path, qiime2_output_path

    # Function to show/hide widgets depending on the selection
    def on_project_change(change):
        if change['new'] == "Start new project":
            new_project_text.layout.display = 'block'
        else:
            new_project_text.layout.display = 'none'
    
    if not start_new_project:
        project_dropdown.observe(on_project_change, names="value")
    
    new_project_text.layout.display = 'block' if start_new_project else 'none'
    
    # Handle the confirmation button click
    def on_confirm_clicked(b):
        with output:
            output.clear_output()
            # If there are no existing projects or "Start new project" is chosen:
            if start_new_project or project_dropdown.value == "Start new project":
                project_name = new_project_text.value.strip()
                if project_name == "":
                    print("Please enter a project name.")
                    return
                project_folder = os.path.join(main_dir, project_name)
                if not os.path.exists(project_folder):
                    os.makedirs(project_folder)
                    print(f"New project folder '{project_name}' created in the main folder.")
                else:
                    print(f"Project folder '{project_name}' already exists. Continuing with the existing folder.")
            else:
                project_name = project_dropdown.value
                project_folder = os.path.join(main_dir, project_name)
                print(f"Using existing project folder: {project_name}")
            
            # Create the project structure
            project_path, base_path, qiime2_output_path = create_project_structure(project_name, project_folder)
            
            # If an existing project is chosen, try copying files from the 'qiime_analysis/output' folder
            if not start_new_project and project_dropdown.value != "Start new project":
                source_path = os.path.join(project_folder, "qiime_analysis", "output")
                if os.path.exists(source_path):
                    files_to_copy = os.listdir(source_path)
                    for item in files_to_copy:
                        s = os.path.join(source_path, item)
                        d = os.path.join(qiime2_output_path, item)
                        try:
                            if os.path.isdir(s):
                                shutil.copytree(s, d, dirs_exist_ok=True)
                            else:
                                shutil.copy2(s, d)
                        except Exception as e:
                            print(f"Error copying {s} to {d}: {e}")
                    print(f"Files copied from {source_path} to {qiime2_output_path}.")
                else:
                    print(f"Source folder '{source_path}' does not exist.")
            
            # metadata 
            meta_source = os.path.join(project_folder, "qiime_analysis", "input")
            if os.path.exists(meta_source):
                for fname in os.listdir(meta_source):
                     if "metadata" in fname.lower():
                        s_meta = os.path.join(meta_source, fname)
                        d_meta = os.path.join(qiime2_output_path, fname)
                        try:
                            shutil.copy2(s_meta, d_meta)
                            print(f"Metadata bestand '{fname}' gekopieerd naar qiime2_output.")
                        except Exception as e:
                            print(f"Error copying metadata {s_meta} to {d_meta}: {e}")
                else:
                    print(f"Input folder voor metadata '{meta_source}' bestaat niet.")
            
            # Display project information
            print("Project name (projects):", project_name)
            print("Base path to r_visualisation:", base_path)
            
            # Assign the variables to the R environment via rpy2
            ro.r.assign("projects", project_name)
            ro.r.assign("base_path", base_path)
            print("Variables assigned to R.")
    
    confirm_button.on_click(on_confirm_clicked)
    
    # Display the widgets
    if not start_new_project:
        display(project_dropdown)
    display(new_project_text, confirm_button, output)
