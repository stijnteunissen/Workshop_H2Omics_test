import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_norm_options():
    # Dropdown for norm_method with options "fcm", "qpcr", and "NULL"
    norm_method_dropdown = widgets.Dropdown(
        options=["fcm", "qpcr", "NULL"],
        value="fcm",
        description="Norm Method:"
    )
    
    # Dropdown for copy_correction with options "TRUE" and "FALSE"
    copy_correction_dropdown = widgets.Dropdown(
        options=["TRUE", "FALSE"],
        value="TRUE",
        description="Copy Correction:"
    )
    
    # Confirmation button
    confirm_button = widgets.Button(description="Confirm Options")
    output = widgets.Output()
    
    # Function executed when the confirmation button is clicked
    def on_confirm_clicked(b):
        with output:
            output.clear_output()
            # Read values from the widgets
            norm_method_value = norm_method_dropdown.value
            copy_correction_value = copy_correction_dropdown.value
            
            # If norm_method is "NULL", assign Python's None to be interpreted as R's NULL
            norm_method_r = None if norm_method_value == "NULL" else norm_method_value
            
            # Assign the variables to the R environment
            ro.r.assign("norm_method", norm_method_r)
            ro.r.assign("copy_correction", copy_correction_value)
            
            print("Options confirmed:")
            print("  norm_method:", norm_method_value)
            print("  copy_correction:", copy_correction_value)
            print("Variables have been assigned to the R environment.")
    
    confirm_button.on_click(on_confirm_clicked)
    
    # Display the widgets
    display(norm_method_dropdown, copy_correction_dropdown, confirm_button, output)

