from pydantic import BaseModel, Field

from . import OuterContextItem, InnerContextItem


class ChatItem(BaseModel):
    outer_context: OuterContextItem = Field(..., alias="OuterContext")
    inner_context: InnerContextItem = Field(..., alias="InnerContext")
