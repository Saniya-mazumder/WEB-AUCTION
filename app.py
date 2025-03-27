from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
  # Allow frontend to communicate with backend

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
        return jsonify({"success": True, "message": "Login successful", "role": user_type}), 201
    except mysql.connector.Error as err:
        return jsonify({"success": False, "error": str(err)}), 400

# Login user
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    cursor.execute("SELECT password, user_type FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[0], password):
        return jsonify({"success": True, "message": "Login successful", "role": user[1]}), 200
    else:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    product_name = data['product_name']
    quantity = data['quantity']
    price = data['price']
    address = data['address']
    phone = data['phone']
    duration = data['duration']
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO auction_items (product_name, quantity, price, address, phone, duration)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_name, quantity, price, address, phone, duration))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Item added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch Active Auction Items
@app.route('/get-items', methods=['GET'])
def get_items():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, product_name, quantity, price, duration FROM auction_items")
        items = cur.fetchall()
        cur.close()
        
        item_list = [{"id": item[0], "name": item[1], "quantity": item[2], "price": item[3], "duration": item[4]} for item in items]
        return jsonify(item_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch Buyers
@app.route('/get-buyers', methods=['GET'])
def get_buyers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE user_type = 'buyer'")
        buyers = cur.fetchall()
        cur.close()
        
        buyer_list = [buyer[0] for buyer in buyers]
        return jsonify(buyer_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Place a Bid
@app.route('/place-bid', methods=['POST'])
def place_bid():
    try:
        data = request.json
        item_id = data['item_id']
        new_price = data['new_price']
        bidder = data['bidder']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE auction_items SET price = %s, highest_bidder = %s WHERE id = %s", (new_price, bidder, item_id))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": "Bid placed successfully!", "new_price": new_price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Approve Bid (Seller finalizing the auction)
@app.route('/approve-bid', methods=['POST'])
def approve_bid():
    try:
        data = request.json
        item_id = data['item_id']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT highest_bidder FROM auction_items WHERE id = %s", (item_id,))
        highest_bidder = cur.fetchone()[0]
        
        if not highest_bidder:
            return jsonify({"error": "No bids to approve"}), 400
        
        cur.execute("UPDATE auction_items SET status = 'sold' WHERE id = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": "Bid approved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
