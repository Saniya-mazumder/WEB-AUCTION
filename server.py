from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change if necessary
app.config['MYSQL_PASSWORD'] = '12345'  # Change if necessary
app.config['MYSQL_DB'] = 'auction_db'

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password, user_type FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return jsonify({"success": True, "message": "Login successful", "role": user[1]})
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

# New API to Fetch Auction Items
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

if __name__ == '__main__':
    app.run(debug=True)
