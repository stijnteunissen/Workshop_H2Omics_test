install_packages <- function() {
  # Define the custom library folder on your Google Drive for phyloseq
  drive_lib <- "/content/Workshop_H2Omics_test/H2Omics_workshop/Rlibs"
  if (!dir.exists(drive_lib)) {
    dir.create(drive_lib, recursive = TRUE)
    message("Custom library folder created at: ", drive_lib)
  }

  # Prepend drive_lib to the library paths so it is searched first
  .libPaths(c(drive_lib, .libPaths()))

  # Install BiocManager in the drive library if not already installed there
  if (!requireNamespace("BiocManager", quietly = TRUE, lib.loc = drive_lib)) {
    install.packages("BiocManager", lib = drive_lib, quiet = TRUE)
  }
  suppressMessages(library(BiocManager, lib.loc = drive_lib))

  # Install phyloseq in the drive library if not already installed there
  if (!requireNamespace("phyloseq", quietly = TRUE, lib.loc = drive_lib)) {
    suppressMessages(BiocManager::install("phyloseq", lib = drive_lib, quiet = TRUE, update = TRUE, ask = FALSE))
  }
  suppressMessages(library(phyloseq, lib.loc = drive_lib))

  # The following packages will be installed in the temporary environment:
  if (!requireNamespace("glue", quietly = TRUE)) {
    install.packages("glue", quiet = TRUE)
  }
  suppressMessages(library(glue))

  if (!requireNamespace("dplyr", quietly = TRUE)) {
    install.packages("dplyr", quiet = TRUE)
  }
  suppressMessages(library(dplyr))

  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    install.packages("ggplot2", quiet = TRUE)
  }
  suppressMessages(library(ggplot2))

  if (!requireNamespace("RColorBrewer", quietly = TRUE)) {
    install.packages("RColorBrewer", quiet = TRUE)
  }
  suppressMessages(library(RColorBrewer))

  if (!requireNamespace("scales", quietly = TRUE)) {
    install.packages("scales", quiet = TRUE)
  }
  suppressMessages(library(scales))

  if (!requireNamespace("ggh4x", quietly = TRUE)) {
    install.packages("ggh4x", quiet = TRUE)
  }
  suppressMessages(library(ggh4x))

  if (!requireNamespace("ggtext", quietly = TRUE)) {
    install.packages("ggtext", quiet = TRUE)
  }
  suppressMessages(library(ggtext))

  if (!requireNamespace("rlang", quietly = TRUE)) {
    install.packages("rlang", quiet = TRUE)
  }
  suppressMessages(library(rlang))

  if (!requireNamespace("tibble", quietly = TRUE)) {
    install.packages("tibble", quiet = TRUE)
  }
  suppressMessages(library(tibble))

  if (!requireNamespace("cowplot", quietly = TRUE)) {
    install.packages("cowplot", quiet = TRUE)
  }
  suppressMessages(library(cowplot))

  if (!requireNamespace("devtools", quietly = TRUE)) {
    install.packages("devtools", quiet = TRUE)
  }
  suppressMessages(library(devtools))

  # Install H2Omics from GitHub in the temporary environment (default library)
  suppressMessages(devtools::install_github("stijnteunissen/H2Omics", force = TRUE, quiet = TRUE))
  suppressMessages(library(H2Omics))

  message("All packages have been installed and loaded.")
}
