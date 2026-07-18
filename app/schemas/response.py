from pydantic import BaseModel

class ResponseUserSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"