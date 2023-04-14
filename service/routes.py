
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.common import status  # HTTP Status Codes
from service.models import TankCommand
from . import app  # Import Flask application

@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK

@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Tank REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )

@app.route("/execute", methods=["POST"])
def move_tank():
    """Execute a TankCommand"""
    check_content_type("application/json")
    command = TankCommand()
    command.deserialize(request.get_json())
    # try to execute the command here...
    
    command.clear()
    command.status = "Executed"
    reply = command.serialize()
    app.logger.debug(reply)
    location_url = "/execute"
    return make_response(
        jsonify(reply), status.HTTP_202_ACCEPTED, {"Location": location_url}
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )

