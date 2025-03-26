# app/utils/logger.py

import logging
import sys

# Set the basic logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)

# Create a global logger instance
logger = logging.getLogger("hubspot-api")
