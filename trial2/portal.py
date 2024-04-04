from flask import Blueprint, render_template

bp = Blueprint('portal', __name__)

@bp.route('/')
def hello_flask():
    # Render the HTML template named 'home.html'
    return render_template('auth/home.html')
