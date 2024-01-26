from pydantic import BaseModel
from datetime import datetime

class notes(BaseModel):

    username:str
    name:str
    email:str
    password:str
    disabled: bool
    