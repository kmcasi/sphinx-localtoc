# Local ToC – Sphinx extension

## Sphinx Local Table of Contents Extension with Object Type Annotations and Dropdowns

This Sphinx extension enhances the local Table of Contents (ToC) by adding object type annotations 
(such as methods, attributes, and classes) and providing collapsible dropdowns for each object. 
It makes it easier for users to navigate complex documentation by categorizing and visualizing object types 
in a structured, interactive way.

## Preview

<table>
  <tr>
    <td style="max-width: 40%;">
      <img
        src="https://raw.githubusercontent.com/kmcasi/sphinx-localtoc/refs/heads/main/images/DefaultFuro.jpg"
        alt="Default local ToC with Furo"
      />
    </td>
    <td style="max-width: 60%;">
      <h3>Default configurations</h3>
      <p>
        The image on the left shows the default configuration of this extension
        using the <strong><u>standard</u> Furo dark theme</strong>.
      </p>
      <p>
        Object type annotations and dropdown controls are enabled, providing
        a compact and navigable local Table of Contents for API-heavy pages.
      </p>
    </td>
  </tr>
  <tr>
    <td style="max-width: 40%;">
      <img
        src="https://raw.githubusercontent.com/kmcasi/sphinx-localtoc/refs/heads/main/images/CustomFuro.jpg"
        alt="Default local ToC with Furo"
      />
    </td>
    <td style="max-width: 60%;">
      <h3>Customized</h3>
      <p>
        The image on the left shows a customized configuration of this extension using the 
        <strong>Furo dark theme</strong>.
      </p>
      <p>The title area shown above the Table of Contents is not managed by this extension.</p>
      <p>
        All visual changes were made using <strong>CSS only</strong>, combined with the configuration option 
        <code>localtoc_dropdown_depth = 2</code> to increase the initial expansion depth.
      </p>
    </td>
  </tr>
</table>


## Features
- **Object Type Annotations**: Automatically categorizes objects in the ToC like classes, methods, attributes, etc.
- **Collapsible Dropdowns**: Adds dropdown buttons next to each object type, allowing users to collapse or expand nested items.
- **Customizable**: Offers view configuration variables and CSS classes to control which future and how they are displayed.

## Requirements
- **Python** • ***3.12+***
- **Sphinx** • ***9.1.0+***
- **beautifulsoup4** • ***4.14.3+***

## Installation
```bash
pip install sphinx-localtoc
```

## Usage

### Enable the extension
In your `conf.py`, add the extension to the `extensions` list.  
Below is an example of a typical Sphinx configuration:

```python
extensions = [
    "sphinx.ext.autodoc",           # pull in docstrings from code
    "sphinx.ext.autosummary",       # generate summary/API pages
    "sphinx.ext.napoleon",          # support Google/NumPy-style docstrings
    "sphinx.ext.intersphinx",       # link to external docs (Kivy, Python, etc.)
    "sphinx.ext.todo",              # support for exposing todo notes
    
    "sphinx_localtoc",              # stylizing the local TOC
]
```

### Configuration options
The extension provides the following configuration variables, shown here with their default values:

```python
# Enable or disable object type annotations in the local ToC.
localtoc_types = True

# Absolute or relative path (including filename) to a debug log file.
# If the file does not exist, it will be created.
# If it already exists, it will be overwritten.
localtoc_type_debug_file = ""

# Enable or disable the dropdown system in the local ToC.
localtoc_dropdown = True

# Number of initial ToC depth levels to skip before applying dropdown logic.
localtoc_dropdown_depth = 1
```

### Debug file example
The debug file feature records all detected object types during the build process.
- This feature runs only during a full ***build***, or when the `_build` directory has been removed.
- The file path is resolved relative to `conf.py`.
- If the file already exists, it will be overwritten.

```python
# Example configuration
localtoc_type_debug_file = "_static/ref/debug_ltt.txt"
```

The contents of the generated file depend on your project structure, but should look similar to the following:

```text
#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Debug Local ToC report for Sphinx extension
#//| Project: KivyDK
#//| Version: 0.1.0
#//|>-----------------------------------------------------------------------------------------------------------------<|

#//|>--------------------------------------------------------<|
#//| Used CSS classes: 6
#//|>--------------------------------------------------------<|
	• slt-dropdown        | <input> items used as checkbox for dropdown system
	• slt-dropdown-branch | Starting depth branch for <ul> items
	• slt-dropdown-depth  | Nested depth branch for <ul> items
	• slt-dropdown-icon   | <label> items used for the arrows of dropdown system
	• slt-dropdown-leaf   | Last <li> items in the depth branch
	• slt-type            | Common class for all object type items


#//|>--------------------------------------------------------<|
#//| Used object type CSS classes: 7
#//|>--------------------------------------------------------<|
	• slt-obj-attribute
	• slt-obj-class
	• slt-obj-data
	• slt-obj-exception
	• slt-obj-function
	• slt-obj-method
	• slt-obj-property


#//|>--------------------------------------------------------<|
#//| One domain used
#//|>--------------------------------------------------------<|
	• py   | Python script


#//|>--------------------------------------------------------<|
#//| Used object types: 7
#//|>--------------------------------------------------------<|
	• py   | attribute
	• py   | class
	• py   | data
	• py   | exception
	• py   | function
	• py   | method
	• py   | property
```
## License
```text
MIT License

Copyright (c) 2026 Afanase Ioan (ASI)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```