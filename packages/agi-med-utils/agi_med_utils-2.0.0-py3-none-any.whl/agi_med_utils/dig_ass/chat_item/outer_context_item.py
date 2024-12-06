from pydantic import BaseModel, Field


class OuterContextItem(BaseModel):
    sex: bool = Field(..., alias="Sex")
    age: int = Field(..., alias="Age")
    user_id: str = Field(..., alias="UserId")
    session_id: str = Field(..., alias="SessionId")
    client_id: str = Field(..., alias="ClientId")
    track_id: str = Field("", alias="TrackId")
