install_packages <- function() {
  options(getClass.msg = FALSE)

  drive_lib <- "/content/Workshop_H2Omics_test/H2Omics_analysis/Rlibs"
  if (!dir.exists(drive_lib)) dir.create(drive_lib, recursive = TRUE)
  .libPaths(c(drive_lib, .libPaths()))

  # Installeer BiocManager indien nodig
  if (!requireNamespace("BiocManager", quietly = TRUE, lib.loc = drive_lib)) {
    install.packages("BiocManager", lib = drive_lib, quiet = TRUE)
  }
  suppressMessages(library(BiocManager, lib.loc = drive_lib))

  # Forceer Bioconductor versie 3.16
  BiocManager::install(version = "3.16", ask = FALSE, quiet = TRUE)
  options(repos = BiocManager::repositories(version = "3.16"))

  # Bioconductor packages
  bioc_pkgs <- c(
    "decontam", "SparseArray", "DelayedArray", "S4Arrays", "SummarizedExperiment",
    "SingleCellExperiment", "TreeSummarizedExperiment", "treeio", "microbiome", "phyloseq"
  )
  for (pkg in bioc_pkgs) {
    if (!requireNamespace(pkg, quietly = TRUE, lib.loc = drive_lib)) {
      BiocManager::install(pkg, lib = drive_lib, quiet = TRUE, ask = FALSE, update = FALSE, version = "3.16")
    }
    suppressMessages(library(pkg, lib.loc = drive_lib, character.only = TRUE))
  }

  # CRAN packages
  cran_pkgs <- c(
    "glue", "parallel", "tinytex", "vegan", "openxlsx", "ggtext", "cowplot", "lubridate",
    "scales", "viridis", "ggrepel", "ggforce", "config", "yaml", "colorspace", "jsonlite",
    "dplyr", "ggplot2", "RColorBrewer", "ggh4x", "rlang", "tibble", "castor", "seqinr", "devtools"
  )
  for (pkg in cran_pkgs) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      install.packages(pkg, quiet = TRUE)
    }
    suppressMessages(library(pkg, character.only = TRUE))
  }

  # GitHub packages
  github_pkgs <- list(
    micromics = "stijnteunissen/micromics",
    qiime2R = "jbisanz/qiime2R",
    RasperGade = "wu-lab-uva/RasperGade",
    RasperGade16S = "wu-lab-uva/RasperGade16S"
  )
  for (pkg in names(github_pkgs)) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      devtools::install_github(github_pkgs[[pkg]], quiet = TRUE)
    }
    suppressMessages(library(pkg, character.only = TRUE))
  }

  # Tidyverse via CRAN
  if (!requireNamespace("tidyverse", quietly = TRUE)) {
    install.packages("tidyverse", quiet = TRUE)
  }
  suppressMessages(library(tidyverse))

  message("lle packages zijn succesvol geïnstalleerd en geladen.")
}
