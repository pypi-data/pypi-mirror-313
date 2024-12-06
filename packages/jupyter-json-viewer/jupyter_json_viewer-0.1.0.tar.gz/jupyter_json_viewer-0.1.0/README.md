```ascii
╔══════════════════════════════════════════════════════════════╗
║ JUPYTER JSON VIEWER v1.0                                     ║
║ >_INTERACTIVE JSON VISUALIZATION SYSTEM                      ║
║ >>DOCUMENTATION INITIALIZED                                  ║
╚══════════════════════════════════════════════════════════════╝
```

>_SYSTEM OVERVIEW
---------------
An interactive JSON viewer for Jupyter Notebooks that provides clear and interactive visualization of complex data structures. The viewer supports both light and dark color schemes and offers distinct visual hierarchy for improved data comprehension.

>_CORE FEATURES
------------
[■] VISUALIZATION
    > Interactive collapsible sections for managing complex structures
    > Clear visual hierarchy with structural markers (┌├└)
    > Syntax highlighting for different data types

[■] INTERFACE
    > Light and dark mode support
    > Monospace font optimization for readability
    > Responsive hover effects

[■] CUSTOMIZATION
    > Configurable display depth
    > Adjustable indentation
    > Optional title support

>_INITIALIZATION
------------
```python
# Import the viewer
from viewer import display_json

# Sample data
data = {
    "name": "example",
    "values": [1, 2, 3],
    "options": {
        "active": True,
        "mode": "standard"
    }
}

# Basic usage
display_json(data)

# Advanced configuration
display_json(
    data,
    title="Data Structure",   # Optional title
    dark_mode=True,          # Enables dark mode
    collapsed=True,          # Starts collapsed
    max_depth=3,            # Maximum display depth
    indent_size=24          # Indentation in pixels
)
```

>_PARAMETERS
---------
AVAILABLE CONFIGURATION OPTIONS:

[DATA]      The JSON-compatible data structure to visualize (required)
[TITLE]     Optional heading above the visualization
[MAX_DEPTH] Maximum nesting depth to display (optional)
[COLLAPSED] State of collapsible elements (default: False)
[INDENT]    Indentation size in pixels (default: 24)
[DARK_MODE] Dark color scheme (default: False)

>_PROJECT STRUCTURE
---------------
```ascii
ROOT
├── viewer.py     // Main module containing display_json function
```

>_TECHNICAL SPECIFICATIONS
---------------------
SYSTEM REQUIREMENTS:
- Python 3.6 or higher
- IPython 7.0.0 or higher
- Jupyter Notebook/Lab

IMPLEMENTED TECHNOLOGIES:
- HTML5 for structural representation
- CSS3 for styling and animations
- JavaScript for interactivity
- IPython display system integration

>_COLOR SCHEMES
-----------
LIGHT MODE:
- Background: #f8f9fa
- Text: #2c3e50
- Strings: #28a745
- Numbers: #0066cc
- Boolean values: #e83e8c

DARK MODE:
- Background: #1e1e1e
- Text: #d4d4d4
- Strings: #6A9955
- Numbers: #569CD6
- Boolean values: #C586C0

>_LICENSE
------
```ascii
╔════════════════════════════════════════════════╗
║ GNU General Public License v3.0                ║
║ Copyright (c) 2024                             ║
║ Developed by Johannes Kaindl                   ║
╚════════════════════════════════════════════════╝
```

>>END OF DOCUMENTATION