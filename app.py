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
def book():
    name = request.form.get('name')
    phone = request.form.get('phone')
    category = request.form.get('category')
    service = request.form.get('service')
    shoot_date = request.form.get('shoot_date')
    address = request.form.get('address')

    conn = sqlite3.connect('studio.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, phone, category, service, shoot_date, address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, phone, category, service, shoot_date, address))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

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
    
