import logging

def get_logger(log_file="app.log"):
    # Configure logger
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger()
    logger.info("Logger initialized successfully.")
    return logger
