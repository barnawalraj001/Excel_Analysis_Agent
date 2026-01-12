import logging

def setup_logger(name: str):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger("excel_analysis_agent")
