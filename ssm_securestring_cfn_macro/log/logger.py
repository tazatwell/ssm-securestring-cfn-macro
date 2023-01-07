"""
logger
    Function to log information during lambda execution
"""

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def add_log(debug, msg):    # pragma: no cover
    """Create log with message"""
    if debug:
        logger.info(msg)
