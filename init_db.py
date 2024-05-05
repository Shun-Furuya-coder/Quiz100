import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database """
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    """ create tables in the SQLite database """
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS quizzes;
    DROP TABLE IF EXISTS questions;
    DROP TABLE IF EXISTS options;
    DROP TABLE IF EXISTS quiz_scores;

    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );

    CREATE TABLE quizzes (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_by INTEGER,
        FOREIGN KEY (created_by) REFERENCES users(user_id)
    );

    CREATE TABLE questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
    );

    CREATE TABLE options (
        option_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        option_text TEXT NOT NULL,
        is_correct BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (question_id) REFERENCES questions(question_id)
    );

    CREATE TABLE quiz_scores (
        score_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    conn.commit()

def insert_sample_data(conn):
    """ insert sample quiz data into the SQLite database """
    cur = conn.cursor()
    # Insert quizzes
    cur.execute("INSERT INTO quizzes (title, created_by) VALUES ('Science Quiz', 1), ('Python Quiz', 1), ('Math Quiz', 1)")
    cur.execute("INSERT INTO questions (quiz_id, question_text) VALUES (1, 'What is the chemical symbol for the element oxygen?'), (1, 'What planet is known as the Red Planet?'), (1, 'What is the hardest natural substance on Earth?'), (2, 'Which of these is not a core data type in Python?'), (2, 'What keyword is used to create a function in Python?'), (2, 'What does ''len()'' function do in Python?'), (3, 'What is the square root of 144?'), (3, 'What is 50 times 5?'), (3, 'What is 15% of 200?')")
    cur.execute("INSERT INTO options (question_id, option_text, is_correct) VALUES (1, 'O', 1), (1, 'Ox', 0), (1, 'Om', 0), (1, 'Oz', 0), (2, 'Earth', 0), (2, 'Mars', 1), (2, 'Venus', 0), (2, 'Mercury', 0), (3, 'Gold', 0), (3, 'Iron', 0), (3, 'Diamond', 1), (3, 'Quartz', 0), (4, 'Lists', 0), (4, 'Dictionary', 0), (4, 'Tuples', 0), (4, 'Class', 1), (5, 'function', 0), (5, 'def', 1), (5, 'create', 0), (5, 'func', 0), (6, 'Prints the length of an object', 0), (6, 'Returns the length of an object', 1), (6, 'Deletes an item from a list', 0), (6, 'None of the above', 0), (7, '12', 1), (7, '14', 0), (7, '16', 0), (7, '18', 0), (8, '250', 1), (8, '205', 0), (8, '505', 0), (8, '500', 0), (9, '30', 1), (9, '25', 0), (9, '20', 0), (9, '35', 0)")
    conn.commit()

if __name__ == '__main__':
    conn = create_connection('database.db')
    create_tables(conn)
    insert_sample_data(conn)
    conn.close()
    print("Database initialized and sample data inserted successfully.")
