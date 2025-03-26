from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change if necessary
app.config['MYSQL_PASSWORD'] = 'yourpassword'  # Change if necessary
app.config['MYSQL_DB'] = 'auction_db'

mysql = MySQL(app)

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

if __name__ == '__main__':
    app.run(debug=True)
