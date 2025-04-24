starting_script.py

import ipywidgets as widgets
from IPython.display import display, clear_output
from rpy2.robjects import r

# 1) Container to hold dynamically added present_variable_factors
present_var_container = widgets.VBox([])
add_button = widgets.Button(description="Add factor", button_style="info")
continue_button = widgets.Button(description="Continue", button_style="success")

def add_factor(b):
    """Add a new text widget for entering a factor."""
    txt = widgets.Text(description="Factor:")
    present_var_container.children += (txt,)

add_button.on_click(add_factor)

# Show initial UI for adding present_variable_factors
display(widgets.HTML("<b>1. Enter your present_variable_factors:</b>"))
display(present_var_container)
display(widgets.HBox([add_button, continue_button]))

def on_continue(b):
    """After clicking Continue: disable adding more factors and show the rest of the form."""
    add_button.disabled = True
    continue_button.disabled = True
    
    # Collect entered present_variable_factors
    present_vars = [w.value for w in present_var_container.children if w.value.strip()]
    
    # 2) Norm method dropdown
    norm_dropdown = widgets.Dropdown(
        options=["qpcr", "fcm", "NULL"],
        description="Norm method:"
    )
    
    # 3) Blank and Mock checkboxes
    blank_checkbox = widgets.Checkbox(description="Blank = TRUE", value=True)
    mock_checkbox  = widgets.Checkbox(description="Mock = TRUE", value=False)
    
    # 4) Sample matrix dropdown
    sample_dropdown = widgets.Dropdown(
        options=["liquid", "solid"],
        description="Sample matrix:"
    )
    
    # 5) Aesthetic mapping dropdowns (select from present_vars or NULL)
    aesth_opts = ["NULL"] + present_vars
    color_dropdown = widgets.Dropdown(options=aesth_opts, description="Color factor:")
    shape_dropdown = widgets.Dropdown(options=aesth_opts, description="Shape factor:")
    size_dropdown  = widgets.Dropdown(options=aesth_opts, description="Size factor:")
    alpha_dropdown = widgets.Dropdown(options=aesth_opts, description="Alpha factor:")
    
    run_button = widgets.Button(description="Run R", button_style="primary")
    out = widgets.Output()
    
    # Display the rest of the form
    display(widgets.HTML("<hr><b>2. Choose additional parameters:</b>"))
    display(norm_dropdown, blank_checkbox, mock_checkbox,
            sample_dropdown, color_dropdown, shape_dropdown,
            size_dropdown, alpha_dropdown, run_button, out)
    
    def run_r(c):
        """Build the R list and pass it into R."""
        def r_bool(val): return "TRUE" if val else "FALSE"
        
        pv_str = "c(" + ",".join(f'"{v}"' for v in present_vars) + ")"
        nm_val = norm_dropdown.value
        nm_str = f'"{nm_val}"' if nm_val != "NULL" else '"raw"'
        blank_str = r_bool(blank_checkbox.value)
        mock_str  = r_bool(mock_checkbox.value)
        sm_str    = f'"{sample_dropdown.value}"'
        
        def str_or_null(dd):
            return f'"{dd.value}"' if dd.value != "NULL" else "NULL"
        
        cf_str    = str_or_null(color_dropdown)
        shape_str = str_or_null(shape_dropdown)
        size_str  = str_or_null(size_dropdown)
        alpha_str = str_or_null(alpha_dropdown)
        
        # Construct the R list
        r_list = (
            f"list("
            f"present_variable_factors={pv_str}, "
            f"norm_method={nm_str}, "
            f"blank={blank_str}, "
            f"mock={mock_str}, "
            f"sample_matrix={sm_str}, "
            f"color_factor={cf_str}, "
            f"shape_factor={shape_str}, "
            f"size_factor={size_str}, "
            f"alpha_factor={alpha_str}"
            f")"
        )
        r_code = f"params <- {r_list}"
        
        with out:
            clear_output()
            print("=== Executed R code ===")
            print(r_code)
            r(r_code)
            print("\n✅ Parameters have been passed to R as 'params'")
    
    run_button.on_click(run_r)

continue_button.on_click(on_continue)
