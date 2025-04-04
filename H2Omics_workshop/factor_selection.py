import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def factor_selection():
    # Retrieve norm_method from the R environment and convert to lowercase
    norm_method = str(ro.r("norm_method")[0]).lower()
    
    # Set dropdown options based on norm_method
    if norm_method == "fcm":
        options = ["treatment, timepoint", "timepoint, treatment", "timepoint", "treatment"]
    elif norm_method == "qpcr":
        options = ["sample_type, regrowth_day", "regrowth_day, sample_type", "sample_type", "regrowth_day"]
    else:
        options = []
        print("Unrecognized norm_method:", norm_method)
    
    # Create a dropdown for factor selection
    factors_dropdown = widgets.Dropdown(
        options=options,
        value=options[0] if options else None,
        description="Factors:"
    )
    
    # Create a confirmation button
    confirm_button_factors = widgets.Button(
        description="Confirm Factors"
    )
    
    # Function to handle button click: pass selected factors to R in the correct format
    def confirm_factors(b):
        selected_value = factors_dropdown.value  # Get the selected value
        factor_list = selected_value.split(", ")  # Split into a list
        
        # Convert the Python list to an R vector and assign it to the R environment
        ro.r.assign("present_variable_factors", ro.StrVector(factor_list))
        
        print("Present variable factors assigned to R:", factor_list)
    
    confirm_button_factors.on_click(confirm_factors)
    
    # Display the dropdown and the button
    display(factors_dropdown, confirm_button_factors)

