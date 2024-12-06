import json
import logging
import threading
import time
import uuid
from abc import ABC, abstractmethod
from typing import Callable, List, TypeVar, Generic

import pika
from pika import SelectConnection
from pika.channel import Channel

from drax_sdk.model.config import DraxConfigParams
from drax_sdk.model.dto import ConfigurationResponse, StateResponse
from drax_sdk.model.event import Event
from drax_sdk.model.node import Configuration, State
from drax_sdk.utils.codec import decode_configuration
from drax_sdk.utils.keystore import KeyStore

logger = logging.getLogger(__name__)


T = TypeVar("T")


class Listener(ABC, Generic[T]):
    id: str = uuid.uuid4().hex
    routing_key: str
    queue: str | None = None
    callback: Callable[[T], None]
    exchange: str = "amq.topic"
    auto_ack: bool = True
    node_id: str | None = None

    _channel: Channel

    def __init__(
        self,
        exchange: str,
        routing_key: str,
        callback: Callable[[T], None],
        queue: str = "",
        auto_ack: bool = True,
        node_id: str = None,
    ):
        self.exchange = exchange
        self.routing_key = routing_key
        self.callback = callback
        self.queue = queue
        self.auto_ack = auto_ack
        self.node_id = node_id

    def on_queue_declared(self, method_frame):
        self.queue = method_frame.method.queue
        self._channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue,
            routing_key=self.routing_key,
            callback=self.on_queue_bound,
        )

    def on_queue_bound(self, method_frame):
        self._channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.on_message,
            auto_ack=self.auto_ack,
        )

    @abstractmethod
    def on_message(self, ch, method, properties, body):
        raise NotImplementedError

    def start_consuming(self, channel: Channel):
        self._channel = channel

        if self._channel is None:
            return

        self._channel.queue_declare(
            queue=self.queue,
            durable=False,
            exclusive=True,
            auto_delete=True,
            callback=self.on_queue_declared,
        )

    def stop_consuming(self):
        if (
            self._channel is not None
            and self.queue is not None
            and self._channel.is_open
        ):
            self._channel.queue_unbind(
                queue=self.queue,
                exchange=self.exchange,
                routing_key=self.routing_key,
            )
            self._channel.basic_cancel(self.queue)


class ConfigurationListener(Listener[Configuration]):

    def __init__(
        self,
        routing_key: str,
        callback: Callable[[Configuration], None],
        node_id: str | None = None,
    ):
        super().__init__(
            routing_key=routing_key,
            callback=callback,
            exchange="amq.topic",
            queue="",
            node_id=node_id,
        )

    def on_message(self, ch, method, properties, body):
        try:
            logger.info("Received configuration: %r", properties)
            json_data = json.loads(body.decode("utf-8"))
            configuration_response = ConfigurationResponse.model_validate(json_data)

            if self.node_id is not None:
                if configuration_response.node_id != self.node_id:
                    logger.info(
                        "Configuration for node %s not for listener %s. Ignoring...",
                        configuration_response.node_id,
                        self.id,
                    )
                    return

            if configuration_response.cryptography_disabled:
                configuration_map = json.loads(
                    configuration_response.configuration.decode()
                )
            else:
                node_private_key = KeyStore.get_private_key(
                    configuration_response.node_id
                )

                configuration_map = decode_configuration(
                    node_private_key, configuration_response.configuration
                )

            configuration = Configuration.from_dict(configuration_map)
            configuration.timestamp = configuration_response.timestamp
            configuration.node_id = configuration_response.node_id

            self.callback(configuration)
        except Exception as e:
            logger.error("Error processing configuration: %s", e)


class StateListener(Listener[State]):
    def __init__(
        self,
        routing_key: str,
        callback: Callable[[State], None],
        node_id: str | None = None,
    ):
        super().__init__(
            routing_key=routing_key,
            callback=callback,
            exchange="amq.topic",
            queue="",
            node_id=node_id,
        )

    def on_message(self, ch, method, properties, body):
        try:
            logger.info("Received state: %r", properties)
            json_data = json.loads(body.decode("utf-8"))
            state_response = StateResponse.model_validate(json_data)

            if self.node_id is not None:
                if state_response.node_id != self.node_id:
                    logger.info(
                        "State for node %s not for listener %s. Ignoring...",
                        state_response.node_id,
                        self.id,
                    )
                    return

            state = State.from_dict(state_response.state)
            state.node_id = state_response.node_id
            state.timestamp = state_response.timestamp

            self.callback(state)
        except Exception as e:
            logger.error("Error processing state: %s", e)


