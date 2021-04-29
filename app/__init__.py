# import Flask class
from flask import Flask

# definition of Flask object called app
app = Flask(__name__)

# import of routings
from app import routes

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port = 8081)
