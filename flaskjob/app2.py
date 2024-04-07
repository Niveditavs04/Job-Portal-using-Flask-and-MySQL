from flask import Flask

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app if it's executed directly
