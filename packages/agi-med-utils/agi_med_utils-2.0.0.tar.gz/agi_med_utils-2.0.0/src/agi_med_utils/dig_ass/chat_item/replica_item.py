from pydantic import BaseModel, Field


class ReplicaItem(BaseModel):
    body: str = Field(..., alias="Body")
    role: bool = Field(..., alias="Role")
    date_time: str = Field(..., alias="DateTime")
    state: str = Field("", alias="State")
