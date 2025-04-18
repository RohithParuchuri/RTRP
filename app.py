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
    uid = session.get('user_id', 0)
    isDoc = session.get('isDoc', 0)
    return render_template('index.html', profileSec=profileSec)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('profileSec') == 1:
        return redirect(url_for("profile"))
    
    if request.method == "POST":

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

            session['user_id'] = user['id']

            session['isDoc'] = user['is_doctor']
            print('working')
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
        isDoc = request.form.get("isDoctor")

        if isDoc == None:
            isDoc = 0
        else:
            isDoc = 1

        if password != rpassword:
            return "Error: Passwords do not match"
       
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO user (username, password, is_doctor) VALUES (?, ?, ?)', (username, hashed_password, isDoc))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO user_profile (user_id) VALUES (?)', (user_id,))
            session['isDoc'] = isDoc
            session['user_id']=user_id
            conn.commit()
        except sqlite3.IntegrityError:
            return "Error: Username already exists"
        finally:
            conn.close()

        return redirect(url_for('login')) 
    return render_template('register.html')

@app.route('/docpage', methods=['GET', 'POST'])
def docpage():
    if session.get('isDoc', 0) == 0:
        return redirect(url_for('login'))
    print(session.get('isDoc'))
    return render_template('docpage.html')

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if session.get('isDoc', 0) == 1:
        return redirect(url_for('login'))
    return render_template('inventory.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('profileSec') != 1:
        flash("You must be logged in to access the profile page.", category="danger")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.username, p.full_name, p.age, p.sex, p.addres, 
               p.phone, p.email, p.emergency_contact, p.blood_type
        FROM user u
        JOIN user_profile p ON u.id = p.user_id
        WHERE u.username = ?;
    ''', (session.get("username"),))
    user_data = cursor.fetchone()
    conn.close()
    d = dict(user_data) if user_data else None
    return render_template('profile.html', username = session.get('username'), user_data=d, isDoc = session.get('isDoc'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['profileSec'] = 0
    session['username'] = 'None'
    return redirect(url_for('home'))

@app.route('/editProfile', methods = ['GET', 'POST'])
def editProfile():
    if request.method == "POST":
        try:
            full_name = request.form["full_name"]
            age = request.form["age"]
            sex = request.form["sex"]
            address = request.form["address"]
            phone = request.form["phone"]
            email = request.form["email"]
            emergency_contact = request.form["emergency_contact"]
            blood_type = request.form["blood_type"]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user_profile
                SET full_name = ?,
                    age = ?,
                    sex = ?,
                    addres = ?,
                    phone = ?,
                    email = ?,
                    emergency_contact = ?,
                    blood_type = ?
                WHERE user_id = ?
            """, (full_name, age, sex, address, phone, email, emergency_contact, blood_type, session.get('user_id')))
            print(session.get('user_id'))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)