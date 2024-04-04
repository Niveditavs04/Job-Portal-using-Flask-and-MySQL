import functools
import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


from trial2.models import Model1
#don't write anything here
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        date_of_birth = request.form.get('date_of_birth')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms_accepted = 'terms' in request.form  # Checkbox value
        user_type = request.form.get('userType')
        gender = request.form.get('usergender')
        print(password)

        # Optional fields
        email_notification = 'emailNotification' in request.form
        sms_notification = 'smsNotification' in request.form
        profile_picture = request.files.get('profilePicture')  # File upload

        # Process the form data
        error = None

        if error is None:
            try:
                model1 = Model1()

                # Establish the database connection
                model1.connect(host='localhost', user='root', password='Mysql@123', database='db1')

                # Now you can get a cursor
                cursor = model1.get_cursor()
                cursor.execute("SELECT MAX(id) FROM user_account")
                max_id = cursor.fetchone()[0]
                new_id = max_id + 1 if max_id is not None else 1
                print("from databse",new_id)

                # Process the selected user type based on your application logic
                user_type_id = 1 if user_type == 'seeker' else 2 if user_type == 'employer' else 3
                cursor.execute(
                      "INSERT INTO user_account (id,user_type_id,email,password,date_of_birth,gender,registration_date) VALUES (%s, %s, %s, %s, %s, %s, CURDATE())",
                      (new_id, user_type_id, email, generate_password_hash(password), date_of_birth, gender)
                             )


                model1.connection.commit()
                  

               

            except mysql.connector.IntegrityError as e:
                error = f"User {email} is already registered. ({e})"
                flash(error)
            finally:
                cursor.close()  # Close the cursor
        
        return redirect(url_for("user.login"))
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        model1 = Model1()

        # Establish the database connection
        model1.connect(host='localhost', user='root', password='Mysql@123', database='db1')

        # Now you can get a cursor
        cursor = model1.get_cursor()
        error = None

        # Execute the query with the correct parameter passing
        cursor.execute(
            'SELECT id, email, password FROM user_account WHERE email = %s', (username,)
        )
        
        # Fetch the user data
        user = cursor.fetchone()
        #print(check_password_hash(user[2], password))

        cursor.close()

        if user is None:
            error = 'Incorrect username.'
        else:
            if not check_password_hash(user[2], password):
                error = 'Incorrect password.'

            else:
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('hello_flask'))

        flash(error)

    return render_template('auth/index1.html')




@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        model1 = Model1()

        # Establish the database connection
        model1.connect(host='localhost', user='root', password='Mysql@123', database='db1')

        # Now you can get a cursor
        cursor = model1.get_cursor()
        cursor.execute(
            'SELECT email FROM user_account WHERE id = %s', (user_id,)
        )  # Using %s placeholder instead of ?
        g.user = cursor.fetchone()
        cursor.close()
