import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import Config, ProductionConfig
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from flask_moment import Moment
from flask_ckeditor import CKEditor

db = SQLAlchemy()
ckeditor=CKEditor()
migrate = Migrate()
bcrypt = Bcrypt()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'






def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'




    db.init_app(app)
    ckeditor.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)



    from .users import bp as user_bp
    
    from .auth import bp as auth_bp
    from .auth import batman_example as batman_example
    from .auth import googlex as googlex
    
    from .errors import bp as errors_bp
    from .visualization import bp as visualization_bp
    from .main import bp as main_bp    
    from .donations import bp as donation_bp    
    
 
    app.register_blueprint(batman_example, url_prefix='/login')
    app.register_blueprint(googlex, url_prefix='/loginx')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')    
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(visualization_bp, url_prefix='/visualization')    
    app.register_blueprint(donation_bp, url_prefix='/donation')    


    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app
