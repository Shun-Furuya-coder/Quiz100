from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='frontend')
CORS(app)

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

from signup import register_user
from login import login_user

# Route
@app.route('/login', methods=['POST'])
def login():
    return login_user()

@app.route('/register', methods=['POST'])
def register():
    return register_user()

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM quizzes")
    quizzes = cur.fetchall()
    conn.close()

    quizzes_list = [dict(quiz) for quiz in quizzes]
    return jsonify(quizzes_list)

@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz_details(quiz_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,))
    quiz = cur.fetchone()

    cur.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
    questions = cur.fetchall()

    questions_list = []
    for question in questions:
        cur.execute("SELECT * FROM options WHERE question_id = ?", (question['question_id'],))
        options = cur.fetchall()
        question_dict = dict(question)
        question_dict['options'] = [dict(option) for option in options]
        questions_list.append(question_dict)

    quiz_details = dict(quiz)
    quiz_details['questions'] = questions_list

    conn.close()
    return jsonify(quiz_details)

@app.route('/api/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.get_json()
    quiz_id = data['quiz_id']
    user_answers = data['answers']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
    questions = cur.fetchall()

    score = 0
    total_questions = len(questions)

    for question in questions:
        correct_option = cur.execute("SELECT * FROM options WHERE question_id = ? AND is_correct = 1", (question['question_id'],)).fetchone()
        if correct_option['option_id'] == user_answers[str(question['question_id'])]:
            score += 1

    conn.close()
    return jsonify({'score': score, 'total_questions': total_questions})

@app.route('/api/create_quiz', methods=['POST'])
def create_quiz():
    data = request.get_json()
    quiz_name = data['title']
    questions = data['questions']

    conn = get_db_connection()
    cur = conn.cursor()

    # クイズタイトルをquizzesテーブルに挿入
    cur.execute("INSERT INTO quizzes (title) VALUES (?)", (quiz_name,))
    quiz_id = cur.lastrowid  # 新しく挿入されたクイズのIDを取得

    # 各質問と選択肢をデータベースに挿入
    for question in questions:
        cur.execute("INSERT INTO questions (quiz_id, question_text) VALUES (?, ?)", (quiz_id, question['question']))
        question_id = cur.lastrowid
        for i, option_text in enumerate(question['options']):
            is_correct = (i + 1 == question['answer'])
            cur.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (?, ?, ?)", (question_id, option_text, is_correct))

    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Quiz created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
