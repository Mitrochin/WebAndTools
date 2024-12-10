from sqlalchemy import func, desc, cast, Numeric, and_
from conf.db import get_db
from conf.models import Student, Grade, Group, Subject, Teacher


# Показать пять лучших балов
def select_1():
    with next(get_db()) as session:
        result = session.query(Student.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
            .join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
        print("Select 1 results:", result)
        return result


# Показать высший бал
def select_2(subject_id):
    with next(get_db()) as session:
        result = session.query(
            Student.name.label("Student_Name"),
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("Avg_Grade")
        ).join(Grade, Grade.student_id == Student.id)\
        .filter(Grade.subject_id == subject_id)\
        .group_by(Student.id, Student.name)\
        .order_by(desc("Avg_Grade"))\
        .limit(1)\
        .all()
        print(f"Select 2 results for subject {subject_id}:", result)
        return result


def select_3(subject_id):
    with next(get_db()) as session:
        result = session.query(Group.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
            .join(Student, Student.group_id == Group.id)\
            .join(Grade, Grade.student_id == Student.id)\
            .filter(Grade.subject_id == subject_id)\
            .group_by(Group.id)\
            .all()
        print(f"Select 3 results for subject {subject_id}:", result)
        return result


def select_4():
    with next(get_db()) as session:
        result = session.query(func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')).all()
        print("Select 4 results:", result)
        return result


def select_5(teacher_id):
    with next(get_db()) as session:
        result = session.query(Subject.name)\
            .filter(Subject.teacher_id == teacher_id).all()
        print(f"Select 5 results for teacher {teacher_id}:", result)
        return result


def select_6(group_id):
    with next(get_db()) as session:
        result = session.query(Student.name).filter(Student.group_id == group_id).all()
        print(f"Select 6 results for group {group_id}:", result)
        return result


def select_7(group_id, subject_id):
    with next(get_db()) as session:
        result = session.query(Student.name, Grade.grade)\
            .join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
        print(f"Select 7 results for group {group_id} and subject {subject_id}:", result)
        return result


def select_8(teacher_id):
    with next(get_db()) as session:
        result = session.query(Subject.name, func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade'))\
            .join(Grade).filter(Subject.teacher_id == teacher_id).group_by(Subject.id).all()
        print(f"Select 8 results for teacher {teacher_id}:", result)
        return result


def select_09(student_id):
    with next(get_db()) as session:
        result = session.query(
            Student.name.label("Student_Name"),
            Subject.name.label("Subject_Name")
        ).join(Grade, Grade.student_id == Student.id)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .filter(Grade.student_id == student_id)\
        .group_by(Student.name, Subject.name)\
        .all()
        print(f"Select 09 results for student {student_id}:", result)
        return result


def select_10(student_id, teacher_id):
    with next(get_db()) as session:
        result = session.query(
            Student.name.label("Student_Name"),
            Subject.name.label("Subject_Name"),
            Teacher.name.label("Teacher_Name")
        ).join(Grade, Grade.student_id == Student.id)\
        .join(Subject, Grade.subject_id == Subject.id)\
        .join(Teacher, Subject.teacher_id == Teacher.id)\
        .filter(
            Grade.student_id == student_id,
            Teacher.id == teacher_id
        ).group_by(
            Student.name,
            Subject.name,
            Teacher.name
        ).all()
        print(f"Select 10 results for student {student_id} and teacher {teacher_id}:", result)
        return result

# Проверки
if __name__ == "__main__":
    #print(select_1())
    #print(select_2(1))
    #print(select_3(1))
    #print(select_4())
    #print(select_5(1))
    #print(select_6(1))
    #print(select_7(1, 1))
    #print(select_8(1))
    #print(select_09(11))
    print(select_10(1, 1))
