from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'database3'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Home page
@app.route('/')
def index():
    role = session.get('role', 'guest')
    conn = get_db_connection()
    books = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('index.html', books=books, role=role)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                session['role'] = user['role']
                session['username'] = username
                return redirect(url_for('index'))
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Add book (admin only)
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (title, author))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
    return render_template('add_book.html')

# Borrow book (user only)
@app.route('/borrow/<int:book_id>')
def borrow(book_id):
    if session.get('role') != 'user':
        return redirect(url_for('index'))
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO borrow (username, book_id) VALUES (%s, %s)', (session['username'], book_id))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
