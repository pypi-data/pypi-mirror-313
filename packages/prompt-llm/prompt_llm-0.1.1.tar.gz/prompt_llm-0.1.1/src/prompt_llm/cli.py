#!/usr/bin/env python

import typer
import json
import os

from .utils import add_to_config, remove_from_config, load_config
from .langchain_util import call

app = typer.Typer()

@app.command()
def add_config(api_key: str='', system: str = '', temperature:float = None):
    """To set a config"""
    if api_key:
        add_to_config('api_key', api_key)

    if system:
        add_to_config('system', system)
    
    if temperature is not None:
        add_to_config('temperature', temperature)

@app.command()
def rm_config(key: str):
    """To unset a config"""
    remove_from_config(key)


@app.command()
async def mistralai(prompt: str):
    """Tool to prompt mistralai"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = "mistralai"
        app_config["model"] = "mistral-large-latest"

        response = await call(prompt, app_config)

        print(response)

@app.command()
def openai(prompt: str):
    """Tool to prompt openai"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = "openai"
        app_config["model"] = "gpt-4o"

        response = call(prompt, app_config)

        print(response.content)


@app.command()
def version():
    """Retrieve the version"""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    init_file = os.path.join(package_dir, '__init__.py')

    with open(init_file, 'r') as file:
        for line in file:
            if line.startswith('__version__'):
                # Extract version from the line
                version = line.split('=')[-1].strip().strip('"').strip("'")
                print(version)

if __name__ == "__main__":
    app()
