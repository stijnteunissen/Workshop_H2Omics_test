import ipywidgets as widgets
from IPython.display import display, clear_output
import rpy2.robjects as ro
from rpy2.robjects import StrVector, BoolVector

# Container for entering multiple present_variable_factors
present_var_container = widgets.VBox()
add_button = widgets.Button(description="Add factor")
continue_button = widgets.Button(description="Continue")

# When “Add factor” is clicked, append a new Text widget
def add_factor(_):
    new_field = widgets.Text(placeholder="Enter factor")
    present_var_container.children += (new_field,)

add_button.on_click(add_factor)

# Display UI for factors
display(widgets.HTML("<b>Enter your present_variable_factors:</b>"))
display(present_var_container, widgets.HBox([add_button, continue_button]))

# After clicking “Continue”, lock factor entry and show the rest
def on_continue(_):
    add_button.disabled = True
    continue_button.disabled = True
    
    # Gather non-empty factors
    factors = [f.value for f in present_var_container.children if f.value.strip()]
    
    # Dropdown for normalization method
    norm_dropdown = widgets.Dropdown(
        options=["qpcr", "fcm", "NULL"],
        description="Norm method:"
    )
    # Checkboxes for blank and mock samples
    blank_checkbox = widgets.Checkbox(description="Blank = TRUE", value=True)
    mock_checkbox  = widgets.Checkbox(description="Mock = TRUE", value=False)
    
    # Dropdown for sample matrix type
    sample_dropdown = widgets.Dropdown(
        options=["liquid", "solid"],
        description="Sample matrix:"
    )
    
    # Dropdowns for aesthetic mappings (choose one factor or NULL)
    aesthetic_options = ["NULL"] + factors
    color_dropdown = widgets.Dropdown(options=aesthetic_options, description="Color factor:")
    shape_dropdown = widgets.Dropdown(options=aesthetic_options, description="Shape factor:")
    size_dropdown  = widgets.Dropdown(options=aesthetic_options, description="Size factor:")
    alpha_dropdown = widgets.Dropdown(options=aesthetic_options, description="Alpha factor:")
    
    run_button = widgets.Button(description="Run R")
    output_area = widgets.Output()
    
    # Show the remaining controls
    display(widgets.HTML("<hr><b>Choose additional parameters:</b>"))
    display(norm_dropdown, blank_checkbox, mock_checkbox,
            sample_dropdown, color_dropdown, shape_dropdown,
            size_dropdown, alpha_dropdown, run_button, output_area)
    
    # When “Run R” is clicked, assign each variable into R
    def run_r(_):
        with output_area:
            clear_output()
            
            # Assign the vector of factors
            ro.r.assign("present_variable_factors", StrVector(factors))
            
            # Handle norm_method: convert NULL→"raw"
            nm = norm_dropdown.value
            ro.r.assign("norm_method", StrVector([nm if nm!="NULL" else "raw"]))
            
            # Assign blank & mock as logical scalars
            ro.r.assign("blank", BoolVector([blank_checkbox.value]))
            ro.r.assign("mock",  BoolVector([mock_checkbox.value]))
            
            # Assign sample matrix
            ro.r.assign("sample_matrix", StrVector([sample_dropdown.value]))
            
            # Helper to assign aesthetics or set to NULL
            def assign_aesthetic(name, widget):
                if widget.value == "NULL":
                    ro.r(f"{name} <- NULL")
                else:
                    ro.r.assign(name, StrVector([widget.value]))
            
            assign_aesthetic("color_factor",  color_dropdown)
            assign_aesthetic("shape_factor",  shape_dropdown)
            assign_aesthetic("size_factor",   size_dropdown)
            assign_aesthetic("alpha_factor",  alpha_dropdown)
            
            print("✅ All parameters have been assigned individually in R.")
            # Optional: show one of them in output
            print("present_variable_factors in R:", ro.r.get("present_variable_factors"))
    
    run_button.on_click(run_r)

continue_button.on_click(on_continue)
