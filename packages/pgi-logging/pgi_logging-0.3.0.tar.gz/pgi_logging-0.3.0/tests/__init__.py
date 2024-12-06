import pgi_logging

# Create a logger for testing
logger = pgi_logging.base_default_logger(
    "test_logger",
    None,
    None,
    pgi_logging.pgi_handlers.LoggerLevel.DEBUG,
    True,
    True,
)
