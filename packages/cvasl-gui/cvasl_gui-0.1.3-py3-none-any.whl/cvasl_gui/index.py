import os
import webbrowser
from threading import Timer
from dotenv import load_dotenv

from dash import html, dcc, Input, Output

from cvasl_gui import data_store
from cvasl_gui.app import app
from cvasl_gui.tab_data_inspection import create_tab_data_inspection
from cvasl_gui.tab_input_selection import create_tab_input_selection
from cvasl_gui.tab_compare import create_tab_compare

data_store.all_data = None
data_store.selected_directory = None

app.layout = html.Div(
    id='root',
    children=[html.Div([
        dcc.Tabs(
            id='tabs',
            value='1',
            children=[
                dcc.Tab(label='Select input', value='1'),
                dcc.Tab(label='Inspect', value='2'),
                dcc.Tab(label='Compare', value='3'),
                dcc.Tab(label='Harmonize', value='4'),
                dcc.Tab(label='Estimate', value='5'),
            ],
            vertical=False
        ),
        # Load all tab contents here but control visibility through a callback
        html.Div(
            [
                html.Div(create_tab_input_selection(), id='tab-1-content', style={'display': 'block'}),
                html.Div(create_tab_data_inspection(), id='tab-2-content', style={'display': 'none'}),
                html.Div(create_tab_compare(), id='tab-3-content', style={'display': 'none'}),
                html.Div("asdf", id='tab-4-content', style={'display': 'none'}),
                html.Div("Estimate content goes here", id='tab-5-content', style={'display': 'none'}),
            ],
            id='tab-content-container'
        )
    ], id='main-container')])


# Callback to toggle visibility based on selected tab
@app.callback(
    [Output(f'tab-{i}-content', 'style') for i in range(1, 6)],
    [Input('tabs', 'value')]
)
def display_content(selected_tab):
    # Set 'display' to 'block' for the selected tab and 'none' for others
    return [{'display': 'block' if selected_tab == str(i) else 'none'} for i in range(1, 6)]


def main():
    # Load environment variables
    load_dotenv()
    port = os.getenv('CVASL_PORT', 8767)
    debug_mode = os.getenv('CVASL_DEBUG_MODE', False)

    # Schedule a timer to open the browser
    if not debug_mode: # we don't want to relaunch on every change
        url = f"http://127.0.0.1:{port}/"
        Timer(1, lambda: webbrowser.open(url)).start()

    # Start the Dash server
    app.run_server(port=port, debug=debug_mode)


if __name__ == '__main__':
    main()
