from pydantic import BaseModel, Field
from typing import List, Dict

class Configuration(BaseModel):
    api_key: str
    model: str
    provider: str