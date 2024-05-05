import sqlite3
from flask import request, jsonify
import traceback

DATABASE = 'quiz_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def register_user():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        print("Entered register_user")
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            print("Before SELECT")
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            print("After SELECT")
            if cur.fetchone():
                print("Return json error")
                return jsonify({'status': 'error', 'message': 'Account already exists'}), 409
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            print("After INSERT")
            conn.commit()
            return jsonify({'status': 'success', 'message': 'Registered successfully'})
    except Exception as e:
        print("Entered exception")
        print(f"An error occurred: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': 'An error occurred during registration'}), 500
    finally:
        print("Entered finally")
        cur.close()
        conn.close()
