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

@app.route('/manage')
def manage():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT shelves.id AS shelf_id, shelves.level, shelves.position, boxes.id AS box_id, boxes.project_number
        FROM shelves
        LEFT JOIN boxes ON shelves.id = boxes.shelf_id
        ORDER BY shelves.level DESC, shelves.position DESC
    ''')
    boxes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage.html', boxes=boxes)

@app.route('/add_project', methods=['POST'])
def add_project():
    project_number = request.form['project_number']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Finde die nächste freie Kiste
    cursor.execute('''
        SELECT shelves.id AS shelf_id
        FROM shelves
        LEFT JOIN boxes ON shelves.id = boxes.shelf_id
        WHERE boxes.id IS NULL
        ORDER BY shelves.level DESC, shelves.position DESC
        LIMIT 1
    ''')
    shelf = cursor.fetchone()
    
    if shelf:
        cursor.execute('''
            INSERT INTO boxes (project_number, shelf_id)
            VALUES (%s, %s)
        ''', (project_number, shelf['shelf_id']))
        conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for('manage'))

@app.route('/edit/<int:box_id>', methods=['GET', 'POST'])
def edit(box_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        if 'delete' in request.form:
            cursor.execute('DELETE FROM boxes WHERE id = %s', (box_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('manage'))
        else:
            project_number = request.form['project_number']
            cursor.execute('UPDATE boxes SET project_number = %s WHERE id = %s', (project_number, box_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('manage'))
    
    cursor.execute('SELECT * FROM boxes WHERE id = %s', (box_id,))
    box = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('edit.html', box=box)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)