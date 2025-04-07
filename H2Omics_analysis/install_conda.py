import subprocess
import sys
import ipywidgets as widgets
from IPython.display import display

def install_conda():
    """
    Installs Conda and required Bioconda packages using condacolab in Google Colab.
    """
    try:
        import condacolab
        print("condacolab already installed.")
    except ImportError:
        print("Installing condacolab...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "condacolab"], check=True)
        import condacolab
        condacolab.install()
        
        # Display "Continue" button after the install
        continue_button = widgets.Button(description="Continue to Install Packages")
        display(continue_button)

        # Function to install Bioconda packages after runtime restart
        def install_bioconda_packages(b):
            print("Installing bioconda packages...")
            subprocess.run(["conda", "install", "-q", "-c", "bioconda/label/cf201901", "hmmer", "-y"], check=True)
            subprocess.run(["conda", "install", "-q", "-c", "bioconda", "easel", "-y"], check=True)
            subprocess.run(["conda", "install", "-q", "-c", "bioconda/label/cf201901", "epa-ng", "-y"], check=True)
            print("Installation completed successfully!")
        
        # Bind the button to the install function
        continue_button.on_click(install_bioconda_packages)
        return  # Stop here, wait for the user to click the button to continue.

    print("Bioconda packages already installed.")
