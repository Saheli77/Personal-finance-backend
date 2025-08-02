import sqlite3
from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import os

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.db')
JWT_SECRET = os.environ.get('JWT_SECRET', 'supersecretkey')

# Ensure data directory exists
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@auth_bp.route('/api/register', methods=['POST'])
def register():
    import traceback
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400
    
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'User registered'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409
    except Exception as e:
        print('Registration error:', e)
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row and bcrypt.check_password_hash(row[1], password):
        token = jwt.encode({
            'user_id': row[0],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, JWT_SECRET, algorithm='HS256')
        return jsonify({'status': 'success', 'token': token})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

@auth_bp.route('/api/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'status': 'error', 'message': 'Token required'}), 401
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = data['user_id']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return jsonify({'status': 'success', 'user': {'id': row[0], 'username': row[1]}})
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except Exception:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

# Call this at startup
def setup_auth(app):
    bcrypt.init_app(app)
    init_db()
    app.register_blueprint(auth_bp)
