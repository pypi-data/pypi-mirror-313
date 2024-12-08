import json
from pathlib import Path

config_dir = Path.home() / ".prompt_llm"
config_file = config_dir / "config.json"

def add_to_config(key:str, value: str):
    """Set config such as api_key"""
    # Ensure the directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing config if it exists
    if config_file.exists():
        with open(config_file, "r") as file:
            config_data = json.load(file)
    else:
        config_data = {}

    # Add or update the API key
    config_data[key] = value

    # Save the updated config
    with open(config_file, "w") as file:
        json.dump(config_data, file, indent=4)

def remove_from_config(key:str):
    """Remove config such as api_key"""
    # Ensure the directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing config if it exists
    if config_file.exists():
        with open(config_file, "r") as file:
            config_data = json.load(file)
            if key in config_data:
                del config_data[key]

    # Save the updated config
    with open(config_file, "w") as file:
        json.dump(config_data, file, indent=4)

def load_config():
    # Load existing config if it exists
    if config_file.exists():
        with open(config_file, "r") as file:
            app_config = json.load(file)

    return app_config
