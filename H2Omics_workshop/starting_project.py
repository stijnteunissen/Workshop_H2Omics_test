import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro
import os

def starting_project():
    
    # Define main directory
    main_dir = "/content/drive/MyDrive/H2Omics_data_analysis"
    
    # Create main directory if it doesn't exist
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
        print("Main folder 'H2Omics_data_analysis' created.")
    else:
        print("Main folder 'H2Omics_data_analysis' already exists.")
    
    # List existing project folders in main_dir
    existing_projects = [d for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]
    
    # Check if there are no existing projects
    if not existing_projects:
        # If no projects exist, force "Start new project" selection
        start_new_project = True
        options = ["Start new project"]
    else:
        start_new_project = False
        options = existing_projects + ["Start new project"]
    
    # Create a dropdown for project selection (if projects exist)
    project_dropdown = widgets.Dropdown(
        options=options,
        description="Project:"
    )
    
    # Create a text input for new project name
    new_project_text = widgets.Text(
        description="New Project Name:",
        placeholder="Enter project name"
    )
    
    # Confirm button to finalize project selection
    confirm_button = widgets.Button(description="Confirm Project")
    
    # Output widget to display messages
    output = widgets.Output()
    
    # Function to handle dropdown changes
    def on_project_change(change):
        if change['new'] == "Start new project":
            new_project_text.layout.display = 'block'
        else:
            new_project_text.layout.display = 'none'
    
    if not start_new_project:
        project_dropdown.observe(on_project_change, names="value")
    
    # Automatically show the text input if no existing projects are found
    new_project_text.layout.display = 'block' if start_new_project else 'none'
    
    # When the confirm button is clicked, process the choice and assign variables to R
    def on_confirm_clicked(b):
        with output:
            output.clear_output()
            # Determine project name
            if start_new_project or project_dropdown.value == "Start new project":
                project_name = new_project_text.value.strip()
                if project_name == "":
                    print("Please enter a project name.")
                    return
                project_folder = os.path.join(main_dir, project_name)
                if not os.path.exists(project_folder):
                    os.makedirs(project_folder)
                    print(f"New project folder '{project_name}' created in main folder.")
                else:
                    print(f"Project folder '{project_name}' already exists. Continuing with existing folder.")
            else:
                project_name = project_dropdown.value
                project_folder = os.path.join(main_dir, project_name)
                print(f"Using existing project folder: {project_name}")
            
            # Create the r_visualisation folder inside the project folder if it doesn't exist
            r_vis_path = os.path.join(project_folder, "r_visualisation")
            if not os.path.exists(r_vis_path):
                os.makedirs(r_vis_path)
                print(f"Folder 'r_visualisation' created in {project_folder}.")
            else:
                print(f"Folder 'r_visualisation' already exists in {project_folder}.")
            
            # Define base_path as the r_visualisation folder path, ensuring it ends with '/'
            base_path = r_vis_path if r_vis_path.endswith('/') else r_vis_path + '/'
            print("Project name (projects):", project_name)
            print("Base path to r_visualisation:", base_path)
            
            # Pass the variables to R using rpy2
            ro.r.assign("projects", project_name)
            ro.r.assign("base_path", base_path)
            print("Variables assigned to R.")
    
    confirm_button.on_click(on_confirm_clicked)
    
    # Display the widgets
    if not start_new_project:
        display(project_dropdown)
    display(new_project_text, confirm_button, output)
