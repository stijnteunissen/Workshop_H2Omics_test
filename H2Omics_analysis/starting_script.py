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
                placeholder="Enter factor",
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='max-content')
            ),
        )
    add_factor_button.on_click(_add_factor)

    # show the factor inputs and buttons
    display(widgets.HTML("<b>Enter your present variable factors:</b>"))
    display(factor_container, widgets.HBox([add_factor_button, continue_button]))

    def _on_continue(b):
        # lock the factor inputs
        add_factor_button.disabled = True
        continue_button.disabled = True

        # collect non-empty factors
        factors = [w.value for w in factor_container.children if w.value.strip()]

        # one shared layout & style for all dropdowns
        dropdown_layout = widgets.Layout(width='max-content')
        label_style = {'description_width': 'initial'}

        # normalization method dropdown
        norm_dropdown = widgets.Dropdown(
            options=["qpcr", "fcm", "NULL"],
            description="Norm method:",
            layout=dropdown_layout,
            style=label_style
        )

        # blank / mock dropdowns
        blank_dropdown = widgets.Dropdown(
            options=["TRUE", "FALSE"],
            description="Blank:",
            layout=dropdown_layout,
            style=label_style
        )
        mock_dropdown = widgets.Dropdown(
            options=["TRUE", "FALSE"],
            description="Mock:",
            layout=dropdown_layout,
            style=label_style
        )

        # sample matrix dropdown
        sample_dropdown = widgets.Dropdown(
            options=["liquid", "solid"],
            description="Sample matrix:",
            layout=dropdown_layout,
            style=label_style
        )

        # aesthetic mapping dropdowns
        aesthetic_opts = ["NULL"] + factors
        color_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Color factor:",
            layout=dropdown_layout,
            style=label_style
        )
        shape_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Shape factor:",
            layout=dropdown_layout,
            style=label_style
        )
        size_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Size factor:",
            layout=dropdown_layout,
            style=label_style
        )
        alpha_dropdown = widgets.Dropdown(
            options=aesthetic_opts,
            description="Alpha factor:",
            layout=dropdown_layout,
            style=label_style
        )

        # stack all controls vertically with equal 10px gap
        controls_box = widgets.Box(
            [
                norm_dropdown,
                blank_dropdown,
                mock_dropdown,
                sample_dropdown,
                color_dropdown,
                shape_dropdown,
                size_dropdown,
                alpha_dropdown
            ],
            layout=widgets.Layout(
                display='flex',
                flex_flow='column',
                align_items='flex-start',
                gap='10px'
            )
        )

        # final confirmation button and output area
        confirm_button = widgets.Button(description="Assign to R")
        output = widgets.Output()

        def _on_confirm(c):
            with output:
                clear_output()
                # assign the vector of factors
                ro.r.assign("present_variable_factors", StrVector(factors))
                # assign norm_method, use "raw" if NULL
                nm = norm_dropdown.value
                ro.r.assign("norm_method", nm if nm != "NULL" else "raw")
                # assign blank and mock as logicals
                ro.r.assign("blank", BoolVector([blank_dropdown.value == "TRUE"]))
                ro.r.assign("mock",  BoolVector([mock_dropdown.value  == "TRUE"]))
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

        # display everything
        display(controls_box, confirm_button, output)

    continue_button.on_click(_on_continue)
