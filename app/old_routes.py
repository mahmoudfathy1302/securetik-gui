from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
#from .firewall import get_firewall_status, apply_firewall_rule
#from .ids import get_ids_logs
from werkzeug.security import check_password_hash
import json
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/firewall', methods=['GET'])
def firewall_status():
    return jsonify(get_firewall_status())

@main.route('/api/firewall', methods=['POST'])
def add_firewall_rule():
    data = request.json
    result = apply_firewall_rule(data)
    return jsonify(result)

@main.route('/api/ids/logs', methods=['GET'])
def ids_logs():
    return jsonify(get_ids_logs())

# Logout route
@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


# إنشاء Blueprint
routes = Blueprint('routes', __name__)

# تحميل المستخدمين من الملف
def load_users():
    users_file = os.path.join(os.path.dirname(__file__), '..', 'users.json')
    with open(users_file, 'r') as f:
        return json.load(f)

# التحقق من صحة البيانات
def authenticate(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and check_password_hash(user['password_hash'], password):
            return user
    return None

# صفحة تسجيل الدخول
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

# صفحة لوحة التحكم
@routes.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('routes.login'))
    return render_template('dashboard.html', user=session['user'], role=session.get('role', 'viewer'))

# تسجيل الخروج
@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))
