copy_number_prediction = function() {

  micromamba_path <- "/content/envs/epa-env/bin"
  Sys.setenv(PATH = paste(micromamba_path, Sys.getenv("PATH"), sep = ":"))

# Set the qiime2 output directory (using base_path and projects)
qiime_output_dir <- file.path(base_path, projects, "qiime2_output")

qza_file = list.files(qiime_output_dir, pattern = "representative_sequences\\.qza$", full.names = TRUE)
temp_dir = tempfile("rep_seq_")
dir.create(temp_dir)
utils::unzip(qza_file, exdir = temp_dir)

# Find the FASTA file that ends with "dna-sequence.FASTA"
fasta_file = list.files(path = temp_dir, pattern = "dna-sequences\\.fasta$", full.names = TRUE, recursive = TRUE)
#fasta_file <- list.files(qiime_output_dir, pattern = "dna-sequences\\.fasta$", full.names = TRUE)[1]
if (is.na(fasta_file)) stop("No FASTA file found in ", qiime_output_dir)

# Run the 16S GCN prediction using the FASTA file
pred.GCN <- predict_16SGCN_from_sequences(seqs = fasta_file)

# Find the prediction RDS file in the temporary Colab directory
epa_file <- list.files("/content/RasperGade16S_EPA", pattern = "prediction\\.RDS$", full.names = TRUE)[1]
if (is.na(epa_file)) stop("No prediction file found in /content/RasperGade16S_EPA")

# Define the new file path: <projects>_copy_number_prediction.RDS in the qiime2_output folder
new_filepath <- file.path(qiime_output_dir, paste0(projects, "_copy_number_prediction.RDS"))

# Copy the file from the temporary location to the drive folder with the new name
file.copy(from = epa_file, to = new_filepath, overwrite = TRUE)
message("File copied and renamed to: ", new_filepath)
}
