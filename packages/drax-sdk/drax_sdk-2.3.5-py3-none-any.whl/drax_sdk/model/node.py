from typing import List, Optional, Any

from pydantic import BaseModel, Field

from drax_sdk.model.dynamic import NodeEntry
from drax_sdk.model.utils import BytesBase64Model
from drax_sdk.utils.timestamp import unix_timestamp


class ECDHKeyType:
    ACTIVE = "active"
    DEFAULT = "default"
    REVOKED = "revoked"


class ECDHKey(BytesBase64Model):
    key: bytes
    status: str


class State(NodeEntry):

    def merge(self, node_entry: NodeEntry):
        for value in node_entry.all_values():
            self.set_value(value.name, value.value)


class Configuration(NodeEntry):

    def merge(self, node_entry: NodeEntry):
        for value in node_entry.all_values():
            self.set_value(value.name, value.value)


class Property(BaseModel):
    name: str
    type: str


class Descriptor(BaseModel):
    properties: List[Property]

    def add_property(self, name: str, type: str):
        if not any(p.name == name for p in self.properties):
            self.properties.append(Property(name=name, type=type))


class NodeType(BaseModel):
    id: str
    name: str
    tag: Optional[str] = Field(default=None)
    project_id: str | None = Field(alias="projectId", default=None)
    peripherals: Descriptor

    def supports(self, property_name: str):
        return any(p == property_name for p in self.peripherals.properties)

    class Config:
        populate_by_name = True


class Value(BaseModel):
    name: str
    value: str


class Node(BaseModel):
    id: Optional[str] = Field(None)
    association_code: Optional[str] = Field(alias="associationCode", default=None)
    project_id: Optional[str] = Field(None, alias="projectId")
    name: str
    urn: Optional[str] = None
    tag: Optional[str] = None
    supported_types: List[str] = Field(default_factory=set, alias="supportedTypes")
    state_publish_topic: Optional[str] = Field(None, alias="statePublishTopic")
    configuration_publish_topic: Optional[str] = Field(
        None, alias="configurationPublishTopic"
    )
    public_keys: List[ECDHKey] = Field(default_factory=list, alias="publicKeys")
    active: bool = False
    script: Optional[str] = None
    max_idle_time: int = Field(0, alias="maxIdleTime")
    last_check: int = Field(default=unix_timestamp(), alias="lastCheck")
    status: Optional[str] = None
    state: State = State()
    values: List[Value] = Field(default_factory=list)

    def add_supported_type(self, type: str):
        self.supported_types.append(type)

    def add_public_key(self, public_key: bytes):
        if not any(k.key == public_key for k in self.public_keys):
            self.public_keys.append(ECDHKey(key=public_key, status=ECDHKeyType.ACTIVE))

    def supports(self, type: str) -> bool:
        return type in self.supported_types

    def revoke_public_key(self, public_key: bytes):
        for key in self.public_keys:
            if key.key == public_key:
                key.status = ECDHKeyType.REVOKED

    def is_key_enabled(self, public_key: bytes) -> bool:
        return any(
            k.key == public_key
            and k.status in (ECDHKeyType.ACTIVE, ECDHKeyType.DEFAULT)
            for k in self.public_keys
        )

    def set_single_public_key(self, public_key: bytes):
        self.public_keys = [ECDHKey(key=public_key, status=ECDHKeyType.DEFAULT)]

    def get_default_key(self) -> Optional[bytes]:
        for key in self.public_keys:
            if key.status == ECDHKeyType.DEFAULT:
                return key.key
        for key in self.public_keys:
            if key.status == ECDHKeyType.ACTIVE:
                return key.key
        return None

    def set_value(self, name: str, value: Any):
        self.values.append(Value(name=name, value=str(value)))

    def get_value(self, name: str) -> str | None:
        for value in self.values:
            if value.name == name:
                return value.value
        return None

    class Config:
        populate_by_name = True
