# CVASL-GUI

This is a GUI for the cvasl package, currently a work-in-progress.


## Install and run

```bash
pip install cvasl-gui
cvasl-gui
```

## Configuration

The application will look for the following environment variables:

```bash
CVASL_DEBUG_MODE  # True for development, False for production. Debug mode will show the Dash debug console on the page. In production mode, the browser will be automatically opened.
CVASL_PORT        # The port the server runs on, default is 8767
```

## Development

```bash
poetry install
poetry run cvasl-gui
```
