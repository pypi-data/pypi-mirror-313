

from pydantic import BaseModel


class ParamsWS(BaseModel):
    limit: int = 10
    offset: int = 0