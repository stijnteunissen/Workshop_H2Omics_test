import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_sample_matrix():
    # Dropdown for sample_matrix: choose between "liquid" and "solid"
    sample_matrix_dropdown = widgets.Dropdown(
        options=["liquid", "solid"],
        value="liquid",
        description="Sample Matrix:"
    )
    
    # Confirmation button
    confirm_button = widgets.Button(description="Confirm Option")
    output = widgets.Output()
    
    # Function executed when the confirmation button is clicked
    def on_confirm_clicked(b):
        with output:
            output.clear_output()
            # Read the value from the widget
            sample_matrix_value = sample_matrix_dropdown.value
            
            # Assign the variable to the R environment
            ro.r.assign("sample_matrix", sample_matrix_value)
            
            print("Option confirmed:")
            print("  sample_matrix:", sample_matrix_value)
            print("Variable has been assigned to the R environment.")
    
    confirm_button.on_click(on_confirm_clicked)
    
    # Display the widget
    display(sample_matrix_dropdown, confirm_button, output)
