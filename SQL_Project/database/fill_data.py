from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 20


def create_tables():
    with sqlite3.connect('university.db') as con:
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            group_id INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            teacher_id INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_id INTEGER,
                            subject_id INTEGER,
                            grade INTEGER,
                            grade_date DATE)''')
        con.commit()


def generate_fake_data():
    fake = faker.Faker()

    groups = [fake.word() for _ in range(NUMBER_GROUPS)]
    students = [(fake.name(), randint(1, NUMBER_GROUPS)) for _ in range(NUMBER_STUDENTS)]
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    subjects = [(fake.word(), randint(1, NUMBER_TEACHERS)) for _ in range(NUMBER_SUBJECTS)]

    grades = []
    for student_id in range(1, NUMBER_STUDENTS + 1):
        for _ in range(NUMBER_GRADES):
            subject_id = randint(1, NUMBER_SUBJECTS)
            grade = randint(1, 100)
            grade_date = fake.date_this_year()
            grades.append((student_id, subject_id, grade, grade_date))

    return groups, students, teachers, subjects, grades


def insert_data_to_db(groups, students, teachers, subjects, grades):
    with sqlite3.connect('university.db') as con:
        cur = con.cursor()

        cur.executemany("INSERT INTO groups (name) VALUES (?)", [(g,) for g in groups])
        cur.executemany("INSERT INTO students (name, group_id) VALUES (?, ?)", students)
        cur.executemany("INSERT INTO teachers (name) VALUES (?)", [(t,) for t in teachers])
        cur.executemany("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", subjects)
        cur.executemany("INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (?, ?, ?, ?)", grades)

        con.commit()


if __name__ == "__main__":
    create_tables()
    data = generate_fake_data()
    insert_data_to_db(*data)

