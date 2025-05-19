
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'logs.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            zone TEXT,
            house TEXT,
            work TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        c.execute("INSERT INTO logs (date, zone, house, work) VALUES (?, ?, ?, ?)", (
            request.form['date'],
            request.form['zone'],
            request.form['house'],
            request.form['work']
        ))
        conn.commit()
    c.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
