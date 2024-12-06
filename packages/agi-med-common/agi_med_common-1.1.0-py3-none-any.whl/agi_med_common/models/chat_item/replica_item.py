from pydantic import Field

from .. import _Base


class ReplicaItem(_Base):
    body: str = Field(alias="Body")
    role: bool = Field(alias="Role", description="True = ai, False = client")
    date_time: str = Field(alias="DateTime")
