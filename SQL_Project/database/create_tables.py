from connect import create_connection


def create_tables():
    with open('university.sql', 'r') as file:
        sql_script = file.read()

    connection = create_connection()
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()

