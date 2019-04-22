# We create the authentication Blueprint
from flask import Blueprint
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.contrib.google import make_google_blueprint, google


googlex = make_google_blueprint(
    client_id="367107748382-6kasp2tp3gd2977lnr4hp8m65hhdrt0t.apps.googleusercontent.com",
    client_secret="AGfnbTqHOzigfabBDpmKFMmg",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email"
    ]
)

bp = Blueprint('auth', __name__)

batman_example = OAuth2ConsumerBlueprint(
    "batman-example", __name__,
    client_id="268153730556085",
    client_secret="558802d57cf1253b7d55e3d1591a2a61",
    base_url="https://graph.facebook.com",
    authorization_url="https://www.facebook.com/dialog/oauth",
    token_url="https://graph.facebook.com/oauth/access_token",
)

from . import routes
from ..models import Permission


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
