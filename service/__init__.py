import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)

# Set up logging
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    # "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
for handler in app.logger.handlers:
    handler.setFormatter(formatter)

from service import routes, models
from service.common import error_handlers

app.logger.info(50 * "*")
app.logger.info(" TANK SERVICE RUNNING ".center(50, "*"))
app.logger.info(50 * "*")


