import os
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_google_vertexai import ChatVertexAI
from langchain_cohere import ChatCohere
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_fireworks import ChatFireworks
from langchain_groq import ChatGroq

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .models import Configuration, dotdict

def get_model_to_invoke(config: dict):
    model, api_key, provider, temperature = config["model"], config["api_key"], config["provider"], config["temperature"]
    model_to_invoke = None

    if provider == 'openai':
        os.environ["OPENAI_API_KEY"] = api_key
        model_to_invoke = ChatOpenAI(model=model, temperature=temperature)
    elif provider == 'mistralai':
        os.environ["MISTRAL_API_KEY"] = api_key
        model_to_invoke = ChatMistralAI(model=model, temperature=temperature)
    elif provider == 'anthropic':
        os.environ["ANTHROPIC_API_KEY"] = api_key
        model_to_invoke = ChatAnthropic(model=model, temperature=temperature)
    elif provider == 'google':
        os.environ["GOOGLE_API_KEY"] = api_key
        model_to_invoke = ChatVertexAI(model=model, temperature=temperature)
    elif provider == 'cohere':
        os.environ["COHERE_API_KEY"] = api_key
        model_to_invoke = ChatCohere(model=model, temperature=temperature)
    elif provider == 'nvidia':
        os.environ["NVIDIA_API_KEY"] = api_key
        model_to_invoke = ChatNVIDIA(model=model, temperature=temperature)
    elif provider == 'fireworks':
        os.environ["FIREWORKS_API_KEY"] = api_key
        model_to_invoke = ChatFireworks(model=model, temperature=temperature)
    elif provider == 'groq':
        os.environ["GROQ_API_KEY"] = api_key
        model_to_invoke = ChatGroq(model=model, temperature=temperature)
    elif provider == 'togetherai':
        os.environ["TOGETHER_API_KEY"] = api_key
        model_to_invoke = ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=os.environ["TOGETHER_API_KEY"],
            model = model
        )
    return model_to_invoke

def validate_config(config: dict):
    if "api_key" not in config or not config["api_key"] or "model" not in config or not config["model"]:
        return False

    return True

def call(prompt: str, config: dict):
    if not validate_config(config):
        return dotdict({"content": "Configuration is incorrect!"})

    model_to_invoke = get_model_to_invoke(config)

    # Messages
    messages_langchain = []
    if "system" in config:
        messages_langchain.append(SystemMessage(content=config["system"]))

    messages_langchain.append(HumanMessage(content=prompt))

    response = model_to_invoke.invoke(messages_langchain)

    return response
