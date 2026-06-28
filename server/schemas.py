from pydantic import BaseModel
from typing import Optional, Literal

class ModelParamsSchema(BaseModel):
    context_size: Optional[int] = 2048
    temperature: Optional[float] = 0.7
    threads: Optional[int] = 2
    max_tokens: Optional[int] = 1024

class ChatRequestSchema(BaseModel):
    model: Literal["luna-v1", "luna-v1-pro"] = "luna-v1"
    system_prompt: Optional[str] = "You are Luna, a helpful assistant created by Yahya at LunaLabs organization."
    prompt: str = ""
    model_params: ModelParamsSchema
    stream: Optional[bool] = False