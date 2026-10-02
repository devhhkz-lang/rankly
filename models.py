from pydantic import BaseModel, Field
from typing import Annotated

class Player(BaseModel):
    player_name: Annotated[
        str, 
        Field(..., min_length=3, max_length=15)
    ]
    player_id: Annotated[
        int,
        Field(..., ge=1, le=1000)
    ]

class Number(BaseModel):
    number: Annotated[
        int,
        Field(..., ge=0, le=100)
    ]