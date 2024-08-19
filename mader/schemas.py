from pydantic import BaseModel


class ReadRoot(BaseModel):
    message: str
