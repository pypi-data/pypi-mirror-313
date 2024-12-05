# my_lambda_lib/common_utils.py

import json
import logging

def setup_logging(log_level=logging.INFO):
    """Configura o logger padrão."""
    logging.basicConfig(level=log_level)
    logger = logging.getLogger()
    logger.setLevel(log_level)
    return logger

def parse_json(event):
    """Parseia um evento JSON e retorna o dicionário correspondente."""
    try:
        return json.loads(event)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
