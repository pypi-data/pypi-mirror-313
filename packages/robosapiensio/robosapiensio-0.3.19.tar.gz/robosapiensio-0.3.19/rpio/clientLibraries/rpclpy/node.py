import yaml
import logging
from rpio.clientLibraries.rpclpy.event_handler import EventHandler
from rpio.clientLibraries.rpclpy.knowledge import KnowledgeManager

class Node:
    def __init__(self, config, verbose = False):
        self.config = self.load_config(config)
        self.logger = self.initialize_logger()
        self.knowledge = self.initialize_knowledge()  # Initialize knowledge within the component
        self.event_handler = self.initialize_event_handler()  # Initialize Event manager
        
        

        # Initialize MQTT and ROS2 Event
        if self.event_handler:
            self.logger.info(f"{self.__class__.__name__} is using Event Manager")

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def initialize_logger(self):
        """Initialize the logger (same as before)."""
        log_config = self.config.get("logging", {})
        logger = logging.getLogger(self.__class__.__name__)
        log_level = log_config.get("level", "INFO").upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

        log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        log_file = log_config.get("file", None)
        
        formatter = logging.Formatter(log_format)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def initialize_knowledge(self):
        """Initialize the Knowledge object based on the config."""
        self.logger.info(f"Initializing Knowledge: {self.config['knowledge_config']['storage_type']} knowledge")
        return KnowledgeManager(self.config['knowledge_config'])

    def initialize_event_handler(self):
        """Initialize the Event Manager based on the config."""
        self.logger.info("Initializing Event Manager")
        return EventHandler(self.config, self.knowledge, self.logger)

    def start(self):
        """Start the component and enable Event."""
        self.logger.info(f"{self.__class__.__name__} is starting...")
        if self.event_handler:
            self.event_handler.start()

    def shutdown(self):
        """Shutdown the component and stop Event."""
        self.logger.info(f"{self.__class__.__name__} is shutting down...")
        if self.event_handler:
            self.event_handler.shutdown()

    def publish_event(self, event_key, message = True):
        """Publish Event using the Event manager."""
        if self.event_handler:
            self.event_handler.send(event_key, message)
        else:
            self.logger.warning("Event manager is not set for Event publishing.")


    def register_event_callback(self, event_key, callback):
        """Register a callback for Event manager events (MQTT or Redis)."""
        if self.event_handler:
            self.event_handler.subscribe(event_key, callback)
            self.logger.info(f"Registered callback for event: {event_key}")
        else:
            self.logger.warning("Event manager is not set for registering event callbacks.")
