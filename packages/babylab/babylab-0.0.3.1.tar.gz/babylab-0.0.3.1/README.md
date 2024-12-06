# babylab-redcap

A GUI for the SJD Babylab REDCap database.

## Installation

You will need Python, ideally Python [3.12.7](https://www.python.org/downloads/release/python-3127/). If you are using Windows, you can install Python from the [App store](https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=en-us&gl=US) or using the terminal via the `winget` command:

```bash
winget install -e --id Python.Python.3.12
```

Once Python is installed, [open your terminal](https://www.youtube.com/watch?v=8Iyldhkrh7E) and run these commands:

```bash
python -m pip install flask babylab
flask --app babylab.main run
```

Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). Log in with your API authentication token, and you should be ready to go!