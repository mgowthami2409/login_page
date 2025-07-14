from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQL Server connection
def get_db_connection():
    return pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=SAP-TRAINING1\SQLEXPRESS;'
    'DATABASE=MyAppDB;'
    'Trusted_Connection=yes;'
    )

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM UserDetails WHERE Email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            flash('Invalid email ID', 'error')
        elif user[3] != password:
            flash('Incorrect password', 'error')
        else:
            session['user_id'] = user.Id
            return render_template('portfolio.html')  # Or redirect to dashboard

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
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO UserDetails (Name, Email, Password) VALUES (?, ?, ?)", 
                           (name, email, password))

            conn.commit()
            conn.close()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except pyodbc.IntegrityError:
            flash('Email already exists', 'error')
        except Exception as e:
            flash(f'Registration failed: {e}', 'error')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
