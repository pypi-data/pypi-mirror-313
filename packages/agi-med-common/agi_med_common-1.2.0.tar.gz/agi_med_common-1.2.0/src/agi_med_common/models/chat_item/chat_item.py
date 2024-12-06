from pydantic import Field

from . import OuterContextItem, InnerContextItem
from .. import _Base


class ChatItem(_Base):
    outer_context: OuterContextItem = Field(alias="OuterContext")
    inner_context: InnerContextItem = Field(alias="InnerContext")
