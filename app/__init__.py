from flask import Flask
from flask_dance.contrib.google import make_google_blueprint, google
from config import Config
import os
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    google_bp = make_google_blueprint(
        client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
        client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
        redirect_to='main.dashboard'  # Ensure this is 'main.dashboard'
    )
    app.register_blueprint(google_bp, url_prefix='/login')

    from . import routes
    app.register_blueprint(routes.bp)

    @app.context_processor
    def inject_google():
        return dict(google=google)

    return app