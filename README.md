# MiniERP - Enterprise Resource Management Prototype

A **mini ERP system prototype** built using **Flask and MySQL** to simulate core business operations such as order management, inventory tracking, and billing. This project is designed as a lightweight ERP simulator with modular architecture for easy understanding and scalability.

---

## **Features**

- **Product Management**

  - Add new products with stock and price.
  - View all products in a responsive table.

- **Order Management**

  - Place orders for products with real-time stock validation.
  - Automatically update product stock after order placement.
  - Display order history with quantity, total, and status.

- **Billing**

  - Automatically generate billing entries for completed orders.

- **Responsive UI**

  - Modern, mobile-friendly dashboard using **Bootstrap**.
  - Custom CSS for better visuals and user experience.

- **Error Handling**
  - Flash messages for success, warnings, and errors (e.g., no stock available).

---

## **Tech Stack**

- **Backend:** Python 3, Flask
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap 5, CSS
- **Others:** Flask-MySQLdb, Jinja2 templates

---

## **Setup Instructions**

## 1. **Clone the repository**
```bash

git clone <your-repo-url>
cd ERP_stimulator
```

## 2. **Install Dependencies**
```
pip install -r requirements.txt
```

## 3. **Create MySQL database**
```
CREATE DATABASE erp_db;
USE erp_db;

-- Create tables
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT DEFAULT 0,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Completed',
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE billing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

## 4. **Update MySQL credentials in app.py**
```
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password_here'
app.config['MYSQL_DB'] = 'erp_db'
```
## 5. **Run the Flask app**
```
python app.py
```