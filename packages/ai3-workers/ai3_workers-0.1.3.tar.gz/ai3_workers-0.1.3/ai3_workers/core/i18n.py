import json
from pathlib import Path
import streamlit as st
from typing import Dict, Optional, Set


def find_i18n_file() -> Optional[Path]:
    """
    Find the i18n.json file by looking in:
    1. Current working directory
    2. src/ subdirectory
    3. Parent directory's src/ subdirectory
    """
    possible_locations = [
        Path.cwd() / "i18n.json",
        Path.cwd() / "src" / "i18n.json",
        Path.cwd().parent / "src" / "i18n.json"
    ]

    for location in possible_locations:
        if location.exists():
            return location

    return None


def load_i18n() -> Dict[str, Dict[str, str]]:
    """Load localization strings from i18n.json."""
    i18n_path = find_i18n_file()

    if i18n_path is None:
        return {}

    try:
        with open(i18n_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


# Cache the loaded strings
_STRINGS: Dict[str, Dict[str, str]] = load_i18n()


def get_available_languages() -> Set[str]:
    """Get all available language codes from localization file."""
    languages = set()
    for translations in _STRINGS.values():
        languages.update(translations.keys())
    return languages


def get_localized_string(key: str, default: Optional[str] = None) -> str:
    """Get localized string for given key."""
    translations = _STRINGS.get(key, {})

    # Default to English
    if "en" in translations:
        return translations["en"]

    # Use default or key itself
    return default if default is not None else key


def get_current_language() -> str:
    """
    Get the current language code from URL parameters.
    Validates the language code against available translations.
    Returns 'en' if no language is specified or if the specified language is not available.
    """
    requested_lang = st.query_params.get("lang", "en")
    available_languages = get_available_languages()

    if requested_lang not in available_languages:
        # If the requested language isn't available, fallback to English
        return "en"

    return requested_lang
