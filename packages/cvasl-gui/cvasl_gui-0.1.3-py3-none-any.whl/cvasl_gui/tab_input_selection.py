from dash import html
from cvasl_gui.components.directory_input import create_directory_input

def create_tab_input_selection():
    return html.Div([
        create_directory_input(),
    ])
