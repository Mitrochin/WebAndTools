import sqlite3


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('student_db.sqlite')
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return connection
