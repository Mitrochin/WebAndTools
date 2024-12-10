import sqlite3


def execute_query(query_file):
    with open(query_file, 'r') as file:
        query = file.read()
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()
        cur.execute(query)
        return cur.fetchall()


if __name__ == "__main__":
    query_files = [
        'queries/query_1.sql',
        'queries/query_2.sql',
        'queries/query_3.sql',
        'queries/query_4.sql',
        'queries/query_5.sql',
        'queries/query_6.sql',
        'queries/query_7.sql',
        'queries/query_8.sql',
        'queries/query_9.sql',
        'queries/query_10.sql'
    ]

    for query_file in query_files:
        try:
            result = execute_query(query_file)
            if result:
                print(f"Results for {query_file}:\n{result}\n")
            else:
                print(f"No results for {query_file}.")
        except Exception as e:
            print(f"Error executing {query_file}: {e}")


