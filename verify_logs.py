import sqlite3

def verify_logs():
    # Connect to the SQLite database
    conn = sqlite3.connect('syslogs.db')
    cursor = conn.cursor()

    # Query to select all logs from the logs table
    cursor.execute("SELECT * FROM logs")

    # Fetch and display all rows
    rows = cursor.fetchall()

    if not rows:
        print("No logs found in the database.")
    else:
        # Print the logs in a readable format
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Timestamp: {row[1]}")
            print(f"Source IP: {row[2]}")
            print(f"Severity: {row[3]}")
            print(f"Log Message: {row[4]}")
            print("-" * 50)

    # Close the connection
    conn.close()

# Call the function to verify logs
verify_logs()
