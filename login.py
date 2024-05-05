from flask import request, jsonify
import sqlite3

DATABASE = 'quiz_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cur.fetchone()
            if user:
                return jsonify({'status': 'success', 'message': 'Login successfully'})
            else:
                return jsonify({'status': 'error', 'message': 'Account or password incorrect'}), 401
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        finally:
            cur.close()
            conn.close()
