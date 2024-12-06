from .factory import Loggable, LoggerFactory
from .modifier import LoggingModifier
from .tools import get_timestamp, mute, to_sci_notation


import logging
class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL