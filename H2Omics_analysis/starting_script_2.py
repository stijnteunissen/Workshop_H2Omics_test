import ipywidgets as widgets
from IPython.display import display, clear_output
import rpy2.robjects as ro
from rpy2.robjects import StrVector, BoolVector

def analysis_options():
    # container for multiple present_variable_factors
    factor_container = widgets.VBox()
    add_factor_button = widgets.Button(description="Add factor")
    continue_button   = widgets.Button(description="Continue")

    # add a text input for each factor
    def _add_factor(b):
        factor_container.children += (
            widgets.Text(
                description="Factor:",
                placeholder="Enter factor"
            ),
        )
    add_factor_button.on_click(_add_factor)

    # show the factor inputs and buttons
    display(widgets.HTML("<b>Enter your present_variable_factors:</b>"))
    display(factor_container, widgets.HBox([add_factor_button, continue_button]))

    def _on_continue(b):
        # lock the factor inputs
        add_factor_button.disabled = True
        continue_button.disabled = True

        # collect non‐empty factors
        factors = [w.value for w in factor_container.children if w.value.strip()]

        # normalization method dropdown
        norm_dropdown = widgets.Dropdown(
            options=["qpcr", "fcm", "NULL"],
            description="Norm method:"
        )

        # blank / mock checkboxes
        blank_dropdown = widgets.Dropdown(
            options=["TRUE", "FALSE"],
            description="Blank:")
        mock_dropdown = widgets.Dropdown(
            options=["TRUE", "FALSE"],
            description="Mock:")

        # sample matrix dropdown
        sample_dropdown = widgets.Dropdown(
            options=["liquid", "solid"],
            description="Sample matrix:"
        )

        # aesthetic mapping dropdowns from factors or NULL
        aesthetic_opts = ["NULL"] + factors
        color_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Color factor:"
        )
        shape_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Shape factor:"
        )
        size_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Size factor:"
        )
        alpha_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Alpha factor:"
        )

        # final confirmation button and output area
        confirm_button = widgets.Button(description="Assign to R")
        output = widgets.Output()

        # helper to convert NULL→None, else string
        def _to_r_val(v, raw_alt=None):
            val = v.strip()
            if val.lower() == "null":
                return None if raw_alt is None else raw_alt
            return val

        def _on_confirm(c):
            with output:
                clear_output()
                # assign the vector of factors
                ro.r.assign("present_variable_factors", StrVector(factors))

                # assign norm_method, use "raw" if NULL
                nm = norm_dropdown.value
                ro.r.assign("norm_method", nm if nm != "NULL" else "raw")

                # assign blank and mock as logicals
                blank_val = (blank_dropdown.value == "TRUE")
                mock_val  = (mock_dropdown.value  == "TRUE")

                ro.r.assign("blank", BoolVector([blank_val]))
                ro.r.assign("mock",  BoolVector([mock_val]))

                # assign sample matrix
                ro.r.assign("sample_matrix", sample_dropdown.value)

                # assign aesthetics or NULL
                for name, widget in [
                    ("color_factor",  color_dropdown),
                    ("shape_factor",  shape_dropdown),
                    ("size_factor",   size_dropdown),
                    ("alpha_factor",  alpha_dropdown),
                ]:
                    if widget.value == "NULL":
                        ro.r(f"{name} <- NULL")
                    else:
                        ro.r.assign(name, widget.value)

                print("Parameters have been assigned to the R environment.")

        confirm_button.on_click(_on_confirm)

        # display all remaining controls
        display(
            norm_dropdown,
            blank_dropdown,
            mock_dropdown,
            sample_dropdown,
            color_dropdown,
            shape_dropdown,
            size_dropdown,
            alpha_dropdown,
            confirm_button,
            output
        )

    continue_button.on_click(_on_continue)
