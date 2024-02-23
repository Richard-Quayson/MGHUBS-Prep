# import libraries
from flask import Flask, jsonify, request
import sqlite3

# create the flask app
app = Flask(__name__)


# connect to db
def db_connection():
    conn = sqlite3.connect("users.db")
    return conn


@app.route("/user/create", methods=["POST"])
def create_user():

    # collect form data
    data = request.get_json()
    firstname = data.get("first_name")
    lastname = data.get("last_name")
    email = data.get("email")

    # establish database connection
    connection = db_connection()

    # create the cursor for the db execution
    cursor = connection.cursor()

    # write the query
    query = """INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?) RETURNING id"""
    cursor.execute(query, (firstname, lastname, email))
    result = cursor.fetchone()

    # commit the change
    connection.commit()

    # close the connection
    connection.close()

    return jsonify({"id": result[0]})


if __name__ == "__main__":
    app.run(debug=True)