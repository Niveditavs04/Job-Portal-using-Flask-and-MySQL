from flask import Flask
import pymysql

app = Flask(__name__)

def connect_to_database(host, user, password, database):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

# Function to insert data into the user_type table
def insert_user_type(connection, user_id, user_type_qname):
    cursor = connection.cursor()
    insert_query = "INSERT INTO user_type (user_id, user_type_name) VALUES (%s, %s)"
    cursor.execute(insert_query, (user_id, user_type_name))
    connection.commit()
    cursor.close()

@app.route('/insert')
def insert_data():
    # Connect to the database
    connection1 = connect_to_database('localhost', 'root', 'avishka24', 'db1')
    insert_user_type(connection1, 3, 'Neutral')
    # Close the connection
    connection1.close()

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app if it's executed directly
