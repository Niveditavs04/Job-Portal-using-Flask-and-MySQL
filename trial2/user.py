import functools
import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


from trial2.models import Model1,Model2
#don't write anything here
bp = Blueprint('user', __name__, url_prefix='/user')
# Create a global variable to hold the database connection
model1 = Model1()
model1.connect(host='localhost', user='root', password='Mysql@123', database='db1')
model4 = Model2()
model4.connect(host='localhost', user='root', password='Mysql@123', database='db4')


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
                

                # Now you can get a cursor
                cursor = model1.get_cursor()
                cursor.execute("SELECT MAX(id) FROM user_account")
                max_id = cursor.fetchone()[0]
                new_id = max_id + 1 if max_id is not None else 1
                print("from databse",new_id)

                # Process the selected user type based on your application logic
                user_type_id = 1 if user_type == 'seeker' else 2 if user_type == 'employer' else 3
                cursor.execute(
                      "INSERT INTO user_account (id,user_type_id,email,password,date_of_birth,gender,user_image,registration_date) VALUES (%s, %s, %s, %s, %s, %s,%s, CURDATE())",
                      (new_id, user_type_id, email, generate_password_hash(password), date_of_birth, gender,profile_picture)
                             )
                cursor.execute("INSERT INTO user_log (useraccount_id,last_login_date) VALUES (%s, NOW())",
                      (new_id,))


                model1.commit()
                  

               

            except mysql.connector.IntegrityError as e:
                error = f"User {email} is already registered. ({e})"
                flash(error)
            finally:
                cursor.close()  # Close the cursor
        
        return redirect(url_for("user.login"))
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    candidate_logged_in = False
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
       
        # Now you can get a cursor
        cursor = model1.get_cursor()
        error = None

        # Execute the query with the correct parameter passing
        cursor.execute(
            'SELECT id, email, password ,user_type_id FROM user_account WHERE email = %s', (username,)
        )
        
        # Fetch the user data
        user = cursor.fetchone()
        #print(check_password_hash(user[2], password))

        

        if user is None:
            error = 'Incorrect username.'
        else:
            if not check_password_hash(user[2], password):
                error = 'Incorrect password.'

            else:
                session.clear()
                session['user_id'] = user[0]
                candidate_logged_in = True  # Set this based on authentication status
                cursor.execute('UPDATE user_log SET last_login_date = NOW()  WHERE useraccount_id = %s', ( user[0],))
                model1.commit()
                cursor.close()

                
                
                if(user[3]==1):
                    return redirect(url_for('seeker.generalseek'))
                elif(user[3]==2):
                    cursor4= model4.get_cursor()
                    cursor4.execute("SELECT pid FROM job_post where posted_by=%s", (user[0],))

                    jpid = [result[0] for result in cursor4.fetchall()]
                    cursor4.close()
                    if jpid:
                        return redirect(url_for('employer.dashemp'))
                    else:
                    # Redirect employer to job posting page
                        return redirect(url_for('employer.generale'))
                else:
                    return redirect(url_for('hello_flask'))


        flash(error)

    return render_template('auth/index1.html')

@bp.route('/forgotpassword', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['password']  # Get the new password from the form
       
        # Now you can get a cursor
        cursor = model1.get_cursor()
        error = None

        # Check if the email exists in the database
        cursor.execute(
            'SELECT id FROM user_account WHERE email = %s', (email,)
        )
        user = cursor.fetchone()

        if user is None:
            error = 'Email does not exist.'
        else:
            # Update the password for the user
            hashed_password = generate_password_hash(new_password)
            cursor.execute(
                'UPDATE user_account SET password = %s WHERE email = %s', (hashed_password, email)
            )
            model1.commit()  # Commit the transaction
            cursor.close()

            flash('Password reset successful.')

            return redirect(url_for('user.login'))

        flash(error)

    return render_template('auth/forgotpass.html')




@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cnx = mysql.connector.connect(user='root', password='Mysql@123',
                                  host='localhost')
        # Now you can get a cursor
        cursor = cnx.cursor()
        cursor.execute(
            'SELECT id ,user_type_id ,email FROM db1.user_account WHERE id = %s', (user_id,)
        )  # Using %s placeholder instead of ?
        
        g.user = cursor.fetchone()
         # Check if user is found before attempting to update user_log
        if g.user:
            try:
                cursor.execute('UPDATE db1.user_log SET last_login_date = NOW() WHERE useraccount_id = %s', (user_id,))
                cnx.commit()
                cursor.close()
            except Exception as e:
                print("Error while updating last login date:", e)
                # Rollback the transaction if an error occurs
                cnx.rollback()
        else:
            # Handle the case where the user is not found
            pass

        
        

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello_flask'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view
