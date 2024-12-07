import uuid
from enum import Enum

from pydantic import BaseModel


class ModelTypeEnum(Enum):
    openai = "openai"
    anthropic = "anthropic"


class ModelDTO(BaseModel):
    id: uuid.UUID
    name: str
    space_id: uuid.UUID
    nickname: str
    base_url: str
    api_key: str
    type: ModelTypeEnum
