from .BrokerConfig import BrokerConfig
from .TopicsConfig import TopicsConfig
from typing import Any

from SerraWatchLogger.backend.LoggerSerraWatch import LoggerSerraWatch
Logger = LoggerSerraWatch.get_instance("SerraWatch")


class Config:
    def __init__(self, broker: BrokerConfig, broker_public: BrokerConfig, topics: TopicsConfig):
        """
        Initializes the Config class with broker, public broker, and topics configurations.
        :param broker: Configuration for the private MQTT broker (address and port).
        :param broker_public: Configuration for the public MQTT broker (address and port).
        :param topics: Configuration for the topics to subscribe and publish to.
        """
        self.broker = broker
        self.broker_public = broker_public
        self.topics = topics
        Logger.debug(self=Logger, message="Config initialized with broker, public broker, and topics configurations.")

    @staticmethod
    def from_dict(config_dict: dict[str, Any]):
        """
        Creates an instance of Config from a dictionary.
        :param config_dict: Dictionary containing configuration data.
        """
        Logger.debug(self=Logger, message="Validating configuration dictionary.")
        Config.validate_config_dict(config_dict)
        Logger.debug(self=Logger, message="Dictionary has the correct format.")

        broker = BrokerConfig(**config_dict['broker'])
        broker_public = BrokerConfig(**config_dict['broker-public'])
        topics = TopicsConfig(
            publishers=config_dict['topics']['publishers'],
            subscribers=config_dict['topics']['subscribers']
        )

        return Config(broker=broker, broker_public=broker_public, topics=topics)

    @staticmethod
    def validate_config_dict(config_dict: dict[str, Any]):
        """
        Validates the structure of the configuration dictionary.
        :param config_dict: Dictionary containing configuration data.
        """
        required_broker_keys = {'address', 'port'}
        required_topics_keys = {'publishers', 'subscribers'}

        if 'broker' not in config_dict:
            raise ValueError("Missing 'broker' section in configuration.")
        if 'broker-public' not in config_dict:
            raise ValueError("Missing 'broker-public' section in configuration.")
        if 'topics' not in config_dict:
            raise ValueError("Missing 'topics' section in configuration.")

        broker_keys = set(config_dict['broker'].keys())
        if not required_broker_keys.issubset(broker_keys):
            missing_keys = required_broker_keys - broker_keys
            raise ValueError(f"Missing keys in 'broker' section: {missing_keys}")

        broker_public_keys = set(config_dict['broker-public'].keys())
        if not required_broker_keys.issubset(broker_public_keys):
            missing_keys = required_broker_keys - broker_public_keys
            raise ValueError(f"Missing keys in 'broker-public' section: {missing_keys}")

        topics_keys = set(config_dict['topics'].keys())
        if not required_topics_keys.issubset(topics_keys):
            missing_keys = required_topics_keys - topics_keys
            raise ValueError(f"Missing keys in 'topics' section: {missing_keys}")

        # Validate that publishers and subscribers are lists
        if not isinstance(config_dict['topics']['publishers'], list):
            raise ValueError("'publishers' section must be a list.")
        if not isinstance(config_dict['topics']['subscribers'], list):
            raise ValueError("'subscribers' section must be a list.")