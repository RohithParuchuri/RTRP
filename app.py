from flask import Flask, render_template, url_for, redirect, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

  
def get_db_connection():
    conn = sqlite3.connect('database.db', timeout=10)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn
 
app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password") 
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cursor.fetchone()
        cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
        ValidUser = cursor.fetchone()
        
        conn.close()
        
        if not user:
            return "No User Name Found"
        elif check_password_hash(user["password"], password):
            return "Successful Login!"
        else:
            return "Login Failed"

    return render_template('login.html')

@ app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password") 
        hashed_password = generate_password_hash(password)
        rpassword = request.form.get("Repassword")
        if password != rpassword:
            return "Error: Passwords do not match"
       
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit() 
        except sqlite3.IntegrityError:
            return "Error: Username already exists"
        
        conn.close()

        return redirect(url_for('login')) 
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)