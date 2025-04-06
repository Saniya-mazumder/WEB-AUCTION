# WEB AUCTION SYSTEM 🛒

A full-stack web application built with **Flask**, **MySQL**, **HTML**, **CSS**, and **JavaScript**, designed for seamless online auction experiences. Sellers can list items, buyers can bid and purchase, and both users can track their activities through dynamic dashboards.

---

### 🧠 Overview of the Solution

The **Web Auction System** provides a platform where:
- **Sellers** can list products for auction.
- **Buyers** can place bids and purchase items.
- Real-time auction durations, bidding history, and transaction tracking are implemented using Flask as the backend and MySQL as the database.
- The front end is built with HTML, CSS, and JavaScript, delivering an intuitive and responsive UI.

---

### ✅ Features Implemented

- **User Authentication**: Secure login/signup for buyers and sellers.
- **Role-Based Dashboards**: Different interfaces and options based on user role.
- **Auction Listing**: Sellers can post items for auction with descriptions, prices, and time durations.
- **Live Bidding**: Buyers can place bids on active products.
- **Purchase Tracking**:
  - Sellers can view all items they listed and their auction status.
  - Buyers can track their purchased items.
- **Admin Panel** (coming soon): View site-wide stats and control features.

---

### ⚙️ Technical Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Package**: `mysql-connector-python`
- **IDE**: Visual Studio Code

---

### 🧑‍💻 Setup Instructions

#### 1. Clone the Repository
git clone https://github.com/Saniya-mazumder/WEB-AUCTION.git

#### 2️. Open the Project in VS Code  
Navigate to the project folder and open it in VS Code:  

cd WEB-AUCTION  
code .

-------------------------------------------------------

🔧 Install Dependencies  

#### 3️. Install MySQL Connector  
In VS Code, open the PowerShell terminal and run:  

pip install mysql-connector-python  

Wait for the installation to complete successfully.  

-------------------------------------------------------

#### 4.  Run the Flask Server  

 Start the Backend  
- Locate app.py in the project folder.  
- Click on it to open the file.  
- Run the script by clicking Run in VS Code or by executing:  

python app.py  

✅ The Flask server will now turn on and start handling authorization requests.  

-------------------------------------------------------

 #### 5. Launch the Web Application  

5️⃣ Open the Website with Live Server  
- In VS Code, right-click on welcome.html.  
- Select "Open with Live Server".  
#### 6. Import SQL Files into MySQL
# ---------------------------------------

Make sure MySQL is installed and running

🛠️ Create database (optional if not already created)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS auction_system;"

 📥 Import the complete schema (includes users, auction_items, and purchase_requests)
mysql -u root -p auction_system < export.sql

OR import only auction_items table
 mysql -u root -p auction_system < auction_items.sql

✅ SQL tables will now be available in the auction_system DB


🔹 If you don’t see "Go Live," install the Live Server extension from the VS Code Extensions Marketplace.  

-------------------------------------------------------

📌 Notes  
- Ensure MySQL is installed and running before using the platform.  
- If you face any issues, try restarting VS Code and repeating the steps.
- Make sure MySQL is in your system PATH or use full path to mysqldump/mysql commands
- If errors occur, restart VS Code or recheck installation steps
- You can manage SQL with MySQL Workbench, phpMyAdmin, or CLI

Enjoy your Web Auction System! 🚀
