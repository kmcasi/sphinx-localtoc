#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 01 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from importlib.resources import files

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from .localtoc_type import setup_type
from .localtoc_dropdown import setup_dropdown


#// GLOBAL VARIABLES
__version__ = "26.2.8"


#// RUN
def setup(app: Sphinx) -> ExtensionMetadata:
    root = files(__name__)
    app.config.html_static_path.append(str(root / "_static"))

    app.add_css_file("styles/localtoc.css")

    setup_type(app)
    setup_dropdown(app)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
