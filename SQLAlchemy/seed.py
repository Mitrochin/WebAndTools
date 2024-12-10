from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from conf.db import engine
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

SUBJECTS_LIST = [
    "Mathematics", "Physics", "Chemistry", "Biology",
    "History of Ukraine", "Ukrainian Literature", "Computer Science", "Art"
]


def seed_data():
    print("Seeding data...")

    # Создание и добавление групп
    groups = [Group(name=fake.word()) for _ in range(NUMBER_GROUPS)]
    session.add_all(groups)
    session.commit()

    # Создание и добавление преподавателей
    teachers = [Teacher(name=fake.name()) for _ in range(NUMBER_TEACHERS)]
    session.add_all(teachers)
    session.commit()

    # Создание и добавление предметов из списка
    subjects = []
    for _ in range(NUMBER_SUBJECTS):
        subject_name = random.choice(SUBJECTS_LIST)
        teacher_id = random.choice(teachers).id
        subject = Subject(name=subject_name, teacher_id=teacher_id)
        subjects.append(subject)
        print(f"Assigned subject name: {subject_name}, teacher ID: {teacher_id}")

    session.add_all(subjects)
    session.commit()

    # Проверка сохранения предметов в базе данных
    saved_subjects = session.query(Subject).all()
    for subject in saved_subjects:
        print(f"Saved Subject: ID: {subject.id}, Name: {subject.name}, Teacher ID: {subject.teacher_id}")

    # Создание и добавление студентов
    students = [Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(NUMBER_STUDENTS)]
    session.add_all(students)
    session.commit()

    # Создание и добавление оценок
    grades = []
    for student in students:
        for _ in range(NUMBER_GRADES):
            subject = random.choice(subjects)
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=random.uniform(0, 100),
                grade_date=fake.date_this_year()
            )
            grades.append(grade)
            print(f"Student: {student.name}, Subject: {subject.name}, Grade: {grade.grade}")

    session.add_all(grades)
    session.commit()


if __name__ == "__main__":
    seed_data()
    print("Seeding completed.")




