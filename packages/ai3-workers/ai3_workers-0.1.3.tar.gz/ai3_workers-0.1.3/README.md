# AI3 Workers

A Python package that provides utilities and standard configurations for creating Streamlit workers in the AIAIAI ecosystem.

## Features

- 🎨 Automatic styling and configuration
- 🌐 Built-in internationalization (i18n) support
- 🔑 Consistent component key management
- 📏 Automatic height adjustment
- 🔄 Worker rendering status tracking

## Installation

Install using Poetry:

```bash
poetry add ai3-workers
```

Or with pip:

```bash
pip install ai3-workers
```

## Quick Start

Create a new worker with minimal boilerplate:

```python
from ai3_workers.core.config import create_worker

# Initialize the worker - must be first line after imports
st = create_worker()

def main():
    name = st.text_input("Enter your name")
    if st.button("Submit"):
        st.write(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

## Project Structure

Recommended project structure for a worker:

```
my-worker/
├── src/
│   ├── i18n.json          # Translations file
│   ├── interface.py       # Main worker file
│   └── modules/           # Worker-specific modules
├── pyproject.toml
└── poetry.lock
```

## Internationalization

Add translations in `src/i18n.json`:

```json
{
  "title": {
    "en": "My Worker",
    "es": "Mi Worker",
    "nl": "Mijn Worker"
  },
  "description": {
    "en": "A simple worker example",
    "es": "Un ejemplo simple de worker",
    "nl": "Een eenvoudig worker voorbeeld"
  }
}
```

The package will automatically load translations and use them for the worker title and description. You can also customize these directly:

```python
st = create_worker(
    title="Custom Title",
    description="Custom description"
)
```

## StreamlitWrapper

The package provides a wrapped version of Streamlit that automatically:

- Generates consistent component keys
- Applies standard styling
- Sets default values for common properties

Supported components include:

- Button components (primary style by default)
- Input components
- Form components
- Data display components
- Media components

## Development Setup

1. Clone the repository:

```bash
git clone git@hub.nucleoo.com:aiaiai/ai3-workers.git
```

2. Install dependencies:

```bash
poetry install
```

## Running a Worker

From your worker directory:

```bash
poetry run streamlit run src/interface.py
```
