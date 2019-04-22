from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import User, Post, Follow, Comment, Role, Permission, Notification, Message
from flask_migrate import upgrade, Migrate


app = create_app()  
app.run(debug=True)
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment, Notification= Notification, Message=Message)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
