#!/usr/bin/env python

import typer
import json
import os

from .utils import add_to_config, remove_from_config, load_config, print_response
from .langchain_util import call
from .constants import OPENAI, MISTRALAI, ANTHROPIC, GOOGLE, COHERE, NVIDIA, FIREWORKS, GROQ, TOGETHER

app = typer.Typer()

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

@app.command()
def config(api_key: str='', model: str='', system: str = '', temperature:float = None):
    """To set a config"""
    if api_key:
        add_to_config('api_key', api_key)
    else:
        print('Please specify the API KEY.')

    if not system:
        system = 'You are an assistant helping the users promptly.'

    add_to_config('system', system)

    if model:
        add_to_config('model', model)
    else:
        print('Please specify the model.')
    
    if temperature is not None:
        add_to_config('temperature', temperature)

@app.command()
def config_rm(key: str):
    """To unset a config"""
    remove_from_config(key)

@app.command()
def config_ls():
    """To view config"""
    config = load_config()
    print(json.dumps(config, sort_keys=True, indent=4))

@app.command()
async def mistralai(prompt: str):
    """To prompt MISTRALAI"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = MISTRALAI

        if "model" not in app_config:
            app_config["model"] = "mistral-large-latest"

        response = await call(prompt, app_config)
        print_response(response, MISTRALAI)

@app.command()
def openai(prompt: str):
    """To prompt OPENAI"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = OPENAI
        if "model" not in app_config:
            app_config["model"] = "gpt-4o"

        response = call(prompt, app_config)
        print_response(response, OPENAI)

@app.command()
def anthropic(prompt: str):
    """To prompt ANTHROPIC"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = "anthropic"
        if "model" not in app_config:
            app_config["model"] = "claude-3-5-sonnet-latest"

        response = call(prompt, app_config)
        print_response(response, ANTHROPIC)


@app.command()
def google(prompt: str):
    """To prompt GOOGLE"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = GOOGLE
        if "model" not in app_config:
            app_config["model"] = "gemini-1.5-pro-latest"

        response = call(prompt, app_config)
        print_response(response, GOOGLE)

@app.command()
def cohere(prompt: str):
    """To prompt COHERE"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = COHERE
        if "model" not in app_config:
            app_config["model"] = "command-xlarge-nightly"

        response = call(prompt, app_config)
        print_response(response, COHERE)

@app.command()
def nvidia(prompt: str):
    """To prompt NVIDIA"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = NVIDIA
        if "model" not in app_config:
            app_config["model"] = "nemo-gpt-megatron-turing-530b"

        response = call(prompt, app_config)
        print_response(response, NVIDIA)


@app.command()
def fireworks(prompt: str):
    """To prompt FIREWORKS"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = FIREWORKS
        if "model" not in app_config:
            app_config["model"] = ""

        response = call(prompt, app_config)
        print_response(response, FIREWORKS)

@app.command()
def grow(prompt: str):
    """To prompt GROQ"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = GROQ
        if "model" not in app_config:
            app_config["model"] = ""

        response = call(prompt, app_config)
        print_response(response, GROQ)


@app.command()
def together(prompt: str):
    """To prompt TOGETHER"""
    app_config = load_config()

    if prompt:
        app_config["provider"] = TOGETHER
        if "model" not in app_config:
            app_config["model"] = ""

        response = call(prompt, app_config)
        print_response(response, TOGETHER)

if __name__ == "__main__":
    app()
