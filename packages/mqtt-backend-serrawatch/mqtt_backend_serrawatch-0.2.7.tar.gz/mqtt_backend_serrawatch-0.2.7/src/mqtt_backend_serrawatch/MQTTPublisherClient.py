import ssl

import paho.mqtt.client as mqtt

from .data import Config
from .data.TopicsConfig import TopicsConfig
from SerraWatchLogger.backend.LoggerSerraWatch import LoggerSerraWatch

Logger = LoggerSerraWatch.get_instance("SerraWatch")
class MQTTPublisherClient:
    def __init__(self, topics: TopicsConfig, broker_address: str, port: int = 1883):
        """
        MQTT Publisher Client for publishing messages to specific topics on an MQTT broker.
        :param topics: Configuration for the topics to publish messages to.
        :param broker_address: Address of the MQTT broker.
        :param port: Port of the MQTT broker (default is 1883).
        """
        self.broker = broker_address
        self.port = port
        self.client = mqtt.Client()

        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.topics = topics

        # Initialize logger
        self.logger = LoggerSerraWatch.get_instance("SerraWatch")
        self.logger.debug(self.logger,"[PUBLISHER] MQTTPublisherClient initialized with broker: {broker_address}, port: {port}, topics: {topics}")

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles the connection to the MQTT broker.
        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param flags: Response flags sent by the broker.
        :param rc: The connection result.
        """
        if rc == 0:
            self.logger.info(self.logger,f"[PUBLISHER] Connected to broker {self.broker}:{self.port} successfully")
        else:
            self.logger.error(self.logger,f"[PUBLISHER] Connection error with code: {rc}")

    def connect(self):
        """
        Connects the client to the MQTT broker and starts the network loop.
        """
        self.logger.debug(self.logger,f"[PUBLISHER] Attempting to connect to broker {self.broker}:{self.port}")

        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

        self.logger.debug(self.logger, f"[PUBLISHER] TLS Establish with success")

        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()
        self.logger.info(self.logger,"[PUBLISHER] MQTT loop started")

    def publish(self, message_type: str, value: str):
        """
        Publishes a message to the specified topic based on the message type.
        :param message_type: The type of message to publish (used to determine the topic).
        :param value: The value to publish.
        """
        self.logger.debug(self.logger,f"[PUBLISHER] Attempting to publish message of type: {message_type} with value: {value}")
        if message_type in self.topics.publishers:
            topic = self.topics.publishers[message_type]
            self.logger.debug(self.logger,f"[PUBLISHER] Publishing to topic: {topic}")
            self.client.publish(topic, value)
            self.logger.info(self.logger,f"[PUBLISHER] Message published: {value} to {topic}")
        else:
            self.logger.warning(self.logger,f"[PUBLISHER] Unrecognized message type: {message_type}")

    def publish_on_interrupt(self, interrupt_event, message_type: str, value: str):
        """
        Publishes a message when an interrupt event is triggered.
        :param interrupt_event: An event object that triggers the message publication.
        :param message_type: The type of message to publish.
        :param value: The value to publish.
        """
        self.logger.debug(self.logger,"[PUBLISHER] Waiting for an interrupt event to publish a message...")
        while not interrupt_event.is_set():
            interrupt_event.wait()  # Wait for the interrupt to be triggered
            self.logger.info(self.logger,"[PUBLISHER] Interrupt triggered, publishing the message...")
            self.publish(message_type, value)

    def disconnect(self):
        """
        Disconnects the client from the MQTT broker.
        """
        self.logger.debug(self.logger,"[PUBLISHER] Attempting to disconnect from MQTT broker")
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info(self.logger,"[PUBLISHER] Disconnected from broker")

    @staticmethod
    def from_config(config: Config):
        """
        Creates an instance of MQTTPublisherClient from a given configuration.
        :param config: Configuration object containing broker and topic information.
        """
        broker_address = config.broker.address
        port = config.broker.port
        topics = config.topics
        return MQTTPublisherClient(broker_address=broker_address, port=port, topics=topics)

