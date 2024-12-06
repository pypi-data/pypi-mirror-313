from pydantic import Field

from .. import _Base
from ..enums import TrackIdEnum


class OuterContextItem(_Base):
    sex: bool = Field(alias="Sex", description="True = male, False = female")
    age: int = Field(alias="Age")
    user_id: str = Field(alias="UserId")
    session_id: str = Field(alias="SessionId")
    client_id: str = Field(alias="ClientId")
    track_id: TrackIdEnum = Field(TrackIdEnum.DIAGNOSTIC, alias="TrackId")

    def create_id(self, short: bool = False) -> str:
        if short:
            return f"{self.user_id}_{self.session_id}_{self.client_id}"
        return f"user_{self.user_id}_session_{self.session_id}_client_{self.client_id}"
