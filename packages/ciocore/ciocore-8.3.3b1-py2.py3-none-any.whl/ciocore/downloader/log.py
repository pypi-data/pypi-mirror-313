import logging
import colorlog
import sys
LOGGER_NAME = "cw.download"

LOG_COLORS	={
		'DEBUG':    'purple',
		'INFO':     'blue',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
}

DEBUG_FORMATTER = colorlog.ColoredFormatter(
	"%(log_color)s%(asctime)s %(name)s %(levelname)8s %(filename)s:%(lineno)d %(threadName)s> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors=LOG_COLORS,
 )

INFO_FORMATTER = colorlog.ColoredFormatter(
	'%(log_color)s%(levelname)s:%(name)s> %(message)s',
    log_colors=LOG_COLORS,
)

LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "NOTSET": logging.NOTSET,
}

class GracefulLogger(logging.Logger):
    def setLevel(self, level):
        super().setLevel(level)

        # Define formatters based on level
        formatter = DEBUG_FORMATTER if level == logging.DEBUG else INFO_FORMATTER
        for handler in self.handlers:
            handler.setFormatter(formatter)
            

class GracefulStreamHandler(colorlog.StreamHandler):
    """
    A custom StreamHandler that suppresses BrokenPipeError.
    
    This handler extends the standard logging.StreamHandler to gracefully handle 
    BrokenPipeErrors that can occur when output streams are closed prematurely. 
    It overrides the emit method to catch and ignore BrokenPipeError, allowing 
    the program to continue without interruption.
    """
 
    def emit(self, record):
        """
        Overrides the StreamHandler.emit method to gracefully handle BrokenPipeError.

        Args:
            record (logging.LogRecord): The log record to be emitted.
        """
        try:
            super().emit(record)
        except BrokenPipeError:
            pass

logging.setLoggerClass(GracefulLogger)
logger = colorlog.getLogger(LOGGER_NAME)
logger.propagate = False 
 
if not any(isinstance(handler, GracefulStreamHandler) for handler in logger.handlers):
    stream_handler = GracefulStreamHandler(sys.stdout)
    logger.addHandler(stream_handler)
 