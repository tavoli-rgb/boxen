from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'user': 'root',
    'password': 'example',
    'host': 'db',
    'database': 'regalverwaltung'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT shelves.id AS shelf_id, shelves.level, shelves.position, boxes.id AS box_id, boxes.project_number
        FROM shelves
        LEFT JOIN boxes ON shelves.id = boxes.shelf_id
        ORDER BY shelves.level, shelves.position
    ''')
    shelves = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', shelves=shelves)

@app.route('/assign', methods=['POST'])
def assign():
    project_number = request.form['project_number']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM boxes WHERE project_number IS NULL LIMIT 1')
    box = cursor.fetchone()
    if box:
        cursor.execute('UPDATE boxes SET project_number = %s WHERE id = %s', (project_number, box[0]))
        conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/remove/<int:box_id>')
def remove(box_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE boxes SET project_number = NULL WHERE id = %s', (box_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)