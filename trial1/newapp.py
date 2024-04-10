from flask import Flask
import mysql.connector
import pymysql
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
#
# Function to establish a connection to a MySQL database
def connect_to_database(host, user, password, database):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

# Function to insert data into the user_type table
def insert_user_type(connection, user_id, user_type_name):
    cursor = connection.cursor()
    insert_query = "INSERT INTO user_type (user_id, user_type_name) VALUES (%s, %s)"
    cursor.execute(insert_query, (user_id, user_type_name))
    connection.commit()
    cursor.close()

@app.route('/')
def hello_flask():
    return render_template('auth/home.html')
# Route for the login page
@app.route('/login')
def login():
    return render_template('auth/index1.html')

# Route for the register page
@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/insert')
def insert_data():
    # Connect to each database
    connection1 = connect_to_database('localhost', 'root', 'Mysql@123', 'db1')
    connection2 = connect_to_database('localhost', 'root', 'Mysql@123', 'db2')
    connection3 = connect_to_database('localhost', 'root', 'Mysql@123', 'db3')
    connection4 = connect_to_database('localhost', 'root', 'Mysql@123', 'db4')

    # Insert data into each database
    #insert_user_type(connection1, 1, 'Job Seeker')
    insert_user_type(connection1, 3, 'Neutral')
    # Close connections
    connection1.close()
    connection2.close()
    connection3.close()
    connection4.close()

    return 'Data inserted successfully!'
    

if __name__ == '__main__':
    app.run(debug=True)
