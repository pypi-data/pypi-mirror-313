
from SerraWatchLogger.backend import LoggerSerraWatch
Logger = LoggerSerraWatch.LoggerSerraWatch.get_instance("SerraWatch")

class TopicsConfig:
    def __init__(self, publishers: list[str], subscribers: list[str]):
        self.publishers = publishers
        self.subscribers = subscribers
        Logger.debug(self=Logger, message=f"TopicsConfig initialized")