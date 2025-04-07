install_packages <- function() {
  # Define the custom library folder on your Google Drive
  drive_lib <- "/content/Workshop_H2Omics_test/H2Omics_analysis/Rlibs"
  if (!dir.exists(drive_lib)) {
    dir.create(drive_lib, recursive = TRUE)
    message("Custom library folder created at: ", drive_lib)
  }

  # Use the custom library path
  .libPaths(c(drive_lib, .libPaths()))

  # Install base CRAN packages in custom library
  cran_packages <- c(
    "parallel", "tinytex", "ggh4x", "vegan", "devtools", "openxlsx", "ape",
    "ggtext", "cowplot", "RColorBrewer", "glue", "lubridate", "scales",
    "viridis", "ggrepel", "ggforce", "config", "yaml", "colorspace", "jsonlite",
    "castor", "seqinr", "dplyr", "tidyverse", "bbmle", "stats4", "pracma"
  )
  for (pkg in cran_packages) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      install.packages(pkg, lib = drive_lib, quiet = TRUE)
    }
    suppressMessages(library(pkg, character.only = TRUE, lib.loc = drive_lib))
  }

  # Install BiocManager
  if (!requireNamespace("BiocManager", quietly = TRUE, lib.loc = drive_lib)) {
    install.packages("BiocManager", lib = drive_lib, quiet = TRUE)
  }
  suppressMessages(library(BiocManager, lib.loc = drive_lib))

  # Install Bioconductor packages
  bioc_packages <- c(
    "phyloseq", "decontam", "SparseArray", "DelayedArray", "S4Arrays",
    "SummarizedExperiment", "SingleCellExperiment", "TreeSummarizedExperiment",
    "treeio", "microbiome"
  )
  for (pkg in bioc_packages) {
    suppressMessages(BiocManager::install(pkg, lib = drive_lib, quiet = TRUE, update = TRUE, ask = FALSE))
    suppressMessages(library(pkg, character.only = TRUE, lib.loc = drive_lib))
  }

  # Install GitHub packages
  suppressMessages(devtools::install_github("stijnteunissen/micromics", quiet = TRUE))
  suppressMessages(devtools::install_github("jbisanz/qiime2R", quiet = TRUE))
  suppressMessages(devtools::install_github("wu-lab-uva/RasperGade", quiet = TRUE))
  suppressMessages(devtools::install_github("wu-lab-uva/RasperGade16S", quiet = TRUE))

  # Load GitHub packages
  github_packages <- c("qiime2R", "micromics", "RasperGade", "RasperGade16S")
  for (pkg in github_packages) {
    suppressMessages(library(pkg, character.only = TRUE))
  }

  message("All packages have been installed and loaded.")
}
