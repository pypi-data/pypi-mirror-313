from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from drax_sdk.model.dynamic import BaseValueObject


class ActivatorType:
    EVENT = "event"
    STATE = "state"
    SCHEDULED = "scheduled"


class Activator(BaseModel):
    type: str = Field(alias="type")
    selector: str = Field(alias="selector")

    class Config:
        populate_by_name = True


class RuleVariable(BaseModel):
    name: str = Field(alias="name")
    label: str = Field(alias="label")
    value: str = Field(alias="value")

    class Config:
        populate_by_name = True


class ValuedDescriptor(BaseModel):
    variables: List[RuleVariable] = Field(alias="variables")

    class Config:
        populate_by_name = True


class ConditionDescriptor(ValuedDescriptor):
    uuid: str = Field(alias="uuid")
    type: str = Field(alias="type")


class ActionDescriptor(ValuedDescriptor):
    uuid: str = Field(alias="uuid")
    type: str = Field(alias="type")


class RuleDescriptor(BaseModel):
    uuid: str = Field(alias="uuid")
    priority: int = Field(alias="priority")
    conditions: List[ConditionDescriptor] = Field(alias="conditions")
    actions: List[ActionDescriptor] = Field(alias="actions")
    is_or: bool = Field(alias="or")

    class Config:
        populate_by_name = True


class Automation(BaseModel):
    code: str = Field(alias="code")
    activator: Activator = Field(alias="activator")
    rules: List[RuleDescriptor] = Field(alias="rules")
    last_execution: Optional[datetime] = Field(alias="lastExecution")
    description: str = Field(alias="description")
    project_id: str = Field(alias="projectId")
    active: bool = Field(alias="active")
    last_activation: Optional[datetime] = Field(alias="lastActivation")
    idle_time_from_last_activation: int = Field(alias="idleTimeFromLastActivation")
    extras: BaseValueObject = Field(alias="extras")

    class Config:
        populate_by_name = True
