import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import datetime
import random
from conf.db import engine, get_db
from conf.models import Base, Group, Student, Teacher, Subject, Grade

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 20


def seed_data():
    print("Seeding data...")
    groups = [Group(name=fake.word()) for _ in range(NUMBER_GROUPS)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(NUMBER_TEACHERS)]
    session.add_all(teachers)
    session.commit()

    subjects = [Subject(name=fake.word(), teacher_id=random.choice(teachers).id) for _ in range(NUMBER_SUBJECTS)]
    session.add_all(subjects)
    session.commit()

    students = [Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(NUMBER_STUDENTS)]
    session.add_all(students)
    session.commit()

    grades = []
    for student in students:
        for _ in range(NUMBER_GRADES):
            grades.append(Grade(
                student_id=student.id,
                subject_id=random.choice(subjects).id,
                grade=random.uniform(0, 100),
                grade_date=fake.date_this_year()
            ))
    session.add_all(grades)
    session.commit()


if __name__ == "__main__":
    seed_data()
    print("Seeding completed.")


