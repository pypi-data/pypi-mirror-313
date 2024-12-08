from pydantic import BaseModel, Field
from typing import List, Dict

class Configuration(BaseModel):
    api_key: str
    model: str
    provider: str


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__