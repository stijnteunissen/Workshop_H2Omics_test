import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def beta_diversity_options():
    # Create input fields for all variables
    color_factor_input = widgets.Text(
        description="Color Factor:",
        placeholder="Enter factor or NULL"
    )

    color_continuous_input = widgets.Text(
        description="Color Continuous:",
        placeholder="Enter factor or NULL"
    )

    shape_factor_input = widgets.Text(
        description="Shape Factor:",
        placeholder="Enter factor or NULL"
    )

    size_factor_input = widgets.Text(
        description="Size Factor:",
        placeholder="Enter factor or NULL"
    )

    alpha_factor_input = widgets.Text(
        description="Alpha Factor:",
        placeholder="Enter factor or NULL"
    )

    date_factor_input = widgets.Text(
        description="Date Factor:",
        placeholder="Enter factor or NULL"
    )

    # Confirmation button
    confirm_button = widgets.Button(description="Confirm Inputs")
    output = widgets.Output()

    def to_r_null_or_string(value):
        """Convert input string to None (to be interpreted as R NULL) or quoted string."""
        return None if value.strip().lower() == "null" else value.strip()

    # Function to handle confirmation
    def on_confirm_clicked(b):
        with output:
            output.clear_output()
            # Process each input
            inputs = {
                "color_factor": to_r_null_or_string(color_factor_input.value),
                "color_continuous": to_r_null_or_string(color_continuous_input.value),
                "shape_factor": to_r_null_or_string(shape_factor_input.value),
                "size_factor": to_r_null_or_string(size_factor_input.value),
                "alpha_factor": to_r_null_or_string(alpha_factor_input.value),
                "date_factor": to_r_null_or_string(date_factor_input.value),
            }

            # Assign each value to the R environment
            for var, val in inputs.items():
                ro.r.assign(var, val)

            # Display the confirmation
            print("The following values have been assigned to the R environment:")
            for var, val in inputs.items():
                print(f"  {var}: {'NULL' if val is None else val}")

    confirm_button.on_click(on_confirm_clicked)

    # Display all widgets
    display(
        color_factor_input, color_continuous_input,
        shape_factor_input, size_factor_input,
        alpha_factor_input, date_factor_input,
        confirm_button, output
    )

