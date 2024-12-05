from pydantic import BaseModel


class DeleteUserV0(BaseModel):
    password: str
