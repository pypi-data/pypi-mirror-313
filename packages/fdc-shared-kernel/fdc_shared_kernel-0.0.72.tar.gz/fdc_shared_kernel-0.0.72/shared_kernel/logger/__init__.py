import logging
import os
import json
from shared_kernel.config import Config
from shared_kernel.utils.thread_local_util import ThreadLocalStorage
class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter to structure log records as JSON.
    """

    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "name": record.name,
            "filename": record.filename,
            "module": record.module,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # Get meta_data if present
        meta_data = getattr(record, 'meta_data', {})

        # Check if 'type' is in meta_data and is 'distributed_trace'
        if meta_data.get("type") == "distributed_trace":
            thread_context = ThreadLocalStorage.get_all()
            # Add each data from thread local storage
            log_record["trace_id"] = thread_context.get("trace_id")
            log_record["span_id"] = thread_context.get("span_id")
            log_record["org_id"] = thread_context.get("org_id")
            log_record["event_name"] = thread_context.get("event_name")
            log_record["event_payload"] = thread_context.get("event_payload")
            log_record.update(meta_data)
        if hasattr(record, 'meta_data'):
            log_record.update(record.meta_data)
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)
class Logger:
    """
    A singleton logger class that ensures only one logger instance is created.
    This logger supports both console and file logging.

    Attributes:
        _instance (Optional[Logger]): The single instance of the logger.
    """

    _instance = None

    def __new__(cls, name=None):
        """
        override __new__ to ensure singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(name=name)
        return cls._instance

    def _initialize(self, name=None, log_file: str = "fdc_app_logs.log", json_log_file: str = "fdc_app_logs.jsonl"):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(filename)s - %(module)s - %(levelname)s - %(message)s"
        )
        self.log_file = log_file
        self.json_log_file = json_log_file

        # ensure handlers are configured only once
        if not self.logger.handlers:
            self.configure_logger()

    def configure_logger(self):
        """
        Configures logger with stream and file handlers.
        """
        self.add_stream_handler()
        self.add_file_handler(log_file=self.log_file)
        self.add_json_file_handler(log_file=self.json_log_file)

    def add_stream_handler(self):
        """
        Adds a stream handler to the logger.
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.logger.level)
        app_config = Config()
        mode = app_config.get("MODE")
        if mode == "PROD":
            stream_handler.setFormatter(JSONFormatter())
        else:
            stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

    def add_file_handler(self, log_file, log_directory="./logs"):
        """
        Adds a file handler to the logger.
        """
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        file_handler = logging.FileHandler(os.path.join(log_directory, log_file))
        file_handler.setLevel(self.logger.level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
    
    def add_json_file_handler(self, log_file, log_directory="./logs"):
        """
        Adds a JSON file handler to the logger.
        """
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        json_file_handler = logging.FileHandler(os.path.join(log_directory, log_file))
        json_file_handler.setLevel(self.logger.level)
        json_file_handler.setFormatter(JSONFormatter())  # Using the custom JSON formatter
        self.logger.addHandler(json_file_handler)

    def info(self, message, *args, **kwargs):
        meta_data = {"meta_data": kwargs}
        self.logger.info(message, *args, extra=meta_data, stacklevel=2)

    def error(self, message, *args, **kwargs):
        meta_data = {"meta_data": kwargs}
        self.logger.error(message, exc_info=True, *args, extra=meta_data, stacklevel=2)

    def debug(self, message, *args, **kwargs):
        meta_data = {"meta_data": kwargs}
        self.logger.debug(message, *args, extra=meta_data, stacklevel=2)

    def warning(self, message, *args, **kwargs):
        meta_data = {"meta_data": kwargs}
        self.logger.warning(message, *args, extra=meta_data, stacklevel=2)
