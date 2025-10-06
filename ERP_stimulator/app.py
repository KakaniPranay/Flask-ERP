from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pranaybalu' # your MySQL password
app.config['MYSQL_DB'] = 'erp_db'

app.secret_key = os.urandom(24)

mysql = MySQL(app)


@app.route('/')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    return render_template('dashboard.html', products=products, orders=orders)


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    stock = request.form['stock']
    price = request.form['price']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products(name, stock, price) VALUES(%s,%s,%s)", (name, stock, price))
    mysql.connection.commit()
    return redirect('/')

@app.route('/place_order', methods=['POST'])
def place_order():
    product_id_str = request.form.get('product_id', '').strip()
    quantity_str = request.form.get('quantity', '').strip()

    if not product_id_str or not quantity_str:
        flash("Please select a product and enter quantity.", "danger")
        return redirect(url_for('dashboard'))

    product_id = int(product_id_str)
    quantity = int(quantity_str)

    cur = mysql.connection.cursor()
    cur.execute("SELECT stock, price FROM products WHERE id=%s", (product_id,))
    result = cur.fetchone()

    if result is None or result[0] <= 0:
        flash("No stock available for this product!", "warning")
        return redirect(url_for('dashboard'))

    stock, price = result

    if quantity > stock:
        flash(f"Only {stock} items available in stock!", "warning")
        return redirect(url_for('dashboard'))

    total = quantity * price
    try:
        cur.execute("UPDATE products SET stock = stock - %s WHERE id=%s", (quantity, product_id))
        cur.execute("INSERT INTO orders(product_id, quantity, total, status) VALUES(%s,%s,%s,'Completed')",
                    (product_id, quantity, total))
        mysql.connection.commit()

        cur.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
        order_id = cur.fetchone()[0]
        cur.execute("INSERT INTO billing(order_id, amount) VALUES(%s,%s)", (order_id, total))
        mysql.connection.commit()

        flash("Order placed successfully!", "success")
    except:
        mysql.connection.rollback()
        flash("Transaction failed!", "danger")
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
