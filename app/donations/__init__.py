from flask import Blueprint

bp = Blueprint('donation', __name__)

from app.donations import routes
