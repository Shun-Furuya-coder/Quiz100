from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$hunF172633'
app.config['MYSQL_DB'] = 'quiz100'

mysql = MySQL(app)

def test_query():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    for result in results:
        print(result)
    cur.close()

if __name__ == '__main__':
    with app.app_context():
        test_query()