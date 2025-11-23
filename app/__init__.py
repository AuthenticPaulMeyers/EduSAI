from flask import Flask, jsonify
import os
from .schema.models import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from .constants.http_status_codes import HTTP_429_TOO_MANY_REQUESTS, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv(override=True)

# Config flask limiter for AI endpoints
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    )

# config cors
cors = CORS()

# initiate app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # initialise CORS
    cors.init_app(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["https://console.twilio.com/us1/develop/sms/try-it-out/send-an-sms", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
            JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    # initialise the database here
    db.app=app
    db.init_app(app)

    # Initialise flask rate limiter
    limiter.init_app(app)
    
    # initialise migrations
    Migrate(app, db)

    # import more blueprints here
    from .routes.sms import sms_bp

    # configure blueprints here
    app.register_blueprint(sms_bp)

    # exception handling | catch runtime errors here
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_file_not_found(error):
        return jsonify({'error': f"{HTTP_404_NOT_FOUND} File not found!"}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_internalServer_error(error):
        return jsonify({'error': "Something went wrong!"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    @app.errorhandler(HTTP_503_SERVICE_UNAVAILABLE)
    def handle_connection_error(error):
        return jsonify({'error': "Service is currently unavailable. Our team is working on it!"}), HTTP_503_SERVICE_UNAVAILABLE
    
    @app.errorhandler(HTTP_429_TOO_MANY_REQUESTS)
    def handle_too_may_requests_error(error):
        return jsonify({'error': 'Too many requests. Please try again later.'}), HTTP_429_TOO_MANY_REQUESTS
    
    # Kill inactive database sessions
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app