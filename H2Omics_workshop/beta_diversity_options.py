import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_beta_diversity_options():
    # Retrieve norm_method from the R environment and convert to lowercase
    norm_method = str(ro.r("norm_method")[0]).lower()
    
    # Define factor options based on the norm_method
    if norm_method == "fcm":
        factor_options = ["treatment", "timepoint"]
    elif norm_method == "qpcr":
        factor_options = ["sample_type", "regrowth_day"]
    else:
        factor_options = []

    # Create dropdowns for selecting factors
    color_factor_dropdown = widgets.Dropdown(
        options=["None"] + factor_options,
        value="None",
        description="Color Factor:"
    )
    
    shape_factor_dropdown = widgets.Dropdown(
        options=["None"] + factor_options,
        value="None",
        description="Shape Factor:"
    )

    taxrank_dropdown = widgets.Dropdown(
        options=["Phylum", "Class", "Order", "Family", "Genus", "ASV"],
        value="Genus",
        description="Taxrank:"
    )
    
    # Keep track of selected values for color and shape
    selected_values = {
        'color_factor': 'None',
        'shape_factor': 'None'
    }

    # Function to update the dropdowns, ensuring that the same option is not selected for both
    def update_dropdowns(change):
        # Update the selected values for color and shape factors
        selected_values['color_factor'] = color_factor_dropdown.value
        selected_values['shape_factor'] = shape_factor_dropdown.value

    # Attach the update function to both dropdowns
    color_factor_dropdown.observe(update_dropdowns, names='value')
    shape_factor_dropdown.observe(update_dropdowns, names='value')
    
    # Create a confirmation button
    confirm_button = widgets.Button(description="Confirm Factors")
    
    # When the confirm button is clicked, assign the selected factors to R
    def confirm_factors(b):
        # Check if color_factor and shape_factor are the same
        if selected_values['color_factor'] == selected_values['shape_factor']:
            print("Error: Color Factor and Shape Factor cannot be the same.")
            return  # Stop further execution if factors are the same
        
        # If 'None' is selected, assign None (interpreted as R NULL) 
        color_factor_value = selected_values['color_factor'] if selected_values['color_factor'] != 'None' else None
        shape_factor_value = selected_values['shape_factor'] if selected_values['shape_factor'] != 'None' else None
        
        # Assign selected factors to R (None will be interpreted as R's NULL)
        ro.r.assign("taxrank_beta_div", taxrank_dropdown.value)
        ro.r.assign("color_factor", color_factor_value)
        ro.r.assign("shape_factor", shape_factor_value)
        
        # Show confirmation message
        print(f"Factors confirmed: Color Factor - {color_factor_value}, Shape Factor - {shape_factor_value}")
        print("Factors have been successfully assigned to R.")
    
    # Correctly attach the confirm_factors function to the confirmation button
    confirm_button.on_click(confirm_factors)
    
    # Display the dropdowns and the confirmation button
    display(taxrank_dropdown, color_factor_dropdown, shape_factor_dropdown, confirm_button)

# To display the widget, call the function:
select_beta_diversity_options()
