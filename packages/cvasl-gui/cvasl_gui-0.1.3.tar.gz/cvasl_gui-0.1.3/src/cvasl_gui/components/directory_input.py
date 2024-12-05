import os
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from cvasl_gui.app import app
from cvasl_gui import data_store


def create_directory_input():
    return html.Div([
        html.Div([
            html.Label("Directory path"),
            dcc.Input(
                id='directory-path-input',
                type='text',
                placeholder="Enter directory path",
                style={'width': '60%'},
                className="input input-bordered w-full max-w-xs"
            ),
            html.Button('Scan Directory', id='scan-button', className='button button-primary', n_clicks=0),
        ]),
        html.Div(id='file-list-container', children=[dcc.RadioItems(
            id='file-list',
            options=[],
            labelStyle={'display': 'block'},
            style={'overflowY': 'scroll', 'height': '200px'}  # Make it scrollable
        )]),  # Display files in directory
        html.Div([html.Button('Load Selected File', id='load-button', className='button button-primary', n_clicks=0)]),
        html.Div(id='file-contents-container')  # Display contents of file
    ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '10px'})


@app.callback(
    Output('file-list', 'options'),
    Input('scan-button', 'n_clicks'),
    State('directory-path-input', 'value')
)
def scan_directory(n_clicks, directory_path):
    if not n_clicks or not directory_path:
        raise PreventUpdate

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        return html.Div(["Directory not found. Please enter a valid path."], style={'color': 'red'})

    # List files in the directory
    files = os.listdir(directory_path)

    return [{'label': file, 'value': file} for file in files]


@app.callback(
    Output('file-contents-container', 'children'),
    Input('load-button', 'n_clicks'),
    State('directory-path-input', 'value'),
    State('file-list', 'value')
)
def load_file(n_clicks, directory_path, selected_file):
    if n_clicks == 0 or not selected_file:
        raise PreventUpdate

    # Load the file
    file_path = os.path.join(directory_path, selected_file)
    try:
        data_store.all_data = pd.read_csv(file_path)
    except Exception as e:
        return html.Div([f"Error loading file: {e}"], style={'color': 'red'})

    return html.Div([
        html.Span(f"Loaded {selected_file}")
    ])
