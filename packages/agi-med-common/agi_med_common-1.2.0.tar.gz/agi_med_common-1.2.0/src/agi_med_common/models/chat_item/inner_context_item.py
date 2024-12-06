from pydantic import Field

from . import ReplicaItem
from .. import _Base


class InnerContextItem(_Base):
    replicas: list[ReplicaItem] = Field(alias="Replicas")
