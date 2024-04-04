from flask import current_app, g
from trial2.models import Model1, Model2, Model3,Model4

def init_app(app):
    # Perform any database initialization/configuration here if needed
    pass

def get_db(db_key):
    # Get the appropriate database based on the key
    if db_key == 'db1':
        return Model1()
    elif db_key == 'db2':
        return Model2()
    elif db_key == 'db3':
        return Model3()
    elif db_key == 'db4':
        return Model4()
    # Add more databases as needed...

    # If the database key is invalid, return None
    return None
