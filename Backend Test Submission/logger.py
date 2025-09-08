import logging
from flask import request
from datetime import datetime

def setup_logger():
    logger = logging.getLogger("url_shortener")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger()

def logging_middleware(app):
    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.path} at {datetime.utcnow().isoformat()}Z")
