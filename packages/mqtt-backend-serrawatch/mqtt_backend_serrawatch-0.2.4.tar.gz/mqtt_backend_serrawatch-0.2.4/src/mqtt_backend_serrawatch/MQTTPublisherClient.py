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
        self.logger.debug(f"MQTTPublisherClient initialized with broker: {broker_address}, port: {port}, topics: {topics}")

    def on_connect(self, client, userdata, flags, rc):
        """
        Handles the connection to the MQTT broker.
        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param flags: Response flags sent by the broker.
        :param rc: The connection result.
        """
        if rc == 0:
            self.logger.info(f"Connected to broker {self.broker}:{self.port} successfully")
        else:
            self.logger.error(f"Connection error with code: {rc}")

    def connect(self):
        """
        Connects the client to the MQTT broker and starts the network loop.
        """
        self.logger.debug(f"Attempting to connect to broker {self.broker}:{self.port}")
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()
        self.logger.info("MQTT loop started")

    def publish(self, message_type: str, value: str):
        """
        Publishes a message to the specified topic based on the message type.
        :param message_type: The type of message to publish (used to determine the topic).
        :param value: The value to publish.
        """
        self.logger.debug(f"Attempting to publish message of type: {message_type} with value: {value}")
        if message_type in self.topics.publishers:
            topic = self.topics.publishers[message_type]
            self.logger.debug(f"Publishing to topic: {topic}")
            self.client.publish(topic, value)
            self.logger.info(f"Message published: {value} to {topic}")
        else:
            self.logger.warning(f"Unrecognized message type: {message_type}")

    def publish_on_interrupt(self, interrupt_event, message_type: str, value: str):
        """
        Publishes a message when an interrupt event is triggered.
        :param interrupt_event: An event object that triggers the message publication.
        :param message_type: The type of message to publish.
        :param value: The value to publish.
        """
        self.logger.debug("Waiting for an interrupt event to publish a message...")
        while not interrupt_event.is_set():
            interrupt_event.wait()  # Wait for the interrupt to be triggered
            self.logger.info("Interrupt triggered, publishing the message...")
            self.publish(message_type, value)

    def disconnect(self):
        """
        Disconnects the client from the MQTT broker.
        """
        self.logger.debug("Attempting to disconnect from MQTT broker")
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Disconnected from broker")

    @staticmethod
    def from_config(config: Config):
        """
        Creates an instance of MQTTPublisherClient from a given configuration.
        :param config: Configuration object containing broker and topic information.
        """
        broker_address = config.broker.address
        port = config.broker.port
        topics = config.topics

        LoggerSerraWatch.get_instance("SerraWatch").debug(f"Creating MQTTPublisherClient from configuration: broker_address={broker_address}, port={port}, topics={topics}")
        return MQTTPublisherClient(broker_address=broker_address, port=port, topics=topics)

