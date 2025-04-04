strarting_project <- function() {

  main_dir = "drive/MyDrive/wetsus_data_analysis"
  # Set the main directory (adjust the path if needed)
  if (!dir.exists(main_dir)) {
    dir.create(main_dir, recursive = TRUE)
    message("Main folder 'wetsus_data_analysis' created.")
  } else {
    message("Main folder 'wetsus_data_analysis' already exists.")
  }

  # Function to create the project structure
  create_project_structure <- function(project_name, base_folder) {
    # Define the paths
    r_vis_path <- file.path(base_folder, "r_visualisation")
    project_path <- file.path(r_vis_path, project_name)
    qiime2_output_path <- file.path(project_path, "qiime2_output")

    # Create the r_visualisation folder if it doesn't exist
    if (!dir.exists(r_vis_path)) {
      dir.create(r_vis_path)
      message("Folder 'r_visualisation' created in ", base_folder)
    }

    # Create the project folder and qiime2_output subfolder
    if (!dir.exists(project_path)) {
      dir.create(project_path)
      message("Project folder '", project_name, "' created in r_visualisation.")
    }
    if (!dir.exists(qiime2_output_path)) {
      dir.create(qiime2_output_path)
      message("Folder 'qiime2_output' created in ", project_path)
    }

    # Set base_path to the r_visualisation folder
    base_path <- ifelse(substr(r_vis_path, nchar(r_vis_path), nchar(r_vis_path)) == "/",
                        r_vis_path,
                        paste0(r_vis_path, "/"))
    return(list(projects = project_name, base_path = base_path))
  }

  # Present the user with two options
  cat("Choose an option:\n")
  cat("1: Use an existing project folder\n")
  cat("2: Create a new project folder\n")
  choice <- as.numeric(readline(prompt = "Enter 1 or 2: "))

  if (choice == 1) {
    # List the existing subdirectories (project folders) in the main folder
    existing_projects <- list.dirs(main_dir, full.names = FALSE, recursive = FALSE)
    if (length(existing_projects) == 0) {
      stop("No existing project folders found. Please choose option 2 to create a new folder.")
    }

    cat("Existing project folders:\n")
    for (i in seq_along(existing_projects)) {
      cat(i, ": ", existing_projects[i], "\n")
    }
    sel <- as.numeric(readline(prompt = "Choose a folder (enter the number): "))
    if (is.na(sel) || sel < 1 || sel > length(existing_projects)) {
      stop("Invalid choice!")
    }
    chosen_folder <- file.path(main_dir, existing_projects[sel])
    project_name <- existing_projects[sel]  # Use the existing folder name as the project name

    # Create the r_visualisation structure and copy files
    res <- create_project_structure(project_name, chosen_folder)

    # Define source and destination paths for copying files
    source_path <- file.path(chosen_folder, "qiime_anlayseis", "output")
    dest_path <- file.path(chosen_folder, "r_visualisation", project_name, "qiime2_output")

    if (dir.exists(source_path)) {
      files_to_copy <- list.files(source_path, full.names = TRUE)
      file.copy(from = files_to_copy, to = dest_path, recursive = TRUE)
      message("Files copied from ", source_path, " to ", dest_path)
    } else {
      message("Source folder '", source_path, "' does not exist.")
    }

  } else if (choice == 2) {
    # Create a new project folder
    project_name <- readline(prompt = "Enter a name for the new project: ")
    new_project_path <- file.path(main_dir, project_name)
    if (!dir.exists(new_project_path)) {
      dir.create(new_project_path)
      message("New project folder '", project_name, "' created in main folder.")
    } else {
      message("Project folder already exists. Continuing with the existing folder.")
    }

    res <- create_project_structure(project_name, new_project_path)

    # Inform the user about uploading files
    message("Now upload files to the folder: ",
            file.path(new_project_path, "r_visualisation", project_name, "qiime2_output"))
    message("For uploading, use the Python snippet provided in the next cell.")

  } else {
    stop("Invalid choice!")
  }

  # Save the desired variables in the R environment
  projects <- res$projects
  base_path <- res$base_path

  cat("Project name (projects):", projects, "\n")
  cat("Base path to r_visualisation:", base_path, "\n")

  return(list(projects = projects, base_path = base_path))
}