class EventListener(Listener[Event]):
    def __init__(
        self,
        routing_key: str,
        callback: Callable[[Event], None],
        node_id: str | None = None,
    ):
        super().__init__(
            routing_key=routing_key,
            callback=callback,
            exchange="amq.topic",
            queue="",
            node_id=node_id,
        )

    def on_message(self, ch, method, properties, body):
        try:
            logger.info("Received state: %r", properties)
            json_data = json.loads(body.decode("utf-8"))
            event = Event.model_validate(json_data)

            if event:
                self.callback(event)
        except Exception as e:
            logger.error("Error processing state: %s", e)


class DraxAmqpBroker:

    _thread: threading.Thread | None
    _configuration: DraxConfigParams
    _connection: SelectConnection | None
    _channel: SelectConnection | None
    _listeners: List[Listener]
    _running = False

    def __init__(self, configuration: DraxConfigParams):
        self._thread = None
        self._configuration = configuration
        self._connection = None
        self._channel = None
        self._listeners = []

    def _connect(self):
        logger.info(
            f"Connecting to AMQP broker at host {self._configuration.broker_host}, vhost {self._configuration.broker_vhost}"
        )
        params = pika.ConnectionParameters(
            host=self._configuration.broker_host,
            virtual_host=self._configuration.broker_vhost,
            credentials=pika.PlainCredentials(
                self._configuration.api_key, self._configuration.api_secret
            ),
        )
        self._connection = pika.SelectConnection(
            params,
            on_open_callback=self.on_connection_open,
            on_close_callback=self.on_connection_closed,
            on_open_error_callback=self.on_connection_error,
        )

        self._connection.ioloop.start()

    def on_connection_open(self, unused_connection):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self._channel = channel
        for listener in self._listeners:
            listener.start_consuming(channel)

    def on_connection_error(self, connection, error):
        logger.error("Connection error: %s", repr(error))
        self._connection.ioloop.stop()

        if self._thread and self._thread.is_alive() and self._running:
            logger.info("Reconnecting...")
            time.sleep(5)
            self._connect()

    def add_configuration_listener(
        self,
        topic: str,
        cb: Callable[[Configuration], None],
        project_id: str = None,
        node_id: str = None,
    ):
        project_id = project_id or self._configuration.project_id
        project_topic = f"{project_id}/{topic}".replace("/", ".")

        listener = ConfigurationListener(
            routing_key=project_topic, callback=cb, node_id=node_id
        )
        self._listeners.append(listener)

        logger.info(
            "Registered configuration listener %s for topic: %s",
            listener.id,
            project_topic,
        )

        listener.start_consuming(self._channel)

    def add_state_listener(
        self,
        topic: str,
        cb: Callable[[State], None],
        project_id: str = None,
        node_id: str = None,
    ):
        project_id = project_id or self._configuration.project_id
        project_topic = f"{project_id}/{topic}".replace("/", ".")

        listener = StateListener(
            routing_key=project_topic, callback=cb, node_id=node_id
        )
        self._listeners.append(listener)

        logger.info(
            "Registered state listener %s for topic: %s",
            listener.id,
            project_topic,
        )

        listener.start_consuming(self._channel)

    def add_event_listener(self, cb: Callable[[Event], None], project_id: str = None):
        project_id = project_id or self._configuration.project_id
        project_topic = f"{project_id}/events".replace("/", ".")

        listener = EventListener(routing_key=project_topic, callback=cb)
        self._listeners.append(listener)

        logger.info(
            "Registered events listener %s for topic: %s",
            listener.id,
            project_topic,
        )

        listener.start_consuming(self._channel)

    def start(self):
        logger.info("Starting broker...")
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        logger.info("Stopping broker...")
        self._running = False
        if self._connection is not None:
            for listener in self._listeners:
                listener.stop_consuming()

            self._channel.close()
            self._connection.close()
            self._connection.ioloop.stop()

            logger.info("Broker stopped")

    def on_connection_closed(self, connection, reason):
        logger.info("Connection closed: %s", reason)

        for listener in self._listeners:
            listener.stop_consuming()

        self._connection.ioloop.stop()
        if self._thread and self._thread.is_alive() and self._running:
            logger.info("Reconnecting...")
            time.sleep(5)  # delay before attempting to reconnect
            self._connect()
            self._connection.ioloop.start()

    def _run(self):
        self._connect()
