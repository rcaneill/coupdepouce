from flask_app import db, Teacher, Student
from werkzeug.security import generate_password_hash

N_prof = 5
N_students = 10
prof_name = "prof"
student_name = "student"

# delete all previous users
'''
for teacher in Teacher.query.all():
    if prof_name in teacher.name:
        db.session.delete(teacher)
for student in Student.query.all():
    if student_name in student.name:
        db.session.delete(student)
'''

# create teachers
for i in range(N_prof):
    username=prof_name+str(i)
    for teacher in Teacher.query.filter_by(username=username).all():
        db.session.delete(teacher)
    prof = Teacher(
        username=username,
        email="",
        name=prof_name,
        surname=str(i),
        password_hash=generate_password_hash(prof_name+str(i)),
        email_confirmed=True
    )
    db.session.add(prof)
    print(f"prof {i} created")

# create students
for i in range(N_students):
    username=student_name+str(i)
    for student in Student.query.filter_by(username=username).all():
        db.session.delete(student)
    student = Student(
        username=student_name+str(i),
        email="",
        name=student_name,
        surname=str(i),
        password_hash=generate_password_hash(student_name+str(i)),
        email_confirmed=True
    )
    db.session.add(student)
    print(f"student {i} created")

db.session.commit()