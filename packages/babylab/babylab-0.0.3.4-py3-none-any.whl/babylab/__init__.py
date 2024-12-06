"""Initialise app
"""

from flask import Flask

app = Flask(__name__)

import babylab.main  # pylint: disable=import-error,unknown-option-value,wrong-import-position
