from flask import Flask, redirect, render_template, url_for
import sqlite3

app = Flask(__name__)

# Function to retrieve logs from the database
def get_logs():
    conn = sqlite3.connect('syslogs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs ORDER BY id DESC')  # Fetch all logs ordered by ID (latest first)
    logs = cursor.fetchall()
    conn.close()
    return logs

@app.route('/')
def logs():
    # Get logs from the database
    logs = get_logs()
    
    # Render the logs in the frontend
    return render_template('logs.html', logs=logs)

# CRUD Operations:

#DELETE:
@app.route('/delete/<int:log_id>')
def delete_log(log_id):
    conn = sqlite3.connect('syslogs.db')
    c = conn.cursor()
    c.execute('DELETE FROM logs WHERE id = ?', (log_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('logs'))




if __name__ == '__main__':
    app.run(debug=True)
