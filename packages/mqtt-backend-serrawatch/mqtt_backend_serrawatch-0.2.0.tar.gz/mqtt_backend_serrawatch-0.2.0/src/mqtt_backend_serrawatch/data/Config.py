from .BrokerConfig import BrokerConfig
from .TopicsConfig import TopicsConfig
from typing import Any

from SerraWatchLogger.backend.LoggerSerraWatch import LoggerSerraWatch
Logger = LoggerSerraWatch.get_instance("SerraWatch")
class Config:
    def __init__(self, broker: BrokerConfig, topics: TopicsConfig):
        self.broker = broker
        self.topics = topics
        Logger.debug(self=Logger, message="Config initialized with broker and topics configurations.")


    @staticmethod
    def from_dict(config_dict: dict[str, Any]):
        Logger.debug(self=Logger, message="Validating configuration dictionary.")
        Config.validate_config_dict(config_dict)
        Logger.debug(self=Logger, message="Dictionary has the correct format.")

        broker = BrokerConfig(**config_dict['broker'])
        topics = TopicsConfig(
            publishers=config_dict['topics']['publishers'],
            subscribers=config_dict['topics']['subscribers']
        )

        return Config(broker=broker, topics=topics)

    @staticmethod
    def validate_config_dict(config_dict: dict[str, Any]):
        required_broker_keys = {'address', 'port'}
        required_topics_keys = {'publishers', 'subscribers'}

        if 'broker' not in config_dict:
            raise ValueError("Missing 'broker' section in configuration.")
        if 'topics' not in config_dict:
            raise ValueError("Missing 'topics' section in configuration.")

        broker_keys = set(config_dict['broker'].keys())
        if not required_broker_keys.issubset(broker_keys):
            missing_keys = required_broker_keys - broker_keys
            raise ValueError(f"Missing keys in 'broker' section: {missing_keys}")

        topics_keys = set(config_dict['topics'].keys())
        if not required_topics_keys.issubset(topics_keys):
            missing_keys = required_topics_keys - topics_keys
            raise ValueError(f"Missing keys in 'topics' section: {missing_keys}")

        # Validate that publishers and subscribers are lists
        if not isinstance(config_dict['topics']['publishers'], list):
            raise ValueError("'publishers' section must be a list.")
        if not isinstance(config_dict['topics']['subscribers'], list):
            raise ValueError("'subscribers' section must be a list.")