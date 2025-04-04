import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_copy_correction():
    # Create a dropdown for copy_correction
    copy_dropdown = widgets.Dropdown(
        options=[("TRUE", "TRUE"), ("FALSE", "FALSE")],  # Keep values as strings for R
        value="TRUE",
        description="Copy Correction:",
    )

    # Create a confirmation button
    confirm_button_copy = widgets.Button(
        description="Confirm Copy Correction"
    )

    def confirm_copy_correction(b):
        # Assign the selected value to R
        ro.r(f'copy_correction <- {copy_dropdown.value}')
        print("Copy number correction assigned to R:", copy_dropdown.value)

    confirm_button_copy.on_click(confirm_copy_correction)

    # Display the dropdown and button
    display(copy_dropdown, confirm_button_copy)
