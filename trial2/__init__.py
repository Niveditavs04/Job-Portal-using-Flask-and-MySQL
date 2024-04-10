from flask import Flask

#from trial2 import db
from trial2.models import Model1, Model2 ,Model3, Model4
#import mysql.connector
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = 'Job portal for dbms project' # imp else will get RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
    
    # Configuration for your databases
    
    # Initialize the Flask application with the database
    #db.init_app(app)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import portal
    app.register_blueprint(portal.bp)
    app.add_url_rule('/', endpoint='hello_flask')

    from . import user
    app.register_blueprint(user.bp)

    from . import seeker
    app.register_blueprint(seeker.bp)

    from . import employer
    app.register_blueprint(employer.bp)
    
    if __name__ == "__main__":
        app.run(debug=True)

    # Return the Flask app instance
    return app
