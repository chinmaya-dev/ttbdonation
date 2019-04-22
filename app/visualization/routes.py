from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from datetime import datetime
from app.visualization import bp
from app.models import User, Post, Follow



@bp.route("/overview")
def overview():

    return render_template('visualization/overview.html',title='Overvew')

# Text analysis part temporary
@bp.route("/index")
def index():
	return render_template('visualization/index.html')
