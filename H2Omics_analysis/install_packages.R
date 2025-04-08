install_packages <- function() {
  # Define the custom library folder on your Google Drive for phyloseq
  drive_lib <- "/content/drive/MyDrive/Rlibs"  # "/content/Workshop_H2Omics_test/H2Omics_analysis/Rlibs"
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

  if (!requireNamespace("decontam", quietly = TRUE, lib.loc = drive_lib)) {
    suppressMessages(BiocManager::install("decontam", lib = drive_lib, quiet = TRUE, update = TRUE, ask = FALSE))
  }
  suppressMessages(library(decontam, lib.loc = drive_lib))

  # The following packages will be installed in the temporary environment:
  if (!requireNamespace("glue", quietly = TRUE)) {
    install.packages("glue", quiet = TRUE)
  }
  suppressMessages(library(glue))

  if (!requireNamespace("parallel", quietly = TRUE)) {
    install.packages("parallel", quiet = TRUE)
  }
  suppressMessages(library(parallel))

  if (!requireNamespace("tinytex", quietly = TRUE)) {
    install.packages("tinytex", quiet = TRUE)
  }
  suppressMessages(library(tinytex))

  if (!requireNamespace("vegan", quietly = TRUE)) {
    install.packages("vegan", quiet = TRUE)
  }
  suppressMessages(library(vegan))

  if (!requireNamespace("openxlsx", quietly = TRUE)) {
    install.packages("openxlsx", quiet = TRUE)
  }
  suppressMessages(library(openxlsx))

  if (!requireNamespace("ggtext", quietly = TRUE)) {
    install.packages("ggtext", quiet = TRUE)
  }
  suppressMessages(library(ggtext))

  if (!requireNamespace("cowplot", quietly = TRUE)) {
    install.packages("cowplot", quiet = TRUE)
  }
  suppressMessages(library(cowplot))

  if (!requireNamespace("lubridate", quietly = TRUE)) {
    install.packages("lubridate", quiet = TRUE)
  }
  suppressMessages(library(lubridate))

  if (!requireNamespace("scales", quietly = TRUE)) {
    install.packages("scales", quiet = TRUE)
  }
  suppressMessages(library(scales))

  if (!requireNamespace("viridis", quietly = TRUE)) {
    install.packages("viridis", quiet = TRUE)
  }
  suppressMessages(library(viridis))

  if (!requireNamespace("ggrepel", quietly = TRUE)) {
    install.packages("ggrepel", quiet = TRUE)
  }
  suppressMessages(library(ggrepel))

  if (!requireNamespace("ggforce", quietly = TRUE)) {
    install.packages("ggforce", quiet = TRUE)
  }
  suppressMessages(library(ggforce))

  if (!requireNamespace("config", quietly = TRUE)) {
    install.packages("config", quiet = TRUE)
  }
  suppressMessages(library(config))

  if (!requireNamespace("yaml", quietly = TRUE)) {
    install.packages("yaml", quiet = TRUE)
  }
  suppressMessages(library(yaml))

  if (!requireNamespace("colorspace", quietly = TRUE)) {
    install.packages("colorspace", quiet = TRUE)
  }
  suppressMessages(library(colorspace))

  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    install.packages("jsonlite", quiet = TRUE)
  }
  suppressMessages(library(jsonlite))

  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    install.packages("jsonlite", quiet = TRUE)
  }
  suppressMessages(library(jsonlite))

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

  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    install.packages("jsonlite", quiet = TRUE)
  }
  suppressMessages(library(jsonlite))

  if (!requireNamespace("castor", quietly = TRUE)) {
    install.packages("castor", quiet = TRUE)
  }
  suppressMessages(library(castor))

  if (!requireNamespace("seqinr", quietly = TRUE)) {
    install.packages("seqinr", quiet = TRUE)
  }
  suppressMessages(library(castor))

  if (!requireNamespace("devtools", quietly = TRUE)) {
    install.packages("devtools", quiet = TRUE)
  }
  suppressMessages(library(devtools))

  # Install micromics from GitHub in the temporary environment (default library)
  suppressMessages(devtools::install_github("stijnteunissen/micromics", force = TRUE, quiet = TRUE))
  suppressMessages(library(micromics))

  if (!requireNamespace(c("SparseArray", "DelayedArray", "S4Arrays", "SummarizedExperiment", "SingleCellExperiment", "TreeSummarizedExperiment", "treeio", "microbiome"), quietly = TRUE)) {
    BiocManager::install(
      c("SparseArray", "DelayedArray", "S4Arrays", "SummarizedExperiment", "SingleCellExperiment", "TreeSummarizedExperiment", "treeio", "microbiome"),
      quiet = TRUE, update = TRUE, ask = FALSE)
  }
  suppressMessages(library("SparseArray"))
  suppressMessages(library("DelayedArray"))
  suppressMessages(library("S4Arrays"))
  suppressMessages(library("SummarizedExperiment"))
  suppressMessages(library("SingleCellExperiment",))
  suppressMessages(library("TreeSummarizedExperiment"))
  suppressMessages(library("treeio"))
  suppressMessages(library("microbiome"))

  if (!requireNamespace("qiime2R", quietly = TRUE)) {
    devtools::install_github("jbisanz/qiime2R", quiet = TRUE)
  }
  suppressMessages(library(qiime2R))

  if (!requireNamespace("tidyverse", quietly = TRUE)) {
    devtools::install_github("tidyverse", quiet = TRUE)
  }
  suppressMessages(library(tidyverse))

  if (!requireNamespace("RasperGade", quietly = TRUE)) {
    devtools::install_github(repo = "wu-lab-uva/RasperGade", quiet = TRUE)
  }
  suppressMessages(library(RasperGade))

  if (!requireNamespace("RasperGade16S", quietly = TRUE)) {
    devtools::install_github(repo = "wu-lab-uva/RasperGade16S", quiet = TRUE)
  }
  suppressMessages(library(RasperGade16S))

  message("All packages have been installed and loaded.")
}
