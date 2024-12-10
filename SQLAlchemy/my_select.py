from sqlalchemy import create_engine, func, desc, cast, Numeric
from sqlalchemy.orm import sessionmaker
from conf.models import Student, Grade, Group, Subject, Teacher

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    result = session.query(Student.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
        .join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    print("Select 1 results:", result)
    return result


def select_2(subject_id):
    result = session.query(Student.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
        .join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(desc('avg_grade')).limit(1).all()
    print("Select 2 results:", result)
    return result


def select_3(subject_id):
    result = session.query(Group.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
        .join(Student, Student.group_id == Group.id)\
        .join(Grade, Grade.student_id == Student.id)\
        .filter(Grade.subject_id == subject_id)\
        .group_by(Group.id)\
        .all()
    print("Select 3 results:", result)
    return result


def select_4():
    result = session.query(func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')).all()
    print("Select 4 results:", result)
    return result


def select_5(teacher_id):
    result = session.query(Subject.name)\
        .filter(Subject.teacher_id == teacher_id).all()
    print("Select 5 results:", result)
    return result


def select_6(group_id):
    result = session.query(Student.name).filter(Student.group_id == group_id).all()
    print("Select 6 results:", result)
    return result


def select_7(group_id, subject_id):
    result = session.query(Student.name, Grade.grade)\
        .join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    print("Select 7 results:", result)
    return result


def select_8(teacher_id):
    result = session.query(Subject.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
        .join(Grade).filter(Subject.teacher_id == teacher_id).group_by(Subject.id).all()
    print("Select 8 results:", result)
    return result


def select_9(student_id):
    result = session.query(Subject.name)\
        .join(Grade).filter(Grade.student_id == student_id).all()
    print("Select 9 results:", result)
    return result


def select_10(student_id, teacher_id):
    result = session.query(Subject.name)\
        .join(Grade).filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).all()
    print("Select 10 results:", result)
    return result

# Выполнение запросов для проверки
select_1()
select_2(1)  # замените 1 на ID предмета, который вы хотите проверить
select_3(1)  # замените 1 на ID предмета, который вы хотите проверить
select_4()
select_5(1)  # замените 1 на ID учителя, которого вы хотите проверить
select_6(1)  # замените 1 на ID группы, которую вы хотите проверить
select_7(1, 1)  # замените 1 на ID группы и предмета, которые вы хотите проверить
select_8(1)  # замените 1 на ID учителя, которого вы хотите проверить
select_9(1)  # замените 1 на ID студента, которого вы хотите проверить
select_10(1, 1)  # замените 1 на ID студента и учителя, которых вы хотите проверить


