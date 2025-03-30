from flask import Flask, render_template, url_for, redirect, request, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

  
def get_db_connection():
    conn = sqlite3.connect('database.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn
 
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem" 
app.secret_key = "einlskyehkl345j jopiw34;klj648jlkrj84kl5320kdlfmyt6'd'l[p34kuj3p]"

@app.route('/')
def home():
    profileSec = session.get('profileSec', 0)
    uName = session.get('username', 'None')
    return render_template('index.html', profileSec=profileSec)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if session.get('profileSec') == 1:
            return redirect(url_for("profile"))
        
        username = request.form.get("username")
        password = request.form.get("password") 
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()

        if not user:
            return "No User Name Found"
        elif check_password_hash(user["password"], password):
            session['username'] = username
            session['profileSec'] = 1
            flash(f"Thanks for posting!", category="success")
            return redirect(url_for("profile"))
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('profileSec') != 1:
        flash("You must be logged in to access the profile page.", category="danger")
        return redirect(url_for('login'))
    return render_template('profile.html', username = session.get('username'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['profileSec'] = 0
    session['username'] = 'None'
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)