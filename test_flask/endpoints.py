# import libraries
from flask import Flask

# creating flask app
app = Flask(__name__)


@app.route("/")
def happy_birthday():
    return {
        "date": "20/02/2024",
        "user": "Abigail",
        "major": "Computer Science",
        "year_group": "2024",
        "event": "birthday",
        "task": "wish",
        "message": "happy birthday, Abigail",
        "^_^": "*_*"
    }