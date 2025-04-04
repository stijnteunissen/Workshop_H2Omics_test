# norm_method.py

import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_norm_method():
    # Create a dropdown for norm_method
    norm_dropdown = widgets.Dropdown(
        options=[("fcm", "fcm"), ("qpcr", "qpcr")],
        value="fcm",
        description="Norm Method:",
    )

    # Create a confirm button for norm_method
    confirm_button_norm = widgets.Button(
        description="Confirm Norm Method"
    )

    def confirm_norm_method(b):
        # Assign the selected norm_method value to R
        ro.r.assign("norm_method", norm_dropdown.value)
        print("Normalization method assigned to R:", norm_dropdown.value)

    confirm_button_norm.on_click(confirm_norm_method)

    # Display the norm_method dropdown and confirm button
    display(norm_dropdown, confirm_button_norm)
