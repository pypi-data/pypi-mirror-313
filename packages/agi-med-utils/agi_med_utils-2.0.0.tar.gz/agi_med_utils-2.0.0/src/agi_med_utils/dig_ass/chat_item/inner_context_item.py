from pydantic import BaseModel, Field

from . import ReplicaItem


class InnerContextItem(BaseModel):
    replicas: list[ReplicaItem] = Field(..., alias="Replicas")
