from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import json
import os
import bcrypt


routes = Blueprint('routes', __name__)

# تحميل المستخدمين من users.json
def load_users():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # المسار الأساسي للمشروع
    users_file = os.path.join(base_dir, 'users.json')
    with open(users_file, 'r') as f:
        return json.load(f)

# التحقق من اسم المستخدم وكلمة السر
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
USERS_FILE = os.path.join(BASE_DIR, '..', 'users.json')

def authenticate(username, password):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    for user in users:
        if user['username'] == username and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return user
    return None

# 🟢 صفحة تسجيل الدخول
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = authenticate(username, password)
        if user:
            session['user'] = username
            session['role'] = user.get('role', 'viewer')
            return redirect(url_for('routes.dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

# 🟢 صفحة لوحة التحكم
@routes.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('routes.login'))

    return render_template('dashboard.html', user=session['user'], role=session.get('role', 'viewer'))

# 🔴 تسجيل الخروج
@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))
@routes.route('/')
def index():
    return redirect(url_for('routes.login'))
