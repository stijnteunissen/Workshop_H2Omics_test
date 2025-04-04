copy_number_prediction <- function() {
  message("Copy number prediction completed")

  # Construct the destination folder using the global variable norm_method
  #destination_folder <- paste0("/content/wetsus_repo_analysis/r_visualisation_scripts/H2Omics_workshop/sequencing_data/", norm_method)
  destination_folder <- paste0("/content/Workshop_H2Omics_test/H2Omics_workshop/sequencing_data/", norm_method)

  # List files that match the prediction RDS pattern
  rasperGade16S_file <- list.files(destination_folder, pattern = "prediction\\.RDS$", full.names = TRUE)

  # Read the RDS file
  rasperGade16S_rds <- readRDS(rasperGade16S_file)

  # Create a tibble from the discrete slot and rename/select relevant columns
  raspergade_df <- rasperGade16S_rds$discrete %>%
    dplyr::rename(OTU = label,
                  copy_number = x,
                  probability = probs) %>%
    dplyr::select(OTU, copy_number, probability) %>%
    as_tibble()

  # Construct the qiime output directory path
  qiime_output_dir <- file.path(base_path, projects, "qiime2_output")

  # Define the new file path in the qiime output directory
  new_filepath <- file.path(qiime_output_dir, paste0(projects, "_copy_number_prediction.RDS"))

  # Copy the prediction RDS file to the qiime output directory, overwriting if it exists
  file.copy(from = rasperGade16S_file, to = new_filepath, overwrite = TRUE)

  # Display a message and show the first 10 rows of the tibble
  print(head(raspergade_df, 10))
}
