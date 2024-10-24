from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'user': 'root',
    'password': 'example',
    'host': 'db',  # Ändere 'localhost' zu 'db'
    'database': 'regalverwaltung',
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
        ORDER BY shelves.level DESC, shelves.position DESC
    ''')
    shelves = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', shelves=shelves)

@app.route('/search', methods=['GET'])
def search():
    project_number = request.args.get('project_number')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT shelves.id AS shelf_id, shelves.level, shelves.position, boxes.id AS box_id, boxes.project_number
        FROM shelves
        LEFT JOIN boxes ON shelves.id = boxes.shelf_id
        WHERE boxes.project_number = %s
        ORDER BY shelves.level DESC, shelves.position DESC
    ''', (project_number,))
    shelves = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if a box was found
    found_box = None
    for shelf in shelves:
        if shelf['project_number'] == project_number:
            found_box = shelf
            break

    message = None
    if found_box:
        message = f"Kiste gefunden: Regalebene {found_box['level']}, Fach {found_box['position']}"
    else:
        message = "Keine Kiste gefunden"

    return render_template('index.html', shelves=shelves, search_project_number=project_number, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)