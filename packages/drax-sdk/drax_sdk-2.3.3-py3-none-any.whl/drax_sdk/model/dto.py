from typing import Optional, List, TypeVar, Generic, Dict

from pydantic import Field, BaseModel

from drax_sdk.model.dynamic import Value
from drax_sdk.model.node import State
from drax_sdk.model.utils import BytesBase64Model
from drax_sdk.utils.timestamp import unix_timestamp

T = TypeVar("T")


class PagedResult(BaseModel, Generic[T]):
    results: List[T] = []
    total_rows: int = Field(alias="totalRows")

    class Config:
        populate_by_name = True


class HandshakeRequest(BaseModel):
    node_id: int | None = Field(alias="nodeId", default=None)
    name: str | None = None
    association_code: str | None = Field(alias="associationCode", default=None)
    urn: str | None = None
    project_id: str | None = Field(alias="projectId", default=None)
    supported_types: List[str] | None = Field(alias="supportedTypes", default=None)
    configuration_publish_topic: str | None = Field(
        alias="configurationPublishTopic", default=None
    )
    state_publish_topic: str | None = Field(alias="statePublishTopic", default=None)
    initial_state: State | None = Field(alias="initialState", default=None)
    extras: List[Value] | None = None

    class Config:
        populate_by_name = True


class HandshakeResponse(BaseModel):
    node_id: int = Field(alias="nodeId")
    urn: str
    public_key: bytes | None = Field(alias="publicKey")
    private_key: bytes | None = Field(alias="privateKey")

    class Config:
        populate_by_name = True


class AssociationRequest(BaseModel):
    apiKey: str
    apiSecret: str
    associationCode: str
    urn: str


class ConfigurationRequest(BaseModel):
    api_key: str | None = Field(alias="apiKey", default=None)
    api_secret: str | None = Field(alias="apiSecret", default=None)
    node_id: Optional[int] = Field(alias="nodeId", default=None)
    urn: str | None = None
    codec: str | None = None
    cryptography_disabled: bool = Field(alias="cryptographyDisabled", default=False)
    timestamp: int = Field(alias="timestamp", default_factory=unix_timestamp)
    configuration: Dict[str, str]

    @classmethod
    def from_configuration(cls, configuration):
        return cls(
            node_id=configuration.node_id,
            timestamp=configuration.timestamp,
            configuration=configuration.to_map(),
        )

    class Config:
        populate_by_name = True


class ConfigurationResponse(BytesBase64Model):
    node_id: str = Field(alias="nodeId")
    timestamp: int = Field(alias="timestamp")
    urn: str | None = Field(alias="urn", default=None)
    configuration: bytes = Field(alias="configuration")
    cryptography_disabled: bool = Field(alias="cryptographyDisabled", default=False)

    class Config:
        populate_by_name = True


class PrepareRequest(BaseModel):
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
    script: Optional[str] = None
    max_idle_time: int = Field(0, alias="maxIdleTime")
    last_check: int = Field(default=unix_timestamp(), alias="lastCheck")
    state: State = State()

    class Config:
        populate_by_name = True


class InstallRequest(BaseModel):
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
    script: Optional[str] = None
    max_idle_time: int = Field(0, alias="maxIdleTime")
    last_check: int = Field(default=unix_timestamp(), alias="lastCheck")
    state: State = State()

    class Config:
        populate_by_name = True


class FlatConfigurationResponse(BaseModel):
    node_id: Optional[str] = Field(alias="nodeId")
    urn: Optional[str] = None
    timestamp: int
    configuration: Dict[str, str]

    @classmethod
    def from_node_and_entry(cls, node, state):
        return cls(
            nodeId=node.id,
            urn=node.urn,
            timestamp=state.timestamp,
            state=state.to_map(),
        )

    @classmethod
    def from_state(cls, state):
        return cls(nodeId=state.nodeId, timestamp=state.timestamp, state=state.to_map())


class StateRequest(BytesBase64Model):
    api_key: str = Field(alias="apiKey", default=None)
    api_secret: str = Field(alias="apiSecret", default=None)
    node_id: Optional[str] = Field(alias="nodeId", default=None)
    urn: Optional[str] = None
    timestamp: int = None
    state: bytes
    codec: str = None
    cryptography_disabled: bool = Field(alias="cryptographyDisabled", default=False)

    class Config:
        populate_by_name = True


class StateResponse(BaseModel):
    node_id: Optional[str] = Field(alias="nodeId")
    urn: Optional[str] = None
    timestamp: int
    state: Dict[str, str]

    @classmethod
    def from_node_and_entry(cls, node, state):
        return cls(
            nodeId=node.id,
            urn=node.urn,
            timestamp=state.timestamp,
            state=state.to_map(),
        )

    @classmethod
    def from_state(cls, state):
        return cls(nodeId=state.nodeId, timestamp=state.timestamp, state=state.to_map())


class AuthenticationRequest(BaseModel):
    api_key: str = Field(alias="apiKey")
    api_secret: str = Field(alias="apiSecret")

    class Config:
        populate_by_name = True


class FindNodeByIdsRequest(BaseModel):
    node_ids: List[int] = Field(alias="nodeIds")

    class Config:
        populate_by_name = True


from pydantic import Field
from typing import Optional


class InstalledNode(BytesBase64Model):
    id: str
    urn: str
    public_key: Optional[bytes] = Field(None, alias="publicKey")
    private_key: Optional[bytes] = Field(None, alias="privateKey")

    @property
    def public_key_hex(self) -> str:
        if self.public_key is None:
            return ""
        return self.public_key.hex()

    @property
    def private_key_hex(self) -> str:
        if self.private_key is None:
            return ""
        return self.private_key.hex()

    class Config:
        populate_by_name = True
