from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)  # Allow frontend to communicate with backend

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="auction_system"
)
cursor = db.cursor()

# Register a new user
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user_type = data["user_type"]

    try:
        cursor.execute("INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)", (username, password, user_type))
        db.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

# Login user
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[0], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
