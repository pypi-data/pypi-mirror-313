import inspect
from functools import wraps
from typing import Callable, Dict, Set

import streamlit as st


class StreamlitWrapper:
    """
    A wrapper around Streamlit components that handles automatic key generation
    and consistent styling.
    """

    # Components that support key attribute
    SUPPORTED_COMPONENTS: Set[str] = {
        # Components with custom styling
        "button", "download_button", "text_area", "text_input",
        "file_uploader", "container", "checkbox",

        # Standard components
        "dataframe", "data_editor", "altair_chart", "plotly_chart",
        "pydeck_chart", "vega_lite_chart", "color_picker", "feedback",
        "multiselect", "pills", "radio", "segmented_control", "selectbox",
        "select_slider", "toggle", "number_input", "slider", "date_input",
        "time_input", "chat_input", "audio_input", "camera_input",
        "form", "chat_input",
    }

    def __init__(self, prefix: str = "ai3"):
        """Initialize wrapper with custom prefix for component keys."""
        self.prefix = prefix
        self.component_counts: Dict[str, int] = {}
        self._wrap_components()

    def _generate_key(self, component_name: str, *args, **kwargs) -> str:
        """Generate a stable key for a component based on its properties."""
        label = args[0] if args else ""
        key_parts = [self.prefix, component_name, str(label)]

        # Add important kwargs to key
        for kwarg in ['placeholder', 'type']:
            if kwarg in kwargs:
                key_parts.append(f"{kwarg}-{kwargs[kwarg]}")

        base_key = "-".join(key_parts)

        # Handle duplicate components
        if base_key in self.component_counts:
            self.component_counts[base_key] += 1
            base_key = f"{base_key}-{self.component_counts[base_key]}"
        else:
            self.component_counts[base_key] = 0

        return base_key

    def _wrap_component(self, func: Callable, name: str) -> Callable:
        """Wrap a single Streamlit component with key generation."""
        if not callable(func) or name not in self.SUPPORTED_COMPONENTS:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'key' not in kwargs:
                kwargs['key'] = self._generate_key(name, *args, **kwargs)

            # Set primary type for buttons
            if name in ['button', 'download_button'] and 'type' not in kwargs:
                kwargs['type'] = "primary"

            return func(*args, **kwargs)
        return wrapper

    def _wrap_components(self):
        """Wrap all supported Streamlit components."""
        for name, attr in inspect.getmembers(st):
            if not name.startswith('_'):
                wrapped = self._wrap_component(attr, name)
                setattr(self, name, wrapped)
