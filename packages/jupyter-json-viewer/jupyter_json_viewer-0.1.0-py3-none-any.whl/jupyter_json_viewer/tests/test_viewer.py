# jupyter_json_viewer/tests/test_viewer.py

import pytest
from jupyter_json_viewer import display_json
from IPython.display import HTML


def test_display_json_basic_types():
    """Test handling of basic JSON data types."""
    test_data = {
        "string": "test",
        "number": 42,
        "boolean": True,
        "null": None,
        "array": [1, 2, 3],
        "object": {"key": "value"}
    }
    
    # Since display_json returns None and displays via IPython.display,
    # we'll just verify it runs without errors
    assert display_json(test_data) is None


def test_display_json_empty_structures():
    """Test handling of empty objects and arrays."""
    test_data = {
        "empty_object": {},
        "empty_array": []
    }
    assert display_json(test_data) is None


def test_display_json_nested_structures():
    """Test handling of deeply nested structures."""
    test_data = {
        "level1": {
            "level2": {
                "level3": {
                    "value": "deep"
                }
            }
        }
    }
    assert display_json(test_data, max_depth=2) is None


def test_display_json_custom_settings():
    """Test customization options."""
    test_data = {"test": "value"}
    assert display_json(
        test_data,
        title="Test JSON",
        collapsed=True,
        dark_mode=True,
        indent_size=32
    ) is None


@pytest.mark.parametrize("test_input", [
    42,
    "string",
    True,
    None,
    [1, 2, 3],
    {"key": "value"}
])
def test_display_json_different_root_types(test_input):
    """Test handling of different root-level data types."""
    assert display_json(test_input) is None