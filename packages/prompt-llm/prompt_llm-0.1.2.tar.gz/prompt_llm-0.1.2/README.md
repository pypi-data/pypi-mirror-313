# prompt_llm

## Version
0.1.2

- Prompt LLMs via cli

## Installation

1. Clone the repo

2. Install
- Local:
    - `pip install --editable .`
- PyPi:
    - `pip install prompt_llm`

3. Install auto-completion:
- `prompt_llm --install-completion`
- `source ~/.bashrc`

## Config:
- Supported configs: `--api-key`, `model`, `--system`, `--temperature`

### Set Config
- `add_config  --api-key "<api_key>" --system "<system_messgae>" --temperature <temperature>`

### Remove Config:
- `prompt_llm rm-config temperature`

### View Config:
- `prompt_llm view-config`

## Run cli
- `prompt_llm openai "Tell me something"`


## To contribute

### 1. Build project
`python -m build`

### 2. Upload
`python3 -m twine upload --repository pypi dist/* --verbose`