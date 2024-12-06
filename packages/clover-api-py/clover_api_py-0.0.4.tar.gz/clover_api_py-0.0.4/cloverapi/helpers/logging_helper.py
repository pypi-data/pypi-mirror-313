import logging

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with a consistent configuration.

    :param name: Name of the logger.
    :return: Configured logger instance.
    """
    logging.basicConfig(
        level=logging.INFO,  # Set the log level to DEBUG
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler()],  # Output logs to the console
    )
    return logging.getLogger(name)