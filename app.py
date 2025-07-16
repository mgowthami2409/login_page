from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'users.db'

# Get connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM UserDetails WHERE Email = ?', (email,))
            user = cursor.fetchone()

        if not user:
            flash('Invalid email ID', 'error')
        elif user['Password'] != password:
            flash('Incorrect password', 'error')
        else:
            session['user_id'] = user['Id']
            return render_template('portfolio.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$'
        if not re.match(password_pattern, password):
            flash('Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.', 'error')
            return render_template('register.html')

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM UserDetails WHERE Email = ?", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash('Email already exists', 'error')
                    return render_template('register.html')

                cursor.execute("INSERT INTO UserDetails (Name, Email, Password) VALUES (?, ?, ?)",
                               (name, email, password))
                conn.commit()
                flash('Registration successful. Please login.', 'success')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f'Registration failed: {e}', 'error')

    return render_template('register.html')

@app.route('/users')
def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    users = cursor.execute('SELECT * FROM UserDetails').fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
