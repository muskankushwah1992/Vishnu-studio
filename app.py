from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('studio.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            category TEXT,
            service TEXT NOT NULL,
            shoot_date TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/book', methods=['POST'])

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    category = request.form.get('category')
    service = request.form.get('service')
    shoot_date = request.form.get('shoot_date')
    address = request.form.get('address')

    conn = sqlite3.connect('studio.db')
    cursor = conn.cursor()
    
    # Table creation with email column just in case
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            category TEXT,
            service TEXT NOT NULL,
            shoot_date TEXT,
            address TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT INTO bookings (name, phone, email, category, service, shoot_date, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, email, category, service, shoot_date, address))
    conn.commit()
    conn.close()

    studio_whatsapp = "918909158011"
    whatsapp_message = f"New Booking Received!\nName: {name}\nPhone: {phone}\nEmail: {email}\nCategory: {category}\nService: {service}\nDate: {shoot_date}\nAddress: {address}"
    
    import urllib.parse
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={studio_whatsapp}&text={encoded_message}"

    return render_template('index.html', success_message="Booking Successful!", whatsapp_url=whatsapp_url)

@app.route('/admin-dashboard')
def admin_dashboard():
    conn = sqlite3.connect('studio.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings ORDER BY id DESC')
    all_bookings = cursor.fetchall()
    conn.close()
    return render_template('admin.html', bookings=all_bookings)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
