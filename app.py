from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        address TEXT,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format!', 'danger')
            return redirect(url_for('index'))

        try:
            c.execute("INSERT INTO contacts (first_name, last_name, address, email, phone) VALUES (?, ?, ?, ?, ?)",
                      (first_name, last_name, address, email, phone))
            conn.commit()
            flash('Contact added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Email or Phone already exists!', 'danger')

    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Contact deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        try:
            c.execute('''UPDATE contacts SET first_name = ?, last_name = ?, address = ?, email = ?, phone = ?
                         WHERE id = ?''', (first_name, last_name, address, email, phone, id))
            conn.commit()
            flash('Contact updated!', 'success')
        except sqlite3.IntegrityError:
            flash('Email or Phone already exists!', 'danger')
        return redirect(url_for('index'))

    c.execute("SELECT * FROM contacts WHERE id = ?", (id,))
    contact = c.fetchone()
    conn.close()
    return render_template('update.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)
