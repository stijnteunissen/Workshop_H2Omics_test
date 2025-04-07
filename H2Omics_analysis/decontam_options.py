import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_decontam_options():
    # Dropdown for decon_method: choose between "prevalence", "frequency", and "both"
    decon_method_dropdown = widgets.Dropdown(
        options=["prevalence", "frequency", "both"],
        value="prevalence",
        description="Decon Method:"
    )
    
    # Dropdown for blank: choose between TRUE and FALSE (as raw input, here as strings)
    blank_dropdown = widgets.Dropdown(
        options=["TRUE", "FALSE"],
        value="TRUE",
        description="Blank:"
    )
    
    # Confirmation button
    confirm_button = widgets.Button(description="Confirm Options")
    output = widgets.Output()
    
    # Function executed when the confirmation button is clicked
    def on_confirm_clicked(b):
        with output:
            output.clear_output()
            # Read values from the widgets
            decon_method_value = decon_method_dropdown.value
            blank_value = blank_dropdown.value
            
            # Assign the variables to the R environment
            ro.r.assign("decon_method", decon_method_value)
            ro.r.assign("blank", blank_value)
            
            print("Options confirmed:")
            print("  decon_method:", decon_method_value)
            print("  blank:", blank_value)
            print("Variables have been assigned to the R environment.")
    
    confirm_button.on_click(on_confirm_clicked)
    
    # Display the widgets
    display(decon_method_dropdown, blank_dropdown, confirm_button, output)
