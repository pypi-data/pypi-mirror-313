from collections.abc import Callable
from typing import List, Any, Dict

from drax_sdk.broker.amqp_broker import DraxAmqpBroker
from drax_sdk.clients.drax_core_client import DraxCoreClient
from drax_sdk.model.config import DraxConfigParams
from drax_sdk.model.dto import (
    PagedResult,
    HandshakeRequest,
    HandshakeResponse,
    InstalledNode,
    FindNodeByIdsRequest,
    StateRequest,
    ConfigurationRequest,
    StateResponse,
    FlatConfigurationResponse,
    InstallRequest,
    PrepareRequest,
)
from drax_sdk.model.event import Event
from drax_sdk.model.node import NodeType, Node, State, Configuration
from drax_sdk.model.project import Project
from drax_sdk.utils.codec import encode_state
from drax_sdk.utils.keystore import KeyStore


class DraxCore:

    client: DraxCoreClient
    config: DraxConfigParams

    def __init__(self, client: DraxCoreClient, config: DraxConfigParams):
        self.client = client
        self.config = config

    def register_node_type(self, node_type: NodeType) -> NodeType:
        return self.client.register_node_type(node_type)

    def update_node_type(self, node_type: NodeType) -> None:
        return self.client.update_node_type(node_type)

    def get_node_type_by_id(self, node_type_id: str) -> NodeType:
        return self.client.get_node_type_by_id(node_type_id)

    def unregister_node_type(self, node_type_id: str) -> None:
        self.client.unregister_node_type(node_type_id)

    # todo: da controllare perche il client non sembra avere parametri
    def list_node_types(self, project_id: str | None = None,) -> PagedResult[NodeType]:
        return self.client.list_node_types(project_id)

    def handshake(self, request: HandshakeRequest) -> HandshakeResponse:
        return self.client.handshake(request)

    def get_my_project(self) -> Project:
        return self.client.get_my_project()

    def get_project_by_id(self, id: str) -> Project:
        return self.client.get_project_by_id(id)

    def register_project(self, project: Project) -> Project:
        return self.client.register_project(project)

    def update_project(self, project: Project) -> None:
        self.client.update_project(project)

    def unregister_project(self, id: str) -> None:
        self.client.unregister_project(id)

    def prepare_node(self, request: PrepareRequest) -> InstalledNode:
        return self.client.prepare_node(request)

    def install_node(self, request: InstallRequest) -> InstalledNode:
        return self.client.install_node(request)

    # def generate_key_pair(self, request: ECDHKeysPairRequest) -> ECDHKeysPairResponse:
    #     return self.client.generate_keys_pair(request)
    #
    # def revoke_key_pair(self, request: ECDHRevokeRequest) -> ECDHRevokeResponse:
    #     return self.client.revoke_key(request)

    def update_node(self, node: Node) -> None:
        self.client.update_node(node)

    def uninstall_node(self, node_id: str) -> None:
        self.client.uninstall_node(node_id)

    def get_node_by_id(self, node_id: str) -> Node:
        return self.client.get_node_by_id(node_id)

    def get_nodes_by_ids(
        self, find_node_by_ids_request: FindNodeByIdsRequest
    ) -> List[Node]:
        return self.client.get_nodes_by_ids(find_node_by_ids_request)

    def list_projects(self, page: int = None, size: int = None) -> PagedResult[Project]:
        return self.client.list_projects()

    def list_nodes(
        self,
        project_id: str | None = None,
        keyword: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> PagedResult[Node]:
        return self.client.list_nodes(project_id, keyword, page, size)

    def list_states(
        self,
        node_id: str,
        project_id: str | None = None,
        from_time: int = None,
        to_time: int = None,
        page: int = 1,
        size: int = 10,
    ) -> PagedResult[StateResponse]:

        return self.client.list_states(
            node_id=node_id,
            project_id=project_id,
            from_time=from_time,
            to_time=to_time,
            page=page,
            size=size,
        )

    def list_configurations(
        self,
        node_id: str,
        from_time: int = None,
        to_time: int = None,
        page: int = 1,
        size: int = 10,
    ) -> PagedResult[FlatConfigurationResponse]:

        return self.client.list_configurations(
            node_id=node_id,
            from_time=from_time,
            to_time=to_time,
            page=page,
            size=size,
        )

    def list_nodes_states(
        self,
        find_node_by_ids_request: FindNodeByIdsRequest,
        start: int,
        end: int,
        page: int,
        size: int,
        project_id: str | None = None,
    ) -> PagedResult[StateResponse]:

        return self.client.list_nodes_states(
            project_id, find_node_by_ids_request, start, end, page, size
        )

    def set_state(self, node_id: str, state_request: StateRequest) -> None:
        self.client.set_state(node_id, state_request)

    def get_state(self, node_id: str) -> StateResponse:
        return self.client.get_state(node_id)

    def set_configuration(
        self, node_id: str, configuration_request: ConfigurationRequest
    ) -> None:
        # convert all values in str
        for key, value in configuration_request.configuration.items():
            configuration_request.configuration[key] = str(value)

        self.client.set_configuration(node_id, configuration_request)

    def invoke(self, event: Event) -> None:
        self.client.invoke(event)


class Drax:
    def __init__(self, config: DraxConfigParams):
        self.config = config
        self.core = DraxCore(
            DraxCoreClient(config.drax_core_url, config.api_key, config.api_secret),
            config,
        )
        # self.drax_automation = DraxAutomation(
        #     AutomationClient(config.automation_url, config.api_key, config.api_secret)
        # )
        # self.drax_data_miner = DraxDataMiner(
        #     DataMinerClient(config.data_miner_url, config.api_key, config.api_secret)
        # )
        # self.drax_ai = DraxAi(
        #     AiClient(config.ai_url, config.api_key, config.api_secret)
        # )
        self.broker = DraxAmqpBroker(config)

    def start(self):
        self.broker.start()
        pass

    def stop(self):
        self.broker.stop()
        pass

    # def get_backend(self):
    #     return self.drax_backend
    #
    # def get_automation(self):
    #     return self.drax_automation
    #
    # def get_data_miner(self):
    #     return self.drax_data_miner

    def set_state(
        self,
        state: State | Dict[str, Any],
        node_id: str = None,
        cryptography_disabled=False,
        urn: str = None,
    ):
        if not isinstance(state, State):
            if node_id is None:
                raise ValueError("node_id must be provided")

        node_id = node_id if node_id else state.node_id
        if not node_id and not urn:
            raise ValueError("Either node_id or urn must be provided")

        node_private_key = KeyStore.get_private_key(node_id)

        request = StateRequest(
            node_id=node_id,
            state=encode_state(node_private_key, state),
            cryptography_disabled=cryptography_disabled,
            urn=urn,
        )
        self.core.set_state(node_id, request)

    def set_configuration(
        self,
        configuration: Configuration | Dict[str, Any],
        node_id: str = None,
        cryptography_disabled=False,
        urn: str = None,
    ):
        if not isinstance(configuration, Configuration):
            if node_id is None:
                raise ValueError("node_id must be provided")

        node_id = node_id if node_id else configuration.node_id
        if not node_id and not urn:
            raise ValueError("Either node_id or urn must be provided")

        configuration_map = (
            configuration.to_map()
            if isinstance(configuration, Configuration)
            else configuration
        )

        self.core.set_configuration(
            node_id,
            ConfigurationRequest(
                node_id=node_id,
                configuration=configuration_map,
                cryptography_disabled=cryptography_disabled,
                urn=urn,
            ),
        )

    def add_configuration_listener(
        self, topic: str, listener: Callable[[Configuration], None]
    ):
        self.broker.add_configuration_listener(topic, listener)

    def add_state_listener(self, topic: str, listener: Callable[[State], None]):
        self.broker.add_state_listener(topic, listener)

    def add_events_listener(
        self, listener: Callable[[Event], None], project_id: str = None
    ):
        project_id = project_id or self.config.project_id
        if not project_id:
            raise ValueError("project_id is required")

        self.broker.add_event_listener(project_id=project_id, cb=listener)
