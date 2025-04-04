import ipywidgets as widgets
from IPython.display import display
import rpy2.robjects as ro

def select_taxrank_alpha_div():
    # Define the available taxonomic ranks
    taxrank_options = ["Phylum", "Class", "Order", "Family", "Genus", "ASV"]
    
    # Create a dropdown for taxrank selection
    taxrank_dropdown = widgets.Dropdown(
        options=taxrank_options,
        value=taxrank_options[0],
        description="Taxrank:"
    )
    
    # Create a confirmation button
    confirm_button = widgets.Button(description="Confirm Taxrank")
    
    # When the confirm button is clicked, assign the selected taxrank to R
    def confirm_taxrank(b):
        ro.r.assign("taxrank_alpha_div", taxrank_dropdown.value)
        print("Taxrank assigned to R:", taxrank_dropdown.value)
    
    confirm_button.on_click(confirm_taxrank)
    
    # Display the dropdown and the confirmation button
    display(taxrank_dropdown, confirm_button)
