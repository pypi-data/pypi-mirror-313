from typing import Dict

from pydantic import BaseModel, Field

from drax_sdk.model.node import Node
from drax_sdk.utils.timestamp import unix_timestamp


class Event(BaseModel):
    timestamp: int = Field(default_factory=unix_timestamp)
    node: Node | None = None
    project_id: str | None = Field(alias="projectId", default=None)
    type: str
    values: Dict[str, str] | None = None

    @classmethod
    def create(cls, type: str, project_id: str, node: str, params: Dict[str, str]):
        event = cls(type=type, project_id=project_id, node=node)
        for key, value in params.items():
            setattr(event, key, value)
        return event

    class Config:
        populate_by_name = True
