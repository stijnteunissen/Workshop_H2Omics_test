import subprocess

def install_conda():
    # Install required Bioconda packages
    subprocess.run(["conda", "install", "-q", "-c", "bioconda/label/cf201901", "hmmer", "-y"], check=True)
    subprocess.run(["conda", "install", "-q", "-c", "bioconda", "easel", "-y"], check=True)
    subprocess.run(["conda", "install", "-q", "-c", "bioconda/label/cf201901", "epa-ng", "-y"], check=True)

    print("Installation completed successfully!")
