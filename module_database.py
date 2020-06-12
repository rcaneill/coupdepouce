from flask_app import db, login_manager
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash

################################################################################
# Definition of the database
# Definition of load_user
################################################################################


@login_manager.user_loader
def load_user(user_id):
    # We need to know if this is a student or a teacher
    user = Teacher.query.filter_by(username=user_id).first()
    if user is not None:
        return user
    else:
        return Student.query.filter_by(username=user_id).first()

"""
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username
"""

association_table_teachers_students = db.Table(
    'association_teachers_students',
    db.metadata,
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id', onupdate="CASCADE", ondelete="CASCADE"))
)

association_table_classrooms_students = db.Table(
    'association_classrooms_students',
    db.metadata,
    db.Column('classroom_id', db.Integer, db.ForeignKey('classrooms.id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('student_id', db.Integer, db.ForeignKey('students.id', onupdate="CASCADE", ondelete="CASCADE"))
)

class Teacher(UserMixin, db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    admin =  db.Column(db.Boolean, default=True)
    last_connection = db.Column(db.DateTime, default=datetime.now())
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, default=None)
    email_confirmed_on = db.Column(db.DateTime, default=None)

    students = db.relationship(
        "Student",
        back_populates="teachers",
        secondary=association_table_teachers_students
    )
    classrooms = db.relationship("Classroom", back_populates="teacher")
    activities = db.relationship("Activity", back_populates="teacher")
    notifications = db.relationship("NotificationTeacher", back_populates="owner")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Student(UserMixin, db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    admin =  db.Column(db.Boolean, default=False)
    last_connection = db.Column(db.DateTime, default=datetime.now())
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, default=None)
    email_confirmed_on = db.Column(db.DateTime, default=None)

    teachers = db.relationship(
        "Teacher",
        back_populates="students",
        secondary=association_table_teachers_students
    )
    classrooms = db.relationship(
        "Classroom",
        back_populates="students",
        secondary=association_table_classrooms_students
    )
    helping_hands = db.relationship("HelpingHandLog", back_populates="student")
    notifications = db.relationship("NotificationStudent", back_populates="owner")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class NotificationTeacher(db.Model):
    __tablename__ = "notifications_teacher"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(128))
    content = db.Column(db.Text)
    is_read =  db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    owner_id = db.Column(db.Integer, db.ForeignKey('teachers.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    owner = db.relationship("Teacher", back_populates="notifications")

class NotificationStudent(db.Model):
    __tablename__ = "notifications_student"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(128))
    content = db.Column(db.Text)
    is_read =  db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    owner_id = db.Column(db.Integer, db.ForeignKey('students.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    owner = db.relationship("Student", back_populates="notifications")

class Classroom(db.Model):
    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    teacher = db.relationship("Teacher", back_populates="classrooms")
    #student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    students = db.relationship(
        "Student",
        back_populates="classrooms",
        secondary=association_table_classrooms_students
    )

    activities = db.relationship("Activity", back_populates="classrooms")

    def __repr__(self):
        return f"<Classroom(name={self.name}, teacher={self.teacher})>"


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    teacher = db.relationship("Teacher", back_populates="activities")
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    classrooms = db.relationship("Classroom", back_populates="activities")

    questions = db.relationship("Question", back_populates="activity")


class Question(db.Model):

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    n_question = db.Column(db.Integer)
    title = db.Column(db.String(128)) #e.g. Q 1.4.2

    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    activity = db.relationship("Activity", back_populates="questions")

    helping_hands = db.relationship("HelpingHand", back_populates="question")

class HelpingHand(db.Model):

    __tablename__ = "helping_hands"

    id = db.Column(db.Integer, primary_key=True)
    n_helping_hand = db.Column(db.Integer)
    content = db.Column(db.Text)

    #question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=True)
    #question = db.relationship("Question", foreign_keys=question_id)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    question = db.relationship("Question", back_populates="helping_hands")

    students = db.relationship("HelpingHandLog", back_populates="helping_hand")

"""
class StudentClass(db.Model):

    __tablename__ = "student_classes"

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=True)
    classroom = db.relationship('Classroom', foreign_keys=classroom_id)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    student = db.relationship('User', foreign_keys=student_id)
"""

"""
class StudentTeacher(db.Model):

    __tablename__ = "student_teachers"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    student = db.relationship('User', foreign_keys=student_id)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    teacher = db.relationship('User', foreign_keys=teacher_id)
"""

"""
class ActivityAccess(db.Model):

    __tablename__ = "activity_accesses"

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=True)
    classroom = db.relationship('Classroom', foreign_keys=classroom_id)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=True)
    activity = db.relationship('Activity', foreign_keys=activity_id)
"""

class HelpingHandLog(db.Model):
    __tablename__ = "helping_hand_logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    student_id = db.Column(db.Integer, db.ForeignKey('students.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    student = db.relationship('Student', back_populates="helping_hands")
    helping_hand_id = db.Column(db.Integer, db.ForeignKey('helping_hands.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
    helping_hand = db.relationship('HelpingHand', back_populates="students")
