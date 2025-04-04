from flask import Flask, request, jsonify, g
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector
import logging

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500", "methods": ["GET", "POST"]}})  # Allow frontend to communicate with backend

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to get a fresh database connection
def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="auction_db"
        )
        return db
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

# Create a new connection and cursor before each request
@app.before_request
def before_request():
    # Open a new database connection before every request
    g.db = get_db_connection()
    if g.db:
        g.cursor = g.db.cursor()
    else:
        logging.error("Database connection failed, cannot proceed with request.")

# Close the connection after each request
@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'db') and g.db:
        g.cursor.close()  # Close cursor
        g.db.close()      # Close database connection

# Register a new user
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user_type = data["user_type"]

    try:
        # Insert user into database
        g.cursor.execute("INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)", (username, password, user_type))
        g.db.commit()
        return jsonify({"success": True, "message": "User registered successfully", "role": user_type}), 201
    except mysql.connector.Error as err:
        logging.error(f"Error while registering user: {err}")
        return jsonify({"success": False, "error": str(err)}), 400

# Login user
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    try:
        g.cursor.execute("SELECT password, user_type FROM users WHERE username = %s", (username,))
        user = g.cursor.fetchone()

        if user and bcrypt.check_password_hash(user[0], password):
            g.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = g.cursor.fetchone()[0]
            response = jsonify({
                "success": True, 
                "message": "Login successful", 
                "role": user[1], 
                "user_id": user_id,
                "username": username 
            })
            return response, 200
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

# Add Item to Auction (Updated)
@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    product_name = data['product_name']
    quantity = data['quantity']
    price = data['price']
    address = data['address']
    phone = data['phone']
    duration = data['duration']
    username = data['username']  # Get the seller's username
    
    try:
        # Get the seller's ID
        g.cursor.execute("SELECT id FROM users WHERE username = %s AND user_type = 'seller'", (username,))
        seller_result = g.cursor.fetchone()
        
        if not seller_result:
            return jsonify({"error": "Seller not found or user is not a seller"}), 404
        
        seller_id = seller_result[0]
        
        query = """
            INSERT INTO auction_items (product_name, quantity, price, address, phone, duration, created_at, seller_id)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        g.cursor.execute(query, (product_name, quantity, price, address, phone, duration, seller_id))
        g.db.commit()

        return jsonify({"message": "Item added successfully!"}), 200
    except Exception as e:
        logging.error(f"Error while adding item: {str(e)}")
        return jsonify({"error": "Failed to add item"}), 500

# Fetch Active Auction Items
@app.route('/get-items', methods=['GET'])
def get_items():
    try:
        g.cursor.execute("SELECT id, product_name, quantity, price, duration FROM auction_items")
        items = g.cursor.fetchall()
        
        item_list = [{"id": item[0], "name": item[1], "quantity": item[2], "price": item[3], "duration": item[4]} for item in items]
        return jsonify(item_list)
    except Exception as e:
        logging.error(f"Error fetching items: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Fetch Buyers
@app.route('/get-buyers', methods=['GET'])
def get_buyers():
    try:
        g.cursor.execute("SELECT username FROM users WHERE user_type = 'buyer'")
        buyers = g.cursor.fetchall()
        
        buyer_list = [buyer[0] for buyer in buyers]
        return jsonify(buyer_list)
    except Exception as e:
        logging.error(f"Error fetching buyers: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Approve Bid (Seller finalizing the auction)
@app.route('/approve-bid', methods=['POST'])
def approve_bid():
    try:
        data = request.json
        item_id = data['item_id']
        
        g.cursor.execute("SELECT highest_bidder FROM auction_items WHERE id = %s", (item_id,))
        highest_bidder = g.cursor.fetchone()[0]
        
        if not highest_bidder:
            return jsonify({"error": "No bids to approve"}), 400
        
        g.cursor.execute("UPDATE auction_items SET status = 'sold' WHERE id = %s", (item_id,))
        g.db.commit()
        
        return jsonify({"message": "Bid approved successfully!"})
    except Exception as e:
        logging.error(f"Error approving bid: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Get Past Bought Items for a User
@app.route('/past-bought-items', methods=['GET'])
def past_bought_items():
    try:
        username = request.args.get('username')
        if not username:
            return jsonify({"error": "Username is required"}), 400
            
        # First, get the user_id from the username
        g.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_result = g.cursor.fetchone()
        
        if not user_result:
            return jsonify({"error": "User not found"}), 404
            
        user_id = user_result[0]
        
        # Query to get items that have been purchased by this user
        query = """
            SELECT ai.product_name, ai.price, ai.quantity, ai.updated_at as purchase_date
            FROM auction_items ai
            WHERE ai.status = 'sold' AND ai.highest_bidder = %s
        """
        g.cursor.execute(query, (user_id,))
        items = g.cursor.fetchall()
        
        item_list = [
            {
                "product_name": item[0], 
                "price": item[1], 
                "quantity": item[2], 
                "purchase_date": item[3].isoformat() if item[3] else None
            } 
            for item in items
        ]
        
        return jsonify(item_list)
    except Exception as e:
        logging.error(f"Error fetching past bought items: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Place a Bid
@app.route('/place-bid', methods=['POST'])
def place_bid():
    try:
        data = request.json
        item_id = data['item_id']
        new_price = data['new_price']
        bidder_username = data['bidder']
        
        # First, get the user_id from the username
        g.cursor.execute("SELECT id FROM users WHERE username = %s", (bidder_username,))
        user_result = g.cursor.fetchone()
        
        if not user_result:
            return jsonify({"error": "Bidder not found"}), 404
        
        bidder_id = user_result[0]  # Get the numeric ID
        
        # Now update the auction item with the numeric ID
        g.cursor.execute("UPDATE auction_items SET price = %s, highest_bidder = %s WHERE id = %s", 
                        (new_price, bidder_id, item_id))
        g.db.commit()
        
        return jsonify({"message": "Bid placed successfully!", "new_price": new_price})
    except Exception as e:
        logging.error(f"Error placing bid: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Get Past Sold Items for a Seller
@app.route('/past-sold-items', methods=['GET'])
def past_sold_items():
    try:
        username = request.args.get('username')
        if not username:
            return jsonify({"error": "Username is required"}), 400
            
        # First, get the user_id from the username
        g.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_result = g.cursor.fetchone()

        if not user_result:
            return jsonify({"error": "User not found"}), 404
            
        user_id = user_result[0]
        
        # Query to get items that have been sold by this user
        query = """
            SELECT ai.id, ai.product_name, ai.price, ai.quantity, ai.updated_at as sold_date,
                   u.username as buyer_username
            FROM auction_items ai
            LEFT JOIN users u ON ai.highest_bidder = u.id
            WHERE ai.status = 'sold' AND ai.seller_id = %s
            ORDER BY ai.updated_at DESC
        """
        g.cursor.execute(query, (user_id,))
        items = g.cursor.fetchall()
        
        item_list = []
        for item in items:
            item_data = {
                "id": item[0],
                "product_name": item[1],
                "price": item[2],
                "quantity": item[3],
                "sold_date": item[4].isoformat() if item[4] else None,
                "buyer": item[5] if item[5] else "Unknown"
            }
            item_list.append(item_data)
        return jsonify(item_list)
    except Exception as e:
        logging.error(f"Error fetching past sold items: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
